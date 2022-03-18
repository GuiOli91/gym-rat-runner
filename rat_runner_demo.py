import os

import pandas as pd
import numpy as np
import pygame as pg


# see if we can load more than standard BMP
if not pg.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

# game cosntants
SPACES = 10
HEIGHT, WIDTH = 720, 720
UNIT_HEIGHT, UNIT_WIDTH = HEIGHT//(SPACES+2), WIDTH//(SPACES+2)

# WIN = pg.display.set_mode((WIDTH, HEIGHT))
SCREENRECT = pg.Rect(0, 0, WIDTH, HEIGHT)
SCORE = 0
DARK_GREEN = (21, 89, 33)
MAZE_FILE = "Open_Maze.csv"

# Scores
MOVE_SCORE = -1
WALL_SCORE = -10
CAT_SCORE = -1000
CHEESE_SCORE = 1000

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "src", "gym_rat_runner", "images", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface.convert()


class Rat(pg.sprite.Sprite):
    """Represents the Agent as a rat trying to catch a cheese"""

    speed = 10
    images = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)

        self.image = pg.transform.scale(self.images[0], (UNIT_WIDTH, UNIT_HEIGHT))
        self.rect = self.image.get_rect(bottomleft=(0 + UNIT_WIDTH, HEIGHT - UNIT_HEIGHT))
        self.origtop = self.rect.top

    def move(self, vmove, hmove):
        if hmove:
            self.rect.move_ip(hmove*UNIT_WIDTH, 0)
            self.rect = self.rect.clamp(SCREENRECT)
        if vmove:
            self.rect.move_ip(0, vmove*UNIT_HEIGHT)
            self.rect = self.rect.clamp(SCREENRECT)

        def switch(pos):
            switch={
                (-1, 1): 7,
                (-1, 0): 6,
                (-1, -1): 5,
                (0, -1): 4,
                (1, -1): 3,
                (1, 0): 2,
                (1, 1): 1,
                (0, 1): 0,
            }
            return switch.get(pos, np.nan)
        sel = switch((hmove, vmove))
        if not np.isnan(sel):
            self.image = self.images[sel]

class Cat(pg.sprite.Sprite):
    """Represents the Enemy as a cat trying to catch the rat"""

    speed = 10
    images = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)

        self.image = pg.transform.scale(self.images[0], (UNIT_WIDTH, UNIT_HEIGHT))
        self.rect = self.image.get_rect(topright=SCREENRECT.center)

class Cheese(pg.sprite.Sprite):
    """Represents the Target for the rat"""

    images = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)

        self.image = pg.transform.scale(self.images[0], (UNIT_WIDTH, UNIT_HEIGHT))
        self.rect = self.image.get_rect(topright = (WIDTH - UNIT_WIDTH,
        UNIT_HEIGHT))
        self.origtop = self.rect.top

class Wall(pg.sprite.Sprite):
    """Builds the Wall to be used in the maze"""

    images = []

    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)

        self.image = pg.transform.scale(self.images[0], (UNIT_WIDTH, UNIT_HEIGHT))
        self.rect = self.image.get_rect(topleft = pos)

class Score(pg.sprite.Sprite):
    """Display the Score on the screen ."""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font(None, 35)
        self.font.set_italic(1)
        self.color = pg.Color("white")
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(10, HEIGHT - 35)

    def update(self):
        """We only update the score in update() when it has changed."""
        if SCORE != self.lastscore:
            self.lastscore = SCORE
            msg = "Score: %d" % SCORE
            self.image = self.font.render(msg, 0, self.color)



def main():
    # Initialize pygame
    pg.init()

    fullscreen = False
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    # Load images, assign to sprite classes
    # (do this before the classes are used, after screen setup)
    img = load_image("rat.gif")
    img = pg.transform.scale(img, (UNIT_WIDTH, UNIT_HEIGHT))
    Rat.images = [pg.transform.rotate(img, i*45) for i in range(8)]
    img = load_image("cat.gif")
    Cat.images = [img]
    img = load_image("cheese.gif")
    Cheese.images = [img]
    img = load_image("wall.gif")
    Wall.images = [img]

    # Decorate the window
    icon = pg.transform.scale(Rat.images[0], (32, 32))
    pg.display.set_icon(icon)
    pg.display.set_caption("Rat Runner")
    pg.mouse.set_visible(0)

    #create a background
    background = pg.Surface(SCREENRECT.size)
    background.fill(DARK_GREEN)
    screen.blit(background, (0,0))
    pg.display.flip()

    # Initialize Game Groups
    all = pg.sprite.RenderUpdates()
    cats = pg.sprite.Group()
    cheeses = pg.sprite.Group()
    walls = pg.sprite.Group()

    # assign default groups to each sprite class
    Rat.containers = all
    Cat.containers = cats, all
    Cheese.containers = cheeses, all
    Wall.containers = walls, all

    # Create Some Starting Values
    global score
    clock = pg.time.Clock()

    # Initialize our starting sprites
    global SCORE
    rat = Rat()
    # note, those  'lives' because it goes into a sprite group
    Cat()
    Cheese()

    # Builds the Wall
    maze_file = os.path.join(main_dir, "src", "gym_rat_runner", "envs", "maze", MAZE_FILE)
    maze = pd.read_csv(maze_file, header= None)

    for i in range(SPACES + 2):
        for j in range(SPACES + 2):
            if maze.iloc[i,j] == 1:
                Wall((i*UNIT_WIDTH, j*UNIT_HEIGHT))
    if pg.font:
        all.add(Score())


    while rat.alive():

        # get input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return

        keystate = pg.key.get_pressed()

        # clear the last drawn sprites
        all.clear(screen, background)

        # update all the sprites
        all.update()

        # handle player input
        vertical_direction = keystate[pg.K_DOWN] - keystate[pg.K_UP]
        horizontal_direction = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
        rat.move(vertical_direction, horizontal_direction)
        if vertical_direction or horizontal_direction:
            SCORE += MOVE_SCORE

        # Detect collisions

        # Wall collisions decreases score and returns the rat to original posistion
        for wall in pg.sprite.spritecollide(rat, walls, False):
            SCORE += WALL_SCORE
            rat.move(-vertical_direction, -horizontal_direction)

        # Cat collision
        for cat in pg.sprite.spritecollide(rat, cats, False):
            SCORE += CAT_SCORE
            rat.kill()

        # Cheese collision
        for cheese in pg.sprite.spritecollide(rat, cheeses, False):
            SCORE += CHEESE_SCORE
            rat.kill()


        #draw the scene
        dirty = all.draw(screen)
        pg.display.update(dirty)

        # Framerate
        clock.tick(10)

    all.clear(screen, background)
    all.update()
    #draw the scene
    dirty = all.draw(screen)
    pg.display.update(dirty)

    pg.time.wait(1000)



    pg.quit()


if __name__ == '__main__':
    main()
