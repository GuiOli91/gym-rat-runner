import numpy as np
import gym
import gym_rat_runner

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

    for i in range(3):
        obs, score, end, info = env.step(1)
    for i in range(2):
        obs, score, end, info = env.step(0)
    for i in range(2):
        obs, score, end, info = env.step(2)
    for i in range(4):
        obs, score, end, info = env.step(1)

    assert((obs['distanceTarget'] == np.array([0,0])).all())
    assert(score == (25-11))
    assert(end)

def test_endbysteps():
    env.reset()

    for i in range(200):
        obs, score, end, info = env.step(0)

    assert(score == -200)
    assert(end)

def main():

    env.render()



if __name__ == '__main__':
    main()
