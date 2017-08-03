import numpy as np
import gym
from gym import wrappers

BINS_X = 130
BINS_VELO = 100
N_LAST_EPISODE = 100
EPISODE = 100000     #training numbers
ALPHA = 0.2         #learning rate
GAMMA = 0.9         #discount reward    
EPSILON = 0.1       #exploration chance

EPISODE_TEST=1000
env=gym.make('MountainCar-v0')


high = env.observation_space.high
low = env.observation_space.low
# x_range = np.array([low[0], high[0]])
# velo_range = np.array([low[1], high[1]])
x_bins = np.linspace(low[0], high[0], num=BINS_X)
velo_bins = np.linspace(low[1], high[1], num=BINS_VELO)

actions = [0,1,2]

q = np.zeros(shape=(BINS_X*BINS_VELO, len(actions)))
# print(np.shape(q))

def state_to_position(s):
    x_inds = np.digitize(s[0], x_bins)
    velo_inds = np.digitize(s[1], velo_bins)    
    return (x_inds-1)*BINS_VELO + (velo_inds-1)

def QLearning():
    average_reward = []
    for i in range(EPISODE):
        s = env.reset()
        s = state_to_position(s)
        total_reward = 0
        for _ in range(1000):
            if np.random.random() < EPSILON:
                # print('random choice')
                a = np.random.choice(actions)
            else:
                a = np.argmax(q[s,:])

            s_, reward, done, info = env.step(a)
            s_ = state_to_position(s_)

            q[s,a] = q[s,a] + ALPHA*(reward + GAMMA*max(q[s_,:]) - q[s,a])

            s = s_
            total_reward += reward


            if done:
                break
        pass
        if EPISODE-i<=N_LAST_EPISODE:
            average_reward.append(total_reward)
        print('total reward %d %f'%(i,total_reward))    
    return sum(average_reward)/len(average_reward)

def QlearningTest():
    average_reward_test = []
    for i in range(EPISODE_TEST):
        s = env.reset()
        s = state_to_position(s)
        total_reward = 0
        while True:
            a = np.argmax(q[s,:])

            s_, reward, done, info = env.step(a)
            s_ = state_to_position(s_)
            s = s_
            total_reward += reward

            if done:
                break
            pass
        if EPISODE_TEST-i<=N_LAST_EPISODE:
            average_reward_test.append(total_reward)
    return sum(average_reward_test)/len(average_reward_test)


# env = wrappers.Monitor(env, './Qlearning_Copy', force=True)

training_result = QLearning()
print('average training_result ', training_result)
test_result = QlearningTest()
print('average test_result', test_result)