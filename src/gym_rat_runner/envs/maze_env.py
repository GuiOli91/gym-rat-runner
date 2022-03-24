import gym
from gym import error, spaces, utils
from collections import OrderedDict
import pandas as pd
import numpy as np
import  os
import glob

import cv2 as cv

#Environment rewards

MOVE_REWARD = -1
HUNTER_REWARD = -300
TARGET_REWARD = 25

#Screen constants

UNIT = 60                           # Units for the renderization
DARK_GREEN = (21, 89, 33)           # Background color
MAZE_FILE = "Maze1.csv"             # Maze file for the renderization

#Text parameters

font                    = cv.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText  = None # Will be updated based on maze's size.
fontScale               = 0.5
fontColor               = (255,255,255)
thickness               = 2
lineType                = 2

main_dir = os.path.abspath(os.path.join(os.path.split(os.path.abspath(__file__))[0], os.pardir))

class MazeEnv(gym.Env):
    """docstring for MazeEnv."""

    class AnimatedObject():
        """
        Internal object to support interactive objects in the environment.
        """

        def __init__(self, pos = None):
            if not pos:
                # NOTE: This part need to be updated based on the maze
                self.x = np.random.randint(0,10)
                self.y = np.random.randint(0,10)
            else:
                self.x = pos[0]
                self.y = pos[1]

        def __str__(self):
            return f"{self.x}, {self.y}"

        def __sub__(self, other):
            return np.array([self.x-other.x, self.y-other.y], np.int32)

        def move(self, x, y):
            self.x += x
            self.y += y

        def action(self, arg):
            """
            Gives the AnimatedObject the option to move in 8 directions.
            """

            actions = {
            0: (1,0),
            1: (1,1),
            2: (0,1),
            3: (-1,1),
            4: (-1,0),
            5: (-1,-1),
            6: (0,-1),
            7: (1,-1)
            }

            x, y = actions.get(choice)
            self.move(x,y)

        def newpos(self, x, y):
            self.x = x
            self.y = y

    metadata = {'render.modes': ['human', 'video', 'rgb_array']}

    def __init__(self):
        super(MazeEnv, self).__init__()

        #Load Maze
        maze_file = os.path.join(main_dir, 'envs', 'maze', MAZE_FILE)
        self.maze = pd.read_csv(maze_file, header = None)

        # Updates based on the Maze
        bottomLeftCornerOfText = (10, self.maze.shape[0]*UNIT - UNIT//2)

        #Load Images
        pathimages = os.path.join(main_dir, 'images', '*.png')

        self.images = {}
        for file in glob.glob(pathimages):
            figname = os.path.split(file)[1][:-4]
            self.images[figname] = cv.imread(file, cv.IMREAD_UNCHANGED)
            self.images[figname] = cv.resize(self.images[figname], (UNIT, UNIT), interpolation = cv.INTER_AREA)

        self.frames = []

        # Animated Objects for the environment
        self.target = None
        self.player = None
        self.hunter = None

        # Set rewards for the game

        self.movereward = MOVE_REWARD
        self.huntereward = HUNTER_REWARD
        self.targetreward = TARGET_REWARD

        self.action = None
        self.reward = 0
        self.done = False
        self.info = {}
        self.action_space = spaces.Discrete(8)

        # The player is able to observer:
        #  - The cartesian position of himself.
        #  - The maze within the observable distance. TO BE ADDED
        self.observation_space = spaces.Dict({
        "position": spaces.Box(low=np.array([0,0]), high=np.array(self.maze.shape), dtype=np.int32)
        })
        self.deterministic = True

    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.

        Accepts an action and returns a tuple (observation, reward, done, info).

        Args:
            action (object): an action provided by the agent

        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """

        pass

    def reset(self, arg):
        """Resets the environment to an initial state and returns an initial
        observation.

        Note that this function should not reset the environment's random
        number generator(s); random variables in the environment's state should
        be sampled independently between multiple calls to `reset()`. In other
        words, each call of `reset()` should yield an environment suitable for
        a new episode, independent of previous episodes.

        Returns:
          observation (object): the initial observation.
        """

        self.done = False
        self.reward = 0

        # REVIEW: Save the info?

        self.info = {}

        if not self.deterministic:
            # NOTE: Proabably will need to be redone
            self.target = self.AnimatedObject()
            self.player = self.AnimatedObject()
            self.hunter = self.AnimatedObject()
        else:
            self.target = self.AnimatedObject([11,33])
            self.player = self.AnimatedObject([11,0])
            self.hunter = self.AnimatedObject([4,15])

            # COMBAK: 20220324
        pass

    def render(self, mode='human', videofile=None):
        """Renders the environment.

        The set of supported modes varies per environment. (And some
        environments do not support rendering at all.) By convention,
        if mode is:

        - human: render to the current display or terminal and
        return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
        representing RGB values for an x-by-y pixel image, suitable
        for turning into a video.
        - ansi: Return a string (str) or StringIO.StringIO containing a
        terminal-style text representation. The text can include newlines
        and ANSI escape sequences (e.g. for colors).
        - video: Return a mov file unsing the Apple's version of the MPEG4 part 10/H.264 through the openvc library

        Note:
          Make sure that your class's metadata 'render.modes' key includes
            the list of supported modes. It's recommended to call super()
            in implementations to use the functionality of this method.

        Args:
          mode (str): the mode to render with

        Example:

        class MyEnv(Env):
          metadata = {'render.modes': ['human', 'rgb_array']}

          def render(self, mode='human'):
              if mode == 'rgb_array':
                  return np.array(...) # return RGB frame suitable for video
              elif mode == 'human':
                  ... # pop up a window and render
              else:
                  super(MyEnv, self).render(mode=mode) # just raise an exception
        """
        if mode == 'human':
            pass

        elif mode == 'rgb_array':
            pass

        elif mode == 'video':
            pass

        else:
            super(MazeEnv, self).render(mode=mode)

    def close(self):
        """Override close in your subclass to perform any necessary cleanup.

        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        pass

    def setrewards(self, movereward = MOVE_REWARD,
                    targetreward = TARGET_REWARD, huntereward = HUNTER_REWARD):

        """Change the rewards values in the environment.
        """
        self.movereward = movereward
        self.targetreward = targetreward
        self.huntereward = huntereward
