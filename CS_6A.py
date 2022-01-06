import numpy as np
import random as rnd


class Genetic:
    def __init__(self, hardness: np.ndarray, times: np.ndarray, powers: np.ndarray, division: np.ndarray,
                 t: int, w: int):
        self.hardness = hardness
        self.times = times
        self.powers = powers
        self.division = division
        self.t = t
        self.w = w
        self.best_time = self.summary_time(self.division)
        self.best_division = division

    def summary_time(self, division):
        max_time = 0
        for worker in range(w):
            time = 0
            for i in range(self.t):
                if worker == division[i] - 1:
                    time += self.times[i] * self.powers[worker][self.hardness[i] - 1]
            if time > max_time:
                max_time = time
        return max_time

    def hard_mutation(self):
        local_best_time = self.best_time
        for k in range(1200):
            new_division = self.division.copy()
            for i in range(t):
                new_division[i] += rnd.randint(-new_division[i]+1, w-new_division[i])

            new_time = self.summary_time(new_division)
            if new_time < local_best_time:
                local_best_time = new_time
                self.best_division = new_division.copy()

    def soft_mutation(self, d: int):
        local_best_time = self.best_time
        for k in range(1200):
            new_division = self.division.copy()
            for j in range(self.t//d):
                i = rnd.randint(0, self.t-1)
                new_division[i] += rnd.randint(-new_division[i]+1, w-new_division[i])

            new_time = self.summary_time(new_division)
            if new_time < local_best_time:
                local_best_time = new_time
                self.best_division = new_division.copy()

    def crossing(self):
        if self.best_time > 700:
            self.hard_mutation()
        elif self.best_time > 625:
            self.soft_mutation(5)
        elif self.best_time > 613:
            self.soft_mutation(50)
        else:
            self.soft_mutation(500)

        swipe_first = rnd.randint(0, t//2)
        parent_length = rnd.randint(t//4, t//2)
        self.division = np.concatenate((self.best_division[:swipe_first], self.division[swipe_first:swipe_first+parent_length],
                                        self.best_division[swipe_first+parent_length:]), axis=0)

        new_time = self.summary_time(self.division)
        if new_time < self.best_time:
            self.best_time = new_time

    def get_division(self):
        return self.division

    def get_time(self):
        return self.best_time


t = int(input())
hardness = [int(i) for i in input().split()]
times = [float(i) for i in input().split()]
w = int(input())
powers = []
for j in range(w):
    powers.append([float(i) for i in input().split()])

g = Genetic(hardness=hardness, times=times, powers=powers, division=np.ones(t, dtype=int)*6, t=t, w=w)
for i in range(200):
    g.crossing()
    print(g.get_division(), g.get_time(), i)

res = g.get_division()
s = ""
for i in res:
    s += str(i)+" "
print(s[:-1])
