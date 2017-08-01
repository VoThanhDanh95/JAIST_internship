import argparse
import numpy as np
from collections import defaultdict
import gym
from gym import wrappers
import pdb

EXP_NAME_PREFIX = 'exp/q_learning'
API_KEY = 'sk_ARsYZ2eRsGoeANVhUgrQ'
ENVS = {
    'copy': 'Copy-v0', # --alpha 0.3 --gamma 0.9 --eps 0.2 --eps_schedule 200 --goal 25 --env copy
    'frozenlake': 'FrozenLake-v0',
    'duplicatedinput': 'DuplicatedInput-v0',
}


def decode(a, dims):
    if len(dims) == 1:
        return a
    res = []
    for d in reversed(dims):
        res.append(a % d)
        a /= d
    res.reverse()
    return res


def q_learning(env, max_episodes, alpha, gamma, eps, eps_schedule, goal):
    if hasattr(env.action_space, 'spaces'):
        dims = [d.n for d in env.action_space.spaces]
    else:
        dims = [env.action_space.n]
    nA = np.prod(dims)
    nS = env.observation_space.n

    Q = np.zeros((nS, nA), np.float32)
    P = np.zeros(nA, np.float32)

    def exec_policy(s):
        P.fill(eps / nA)
        P[np.argmax(Q[s])] += 1 - eps
        return np.random.choice(xrange(nA), p=P)

    tR = np.zeros(100, np.float32)
    for e in xrange(max_episodes):
        if e % 50 == 0 and e > 0:
            print 'episode %d, average reward: %.3f' % (e, np.mean(tR))
            if np.mean(tR) > goal:
                return e
        if e % eps_schedule == 0 and e > 0:
            eps /= 2

        s = env.reset()
        done = False
        tR[e % tR.size] = 0.
        while not done:
            a = exec_policy(s)
            ns, r, done, _ = env.step(decode(a, dims))
            Q[s][a] += alpha * ((r + gamma * np.max(Q[ns])) - Q[s][a])
            s = ns
            tR[e % tR.size] += r
    return max_episodes


def main():
    parser = argparse.ArgumentParser(description='Q-learning')
    parser.add_argument('--env', choices=ENVS.keys())
    parser.add_argument('--max_episodes', type=int, default=10000)
    parser.add_argument('--alpha', type=float, default=1.0)
    parser.add_argument('--gamma', type=float, default=1.0)
    parser.add_argument('--eps', type=float, default=0.1)
    parser.add_argument('--eps_schedule', type=int, default=10000)
    parser.add_argument('--goal', type=float, default=1.0)
    parser.add_argument('--upload', action='store_true', default=False)
    args = parser.parse_args()

    exp_name = '%s_%s' % (EXP_NAME_PREFIX, args.env)

    env = gym.make('Copy-v0')
    env.seed(0)
    np.random.seed(0)
    if args.upload:
        env = wrappers.Monitor(env, exp_name, force=True)

    res = q_learning(env, args.max_episodes, args.alpha,
            args.gamma, args.eps, args.eps_schedule, args.goal)
    print 'result -> %d' % res

    env.close()
    if args.upload:
        gym.upload(exp_name, api_key=API_KEY)


if __name__ == '__main__':
    main()