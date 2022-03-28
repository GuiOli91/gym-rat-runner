import numpy as np
import gym
import gym_rat_runner
from pathlib import Path
import os

env = gym.make('maze-v0')


def test_InitialObservation():
    env.setframepersec(2)
    obs = env.reset()
    env.render()
    assert ((obs['position'] == np.array([5,1], dtype='int32')).all())
    assert ((obs['hunter'] == np.array([2,16], dtype='int32')).all())
    assert ((obs['target'] == np.array([5,32], dtype='int32')).all())

def test_changefieldvision():
    env.setfieldvision(range = 8)
    obs = env.reset()
    env.render()
    assert ((obs['position'] == np.array([5,1], dtype='int32')).all())
    assert ((obs['hunter'] == np.array([-1,-1], dtype='int32')).all())
    assert ((obs['target'] == np.array([5,32], dtype='int32')).all())
    env.setfieldvision(range = 40)

def test_move_Right():
    obs = env.reset()
    env.setframepersec(20)
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
    obs = env.reset()
    env.render()
    # 9 moves to Right
    for i in range(9):
        obs, reward, done, info = env.step(0)
        env.render()
    # 3 moves to Up
    for i in range(2):
        obs, reward, done, info = env.step(2)
        env.render()
    for i in range(6):
        obs, reward, done, info = env.step(0)
        env.render()
    obs, reward, done, info = env.step(2)
    env.render()
    assert((obs['position'] == obs['hunter']).all())
    assert(reward == -318)
    assert(done == False)

def test_win():
    obs = env.reset()
    env.render()
    # 9 moves to Right
    for i in range(9):
        obs, reward, done, info = env.step(0)
        env.render()
    # 3 moves to Up
    for i in range(2):
        obs, reward, done, info = env.step(2)
        env.render()
    for i in range(14):
        obs, reward, done, info = env.step(0)
        env.render()
    for i in range(2):
        obs, reward, done, info = env.step(6)
        env.render()
    for i in range(9):
        obs, reward, done, info = env.step(0)
        env.render()
    env.render()
    assert((obs['position'] == obs['target']).all())
    assert(reward == 14)
    assert(done == True)

def test_win_dark():
    env.setfieldvision(range = 5)
    obs = env.reset()
    env.render()
    # 9 moves to Right
    for i in range(9):
        obs, reward, done, info = env.step(0)
        env.render()
    # 3 moves to Up
    for i in range(2):
        obs, reward, done, info = env.step(2)
        env.render()
    for i in range(14):
        obs, reward, done, info = env.step(0)
        env.render()
    for i in range(2):
        obs, reward, done, info = env.step(6)
        env.render()
    for i in range(9):
        obs, reward, done, info = env.step(0)
        env.render()
    env.render()
    assert((obs['position'] == obs['target']).all())
    assert(reward == 14)
    assert(done == True)


def main():
    pass


if __name__ == '__main__':
    main()
