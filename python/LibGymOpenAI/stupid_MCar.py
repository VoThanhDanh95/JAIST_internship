import gym
import numpy as np


env = gym.make('MountainCar-v0')
EPISODE = 30000
ALPHA = 0.8
GAMMA = 0.9
EPSILON = 0.08
DECIMALS_AROUND = 2

actions = [0,1,2]
q = {}

def getQ(state, action):
    if q.get((state, action)) == None:
        q[state, action] = 0
    else:
        # print('no repeat')
        return q.get((state, action))
    pass


def QLearning():
    for each_episode in range(EPISODE):
        s = env.reset()
        s = tuple([round(x,DECIMALS_AROUND) if isinstance(x, float) else x for x in s])

        [getQ(s, action) for action in actions] #UPDATE Q
        total_reward = 0

        for _ in range(1000):
            if np.random.random() < EPSILON:
                # print('random choice')
                a = np.random.choice(actions)
            else:
                list_score = [getQ(s, action) for action in actions]
                a = np.argmax(list_score)

            s_, reward, done, info = env.step(a)
            
            # print('reward', reward)

            s_ = tuple([round(x,DECIMALS_AROUND) if isinstance(x, float) else x for x in s_])
            [getQ(s_, action) for action in actions]
            list_score_s_ = [getQ(s_, action) for action in actions]
            # print('list_score_s_', list_score_s_)
            # env.render()
            q[s,a] = q[s,a] + ALPHA*(reward + GAMMA*np.max(list_score_s_) - q[s,a])

            s = s_
            total_reward += reward
            if each_episode == (EPISODE-1):
                env.render()
            # if done:
            #     break
        pass
        # print('q')
        print('total reward %d %f'%(each_episode,total_reward))    
    pass

QLearning()
print(q)
# s = env.reset()
# # print(np.around(s, decimals = DECIMALS_AROUND))
# # getQ(tuple(np.around(s,decimals= DECIMALS_AROUND)),0)
# s = tuple([round(x,2) if isinstance(x, float) else x for x in s])
# print s[0]
# # q[, 0] = 0
# print q