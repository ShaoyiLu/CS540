import gym
import random
import numpy as np
import time
from collections import deque
import pickle

from collections import defaultdict

EPISODES = 20000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999


def default_Q_value():
    return 0


if __name__ == "__main__":

    random.seed(1)
    np.random.seed(1)
    env = gym.envs.make("FrozenLake-v1")
    env.seed(1)
    env.action_space.np_random.seed(1)

    Q_table = defaultdict(default_Q_value)  # starts with a pessimistic estimate of zero reward for each state.
    episode_reward_record = deque(maxlen=100)

    for i in range(EPISODES):
        episode_reward = 0
        done = False
        obs = env.reset()

        #Q-Learning
        while (not done):
            if random.uniform(0, 1) > EPSILON:
                exception = np.array([Q_table[(obs, i)] for i in range(env.action_space.n)])
                activity = np.argmax(exception)
            else:
                activity = env.action_space.sample()

            next_state, award, done, info = env.step(activity)
            next_exception = np.array([Q_table[(next_state, j)] for j in range(env.action_space.n)])
            cost = np.amax(next_exception)

            if not done:
                Q_table[(obs, activity)] = Q_table[(obs, activity)] * (1 - LEARNING_RATE) + (award + cost * DISCOUNT_FACTOR) * LEARNING_RATE
            else:
                Q_table[(obs, activity)] = Q_table[(obs, activity)] * (1 - LEARNING_RATE) + award * LEARNING_RATE

            obs = next_state
            episode_reward += award

        EPSILON = EPSILON * EPSILON_DECAY

        # record the reward for this episode
        episode_reward_record.append(episode_reward)

        if i % 100 == 0 and i > 0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record)) / 100))
            print("EPSILON: " + str(EPSILON))

    model_file = open('Q_TABLE.pkl', 'wb')
    pickle.dump([Q_table, EPSILON], model_file)
    model_file.close()
