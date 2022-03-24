import numpy as np
import gym
import gym_rat_runner
from pathlib import Path
import os

env = gym.make('maze-v0')
pos = env.reset()

def test_simplerender():
    env.render()
