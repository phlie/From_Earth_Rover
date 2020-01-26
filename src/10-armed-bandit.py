import random


total_steps = 1000

bandits_probability = []


def setup_bandits():

    for bandits in range(10):
        lower = random.randint(-5, 5)
        upper = random.randint(lower + 1,lower + 5)
        bandits_probability.append([lower, upper])

    print(bandits_probability)
    return bandits_probability

def bet_on_bandit(index):
    reward = random.randint(bandits_probability[index][0], bandits_probability[index][1])
    return reward

setup_bandits()

for x in range(25):
    print(bet_on_bandit(0))

def a_bandit_run():
    total_reward = 0
    Q = [0.0 for _ in range(10)]
    N = [0.0 for _ in range(10)]
    for steps in range(total_steps):
        e = random.randint(0, 9)
        if e <= 1:
            action_to_choose = random.randint(0,9)
        else:
            action_to_choose = Q.index(max(Q))

        reward = bet_on_bandit(action_to_choose)
        N[action_to_choose] += 1
        Q[action_to_choose] = Q[action_to_choose] + (reward - Q[action_to_choose]) / N[action_to_choose]
        total_reward += reward
    return total_reward, Q

runs_reward = 0
for runs in range(50):
    r, q = a_bandit_run()
    runs_reward += r
    print("Value: ", q)
    print("Total Reward: ", r)

print("The total reward is: ", runs_reward)
print("The average reward is: ", runs_reward / 100)
