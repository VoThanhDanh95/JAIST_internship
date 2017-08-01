import gym
from gym import wrappers
import numpy as np
import argparse


parser = argparse.ArgumentParser(description='OpenAI - Copy-v0')
parser.add_argument('--eps', metavar='episode', type=int, nargs=1, default=[10000], help='Total number of episodes used to train.')
parser.add_argument('--lr', metavar='learning rate', type=float, nargs=1, default=[0.1], help='Learning rate used when training with Q-Learning or Sarsa.')
parser.add_argument('--dis', metavar='discount value', type=float, nargs=1, default=[0.9], help='Discount value for rewards.')
parser.add_argument('--e', metavar='epsilon', type=float, nargs=1, default=[0.3], help='Epsilon for greedy method.')

args = parser.parse_args()
print(args)
lr = args.lr[0]
epsilon = args.e[0]
discount = args.dis[0]
num_episodes = args.eps[0]
print(lr, epsilon, discount, num_episodes)


env = gym.make('Copy-v0')
s = env.reset()
dim = [u.n for u in env.action_space.spaces]
n_action = np.prod(dim)
actions = list(range(n_action))
print(actions)
q = np.zeros((env.observation_space.n, n_action))
def decode(a, dims):
    res = []
    for d in reversed(dims):
        res.append(a % d)
        a //= d
    res.reverse()
    return res


def q_learning(env):
    reward_list = []
    
    for episode in range(num_episodes):
        done = False
        total_reward = 0
        s = env.reset()
        while True:
            p = np.ones(n_action)*epsilon/n_action
            p[np.argmax(q[s,:])] += 1-epsilon
            a = np.random.choice(a=actions, p=p)
            s_, reward, done, info = env.step(decode(a, dim))
            print('q before get action')
            print(q)
            print('state s',s)
            q[s, a] = q[s, a] + lr*(reward + discount*np.max(q[s_,:])- q[s, a])
            s = s_
            total_reward += reward
            print('reward', reward)
            print('action', a)
            print('state s_',s)
            print('q after get action')
            print(q)
            if episode == num_episodes-1:
                env.render(); # only render the last episode
            if done:
                break

        print("Training  episode %d - Reward %f"%(episode,total_reward))
        #print("end episode-----------------------------------")
        #print("Total reward %d"%total_reward)
        reward_list.append(total_reward)
    print("Average reward (last 100 step): %f"%(np.sum(reward_list[-100:])/100))
    print(q)
    print('q[1,1]', q[1,1])
    return q

def test(q, env):
    rl = []
    for ep in range(1000):
        done = False
        
        total_reward = 0
        s = env.reset()

        while True:
            a = np.argmax(q[s,:])
            s_, reward, done, info = env.step(decode(a, dim))
            s = s_
            total_reward += reward
            # env.render()
            if done:
                break

        rl.append(total_reward)
    print("Test accuracy %f"%(np.sum(rl)/len(rl)))


if __name__ == "__main__":
    global env

    q = q_learning(env)

    # env = wrappers.Monitor(gym.make('Copy-v0'), './copy-v0', force=True)

    test(q, env)
    env.reset()

    
