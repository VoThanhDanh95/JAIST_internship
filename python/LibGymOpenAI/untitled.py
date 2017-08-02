import numpy as np
import gym
BINS = 100
N_LAST_EPISODE = 100
EPISODE = 50000
ALPHA = 0.2
GAMMA = 0.9
EPSILON = 0.1
env=gym.make('MountainCar-v0')


high = env.observation_space.high
low = env.observation_space.low
# x_range = np.array([low[0], high[0]])
# velo_range = np.array([low[1], high[1]])
x_bins = np.linspace(low[0], high[0], num=BINS)
velo_bins = np.linspace(low[1], high[1], num=BINS)

actions = [0,1,2]

q = np.zeros(shape=(BINS**2, len(actions)))
# print(np.shape(q))

def state_to_position(s):
    x_inds = np.digitize(s[0], x_bins)
    velo_inds = np.digitize(s[1], velo_bins)    
    return (x_inds-1)*BINS + (velo_inds-1)

def QLearning():
    average_reward = 0
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
            average_reward += total_reward
        print('total reward %d %f'%(i,total_reward))    
    return average_reward/N_LAST_EPISODE

result = QLearning()
print('average result ', result)