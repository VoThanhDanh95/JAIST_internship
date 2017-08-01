import gym
import numpy as np
from gym import wrappers

EPISODE = 10000
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.5

EPISODE_TEST = 1000

API_KEY = 'sk_nBRdqCHSS3mSmcUbVCb8uQ'

# print(np.argmax(q[o]))
def decode(a, dims):
    res = []
    for d in reversed(dims):
        res.append(a % d)
        a //= d
    res.reverse()
    return res

def QLearning():
    for each_episode in range(EPISODE):
        s = env.reset()
        total_reward = 0

        while True:
            if np.random.random() < EPSILON:
                a = np.random.choice(actions)
            else:
                a = np.argmax(q[s])
            pass
            s_, reward, done, info = env.step(decode(a, dims))
            q[s,a] = q[s,a] + ALPHA*(reward + GAMMA*np.max(q[s_,:]) - q[s,a])
            s = s_
            total_reward = total_reward + reward
            if done:
                break
    pass

def testQLearning():
    result = 0
    for _ in range(EPISODE_TEST):
        s = env.reset()
        while True:
            a = np.argmax(q[s])
            s_, reward, done, info = env.step(decode(a, dims))
            s = s_
            result += reward
            # raw_input('press to continue')
            # env.render()
            if done:
                break
            pass
    return result/EPISODE_TEST

env = gym.make('Copy-v0')
env = wrappers.Monitor(env, './Qlearning_Copy', force=True)
dims = [i.n for i in env.action_space.spaces]
actions = range(np.prod(dims))
states_length = env.observation_space.n

q = np.zeros(shape=(states_length, len(actions)))

QLearning()
print('done training')

average_result = testQLearning()
print("average_result ", average_result, "test count", EPISODE_TEST)
