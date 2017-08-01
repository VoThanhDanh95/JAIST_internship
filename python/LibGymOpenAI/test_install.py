import gym
env = gym.make('Copy-v0')
for i_episode in range(20):
    observation = env.reset()
    for t in range(10):
        env.render()
        print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        print('observation', observation)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break