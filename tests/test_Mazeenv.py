import numpy as np
import gym
import gym_rat_runner
from pathlib import Path
import os
from gym.envs.registration import register

env = gym.make('maze-v0')


def test_InitialObservation():
    env.setframepersec(40)
    obs = env.reset()
    env.render()
    assert ((obs['position'] == np.array([5,1], dtype='int32')).all())
    assert ((obs['hunter'] == np.array([2,16], dtype='int32')).all())
    assert ((obs['target'] == np.array([5,32], dtype='int32')).all())

def test_StocObservation():
    env.randomposition()
    for i in range(10):
        obs = env.reset()
        env.render()
    env.randomposition(randompos = False)

def test_changefieldvision():
    env.setfieldvision(range = 10)
    obs = env.reset()
    env.render()
    assert ((obs['position'] == np.array([5,1], dtype='int32')).all())
    assert ((obs['hunter'] == np.array([-1,-1], dtype='int32')).all())
    assert ((obs['target'] == np.array([5,32], dtype='int32')).all())
    env.setfieldvision(range = 40)

def test_move_Right():
    obs = env.reset()
    env.setframepersec(40)
    env.render()
    obs, reward, done, info = env.step(0)
    env.render()
    assert((obs['position'] == np.array([5,2], dtype='int32')).all())
    assert(reward == -1)
    assert(done == False)

def test_move_Up_Right():
    obs = env.reset()
    env.render()
    obs, reward, done, info = env.step(1)
    env.render()
    assert((obs['position'] == np.array([5,2], dtype='int32')).all())
    assert(reward == -1)
    assert(done == False)

def test_move_Up():
    obs = env.reset()
    env.render()
    obs, reward, done, info = env.step(2)
    env.render()
    assert((obs['position'] == np.array([5,1], dtype='int32')).all())
    assert(reward == -1)
    assert(done == False)
    assert(info['wall_colisions'] == 1)

def test_move_Up_Left():
    obs = env.reset()
    env.render()
    obs, reward, done, info = env.step(3)
    env.render()
    assert((obs['position'] == np.array([5,1], dtype='int32')).all())
    assert(reward == -1)
    assert(done == False)
    assert(info['wall_colisions'] == 1)

def test_move_Left():
    obs = env.reset()
    env.render()
    obs, reward, done, info = env.step(4)
    env.render()
    assert((obs['position'] == np.array([5,1], dtype='int32')).all())
    assert(reward == -1)
    assert(done == False)

def test_move_Down_Left():
    obs = env.reset()
    env.render()
    obs, reward, done, info = env.step(5)
    env.render()
    assert((obs['position'] == np.array([5,1], dtype='int32')).all())
    assert(reward == -1)
    assert(done == False)
    assert(info['wall_colisions'] == 1)

def test_move_Down():
    obs = env.reset()
    env.render()
    obs, reward, done, info = env.step(6)
    env.render()
    assert((obs['position'] == np.array([5,1], dtype='int32')).all())
    assert(reward == -1)
    assert(done == False)
    assert(info['wall_colisions'] == 1)

def test_move_Down_Right():
    obs = env.reset()
    env.render()
    obs, reward, done, info = env.step(7)
    env.render()
    assert((obs['position'] == np.array([5,2], dtype='int32')).all())
    assert(reward == -1)
    assert(done == False)
    assert(info['wall_colisions'] == 1)

def test_death():
    obs = env.reset(seed= 123)
    env.render()

    while True:
        obs, reward, done, info = env.step(0)
        env.render()
        if done:
            break
    assert((obs['position'] == obs['hunter']).all())
    assert(reward < -300)
    assert(done == True)

def test_win():
    obs = env.reset(seed=123)
    env.render()
    # 9 moves to Right
    moves = [0]*2 + [6]*2 + [4]*2 + [6]*2 + [4]*4 + [2]*2 + [4]*1 + [2]*2 + [0]*2
    for move in moves:
        obs, reward, done, info = env.step(move)
        env.render()
        if done:
            break

    assert((obs['position'] == obs['target']).all())
    assert(reward == 6)
    assert(done == True)

def test_win_dark():
    env.setfieldvision(range = 5)
    obs = env.reset(seed=123)
    env.render()
    # 9 moves to Right
    moves = [0]*2 + [6]*2 + [4]*2 + [6]*2 + [4]*4 + [2]*2 + [4]*1 + [2]*2 + [0]*2
    for move in moves:
        obs, reward, done, info = env.step(move)
        env.render()
        if done:
            break


    assert((obs['position'] == obs['target']).all())
    assert(reward == 6)
    assert(done == True)

def test_changedeterministic():
    global env
    assert(env.spec.nondeterministic == False)
    env = gym.make('maze-stoc-v0')
    assert(env.spec.nondeterministic == True)

    obs = env.reset(seed=123)
    env.render()

    while True:
        obs, reward, done, info = env.step(0)
        env.render()
        if done:
            break


def main():

    from matplotlib import pyplot as plt
    import cv2 as cv

    env = gym.make('maze-v0')
    obs = env.reset()
    frame = env.render(mode='rgb_array')
    frame_rgb = cv.cvtColor(frame[0], cv.COLOR_BGR2RGB)
    plt.imsave("test.png", arr = frame_rgb)



if __name__ == '__main__':
    main()
