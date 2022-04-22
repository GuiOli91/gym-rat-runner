import numpy as np
import gym
import gym_rat_runner
from pathlib import Path
import os

env = gym.make('open-v0')
pos = env.reset()

def test_playerInitialpos():
    assert(env.player.x == 0 and env.player.y == 0)

def test_distanceEnemy():
    assert((pos['distanceEnemy'] == np.array([4,4])).all())

def test_distanceTarget():
    assert((pos['distanceTarget'] == np.array([9,9])).all())

def test_move0():
    env.step(0)
    assert(env.player.x == 1 and env.player.y == 0)

def test_move1():
    env.reset()
    env.step(1)
    assert(env.player.x == 1 and env.player.y == 1)

def test_move2():
    env.reset()
    env.step(2)
    assert(env.player.x == 0 and env.player.y == 1)

def test_move3():
    env.reset()
    env.step(3)
    assert(env.player.x == 0 and env.player.y == 1)

def test_move4():
    env.reset()
    env.step(4)
    assert(env.player.x == 0 and env.player.y == 0)

def test_move5():
    env.reset()
    env.step(5)
    assert(env.player.x == 0 and env.player.y == 0)

def test_move6():
    env.reset()
    env.step(6)
    assert(env.player.x == 0 and env.player.y == 0)

def test_move7():
    env.reset()
    env.step(7)
    assert(env.player.x == 1 and env.player.y == 0)

def test_death():

    env.reset()

    for i in range(4):
        obs, score, end, info = env.step(1)
    assert((obs['distanceEnemy'] == np.array([0,0])).all())
    assert(score == -304)
    assert(end)

def test_won():
    env.reset()
    home = str(Path.home())
    videopath=os.path.join(home, 'Videos', 'rat_runner_Openenv')
    if not Path(videopath).is_dir():
        os.mkdir(videopath)
    videopath = os.path.join(videopath, 'testwon.mov')
    for i in range(3):
        env.render(mode='video', videofile=videopath)
        obs, score, end, info = env.step(1)
    for i in range(2):
        env.render(mode='video', videofile=videopath)
        obs, score, end, info = env.step(0)
    for i in range(2):
        env.render(mode='video', videofile=videopath)
        obs, score, end, info = env.step(2)
    for i in range(4):
        env.render(mode='video', videofile=videopath)
        obs, score, end, info = env.step(1)
    env.render(mode='video', videofile=videopath)

    assert((obs['distanceTarget'] == np.array([0,0])).all())
    assert(score == (25-11))
    assert(end)

def test_newreward_won():

    env.reset()
    home = str(Path.home())
    videopath=os.path.join(home, 'Videos', 'rat_runner_Openenv')
    if not Path(videopath).is_dir():
        os.mkdir(videopath)
    videopath = os.path.join(videopath, 'newtestwon.mov')
    env.setrewards(targetreward=1000)
    for i in range(3):
        env.render(mode='video', videofile=videopath)
        obs, score, end, info = env.step(1)
    for i in range(2):
        env.render(mode='video', videofile=videopath)
        obs, score, end, info = env.step(0)
    for i in range(2):
        env.render(mode='video', videofile=videopath)
        obs, score, end, info = env.step(2)
    for i in range(4):
        env.render(mode='video', videofile=videopath)
        obs, score, end, info = env.step(1)
    env.render(mode='video', videofile=videopath)

    assert((obs['distanceTarget'] == np.array([0,0])).all())
    assert(score == (1000-11))
    assert(end)


def test_endbysteps():
    env.reset()

    for i in range(200):
        env.render()
        obs, score, end, info = env.step(0)
    env.render()
    assert(score == -200)
    assert(end)

def main():

    from matplotlib import pyplot as plt
    import cv2 as cv

    env = gym.make('open-v0')
    obs = env.reset()
    frame = env.render(mode='rgb_array')
    frame_rgb = cv.cvtColor(frame[0], cv.COLOR_BGR2RGB)
    plt.imsave("Open_Environment.png", arr = frame_rgb)




if __name__ == '__main__':
    main()
