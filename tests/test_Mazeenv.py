import numpy as np
import gym
import gym_rat_runner
from pathlib import Path
import os

env = gym.make('maze-v0')


def test_InitialObservation():
    obs = env.reset()
    env.render()
    assert ((obs['position'] == np.array([0,13], dtype='int32')).all())
    assert ((obs['hunter'] == np.array([16,16], dtype='int32')).all())
    assert ((obs['target'] == np.array([33,13], dtype='int32')).all())

def test_changefieldvision():
    env.setfieldvision(range = 8)
    env.reset()
    assert ((obs['position'] == np.array([0,13], dtype='int32')).all())
    assert ((obs['hunter'] == np.array([np.nan,np.nan], dtype='int32')).all())
    assert ((obs['target'] == np.array([33,13], dtype='int32')).all())
    env.setfieldvision(range = 40)

# def test_move0():
#     env.reset()
#     env.step(0)
#     assert(env.player.x == 1 and env.player.y == 13)
#
# def test_move1():
#     env.reset()
#     env.step(1)
#     assert(env.player.x == 1 and env.player.y == 14)
#
# def test_move2():
#     env.reset()
#     env.step(2)
#     assert(env.player.x == 0 and env.player.y == 14)
#
# def test_move3():
#     env.reset()
#     env.step(3)
#     assert(env.player.x == 0 and env.player.y == 1)
#
# def test_move4():
#     env.reset()
#     env.step(4)
#     assert(env.player.x == 0 and env.player.y == 0)
#
# def test_move5():
#     env.reset()
#     env.step(5)
#     assert(env.player.x == 0 and env.player.y == 0)
#
# def test_move6():
#     env.reset()
#     env.step(6)
#     assert(env.player.x == 0 and env.player.y == 0)
#
# def test_move7():
#     env.reset()
#     env.step(7)
#     assert(env.player.x == 1 and env.player.y == 0)


def main():
    pass


if __name__ == '__main__':
    main()
