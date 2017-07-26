# import gym
# import numpy as np
# from gym.envs.classic_control import rendering
# def repeat_upsample(rgb_array, k=1, l=1, err=[]):
#     # repeat kinda crashes if k/l are zero
#     if k <= 0 or l <= 0: 
#         if not err: 
#             print "Number of repeats must be larger than 0, k: {}, l: {}, returning default array!".format(k, l)
#             err.append('logged')
#         return rgb_array

#     # repeat the pixels k times along the y axis and l times along the x axis
#     # if the input image is of shape (m,n,3), the output image will be of shape (k*m, l*n, 3)

#     return np.repeat(np.repeat(rgb_array, k, axis=0), l, axis=1)

# viewer = rendering.SimpleImageViewer()
# env = gym.make('Freeway-v0')
# env.reset()
# action=0
# for _ in range(1000):
#     rgb = env.render('rgb_array')
#     upscaled=repeat_upsample(rgb,4, 4)
#     viewer.imshow(upscaled)
#     action = env.action_space.sample() # your agent here (this takes random actions)
#     observation, reward, done, info = env.step(action)

    


import gym
import numpy as np
env = gym.make("Freeway-v0")
observation = env.reset()
for _ in range(1000):
  env.render()
  action = env.action_space.sample() # your agent here (this takes random actions)
  observation, reward, done, info = env.step(action)

