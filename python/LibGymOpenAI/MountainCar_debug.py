import gym
import numpy as np
import pandas as pd


env = gym.make('MountainCar-v0')
EPISODE = 30000
ALPHA = 0.8
GAMMA = 0.9
EPSILON = 0.1
DECIMALS_AROUND = 2

actions = [0,1,2]
q = {}

pos_bins = pd.cut([-1.2,0.6],bins=99,retbins=True)[1]
vel_bins = pd.cut([-.07,.07],bins=99,retbins=True)[1]

allStates= []
for ii in pos_bins:
    for jj in vel_bins:
      allStates.append(np.array([ii,jj]))
allStates = np.array(allStates)

def value_to_state(x):
    global allStates
    global pos_bins
    global vel_bins
    xpos=np.digitize(x[0],pos_bins)
    xvel=np.digitize(x[1],vel_bins)
    stateValue = np.array([pos_bins[xpos],vel_bins[xvel]])
    state = np.where((allStates==stateValue).all(axis=1))[0][0]
    return state

Q = np.zeros([len(allStates),
              env.action_space.n])
lr =0.8
y =0.95
num_episodes= 30000
rList = []

# for i in range(num_episodes):
#     s_raw = env.reset()
#     s = value_to_state(s_raw)
#     rAll =0
#     d = False
#     j = 0
#     while j<200:
#         j+=1
#         a =np.argmax(Q[s,:]+np.random.randn(1,env.action_space.n)*(1./(i+1)))
#         s1_raw,r,d,_ = env.step(a)
#         s1 = value_to_state(s1_raw)
#         # env.render()
#         Q[s,a]= Q[s,a]+lr*(r+y*np.max(Q[s1,:])-Q[s,a])
#         #Q[s,a]= Q[s,a]+r+y*np.max(Q[s1,:])
#         rAll +=r
#         s = s1
#         if d ==True or j==199:
#             if d== False:
#                 print "Not Episode"
#             print "Episode " +str(i) +" and Reward " +str(rAll)
#             rList.append(rAll)
#             break


def QLearning():
    for i in range(EPISODE):
        s = env.reset()
        s = value_to_state(s)
        total_reward = 0
        for _ in range(10000):
            if np.random.random() < EPSILON:
                a = np.random.choice(actions)
            else:
                a = np.argmax(Q[s,:])
            # a = np.argmax(Q[s,:]+np.random.randn(1,env.action_space.n)*(1./(i+1)))


            s_, reward, done, info = env.step(a)
            
            s_ = value_to_state(s_)            
            # print('reward', reward)

            # s_ = tuple([round(x,DECIMALS_AROUND) if isinstance(x, float) else x for x in s_])
            # [getQ(s_, action) for action in actions]
            # list_score_s_ = [getQ(s_, action) for action in actions]
            # print('list_score_s_', list_score_s_)
            # env.render()
            # Q[s,a] = Q[s,a] + ALPHA*(reward + GAMMA*np.max(Q[s_,:]) - Q[s,a])
            Q[s,a]= Q[s,a]+lr*(reward+y*np.max(Q[s_,:])-Q[s,a])

            s = s_
            total_reward += reward
            if i == (EPISODE-1):
                env.render()
            if done:
                break
        # print('q')
        # print('--------------------------------------------')
        # print('--------------------------------------------')
        # print('--------------------------------------------')
        # print(len(q))
        # print('--------------------------------------------')
        # print('--------------------------------------------')
        # print('--------------------------------------------')

        print('total reward %d %f'%(i,total_reward))    
    pass

QLearning()
# print(q)
# s = env.reset()
# # print(np.around(s, decimals = DECIMALS_AROUND))
# # getQ(tuple(np.around(s,decimals= DECIMALS_AROUND)),0)
# s = tuple([round(x,2) if isinstance(x, float) else x for x in s])
# print s[0]
# # q[, 0] = 0
# print q