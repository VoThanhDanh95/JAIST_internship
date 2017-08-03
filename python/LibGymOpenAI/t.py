import gym
import numpy as np
import pandas as pd

env = gym.make('MountainCar-v0')
s = env.reset()
# env.render()

# In[3]
pos_bins = pd.cut([-1.2,0.6],bins=99,retbins=True)[1]
vel_bins = pd.cut([-.07,.07],bins=99,retbins=True)[1]

# print(pos_bins)
# print(np.shape(pos_bins))
# print(vel_bins)
# print(np.shape(vel_bins))


allStates= []
for ii in pos_bins:
    for jj in vel_bins:
      allStates.append(np.array([ii,jj]))

# print(len(allStates))
# print(allStates)
allStates = np.array(allStates)
# print(allStates)
def value_to_state(x):
    global allStates
    global pos_bins
    global vel_bins
    xpos=np.digitize(x[0],pos_bins)
    print('xpos', xpos)
    xvel=np.digitize(x[1],vel_bins)
    print('xvel', xvel)
    stateValue = np.array([pos_bins[xpos],vel_bins[xvel]])
    print('stateValue', stateValue)
    state = np.where((allStates==stateValue).all(axis=1))[0][0]
    print('state', state)
    return state

# In[4] Q Table
Q = np.zeros([len(allStates),
              env.action_space.n])
# print(len(Q))
lr =0.8
y =0.95
num_episodes= 30000
rList = []

# In[4]
for i in range(10):
    s_raw = env.reset()
    # print('s_raw', s_raw)
    s = value_to_state(s_raw)
    # print(s)
    rAll =0
    d = False
    j = 0
    # while j<200:
    #     j+=1
    #     a =np.argmax(Q[s,:]+np.random.randn(1,env.action_space.n)*(1./(i+1)))
    #     s1_raw,r,d,_ = env.step(a)
    #     s1 = value_to_state(s1_raw)
    #     # env.render()
    #     Q[s,a]= Q[s,a]+lr*(r+y*np.max(Q[s1,:])-Q[s,a])
    #     #Q[s,a]= Q[s,a]+r+y*np.max(Q[s1,:])
    #     rAll +=r
    #     s = s1
    #     if d ==True or j==199:
    #         if d== False:
    #             print "Not Episode"
    #         print "Episode " +str(i) +" and Reward " +str(rAll)
    #         rList.append(rAll)
    #         break