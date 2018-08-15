from prettytable import PrettyTable
import requests
from random import random, randint
import math


def clamp(minn, x, maxx):
    return max(minn, min(x, maxx))


class State:

    def __init__(self, phi1, theta1, phi2, theta2, phi3, theta3):
        self.phi1 = clamp(0, phi1, 359)
        self.theta1 = clamp(0, theta1, 359)
        self.phi2 = clamp(0, phi2, 359)
        self.theta2 = clamp(0, theta2, 359)
        self.phi3 = clamp(0, phi3, 359)
        self.theta3 = clamp(0, theta3, 359)
        self.energy = -math.inf

        self.list = [self.phi1, self.theta1, self.phi2, self.theta2, self.phi3, self.theta3]

    def get_energy(self):
        URL = 'http://localhost:8080/antenna/simulate?'

        URL += 'phi1={}&theta1={}&phi2={}&theta2={}&phi3={}&theta3={}'.format(self.list[0], self.list[1], self.list[2],
                                                                              self.list[3], self.list[4], self.list[5])
        r = requests.post(url=URL)
        self.energy = float(r.text.splitlines()[0])
        return self.energy

    def get_neighbour(self):
        new_state = State(randint(self.list[0] - 90, self.list[0] + 90),
                          randint(self.list[1] - 90, self.list[1] + 90),
                          randint(self.list[2] - 90, self.list[2] + 90),
                          randint(self.list[3] - 90, self.list[3] + 90),
                          randint(self.list[4] - 90, self.list[4] + 90),
                          randint(self.list[5] - 90, self.list[5] + 90))
        return new_state

    def __str__(self):
        return '{}|{},{},{},{},{},{}'.format(self.energy, self.list[0], self.list[1], self.list[2], self.list[3],
                                             self.list[4], self.list[5])


def simulate(s0: State, T0, Tf, alfa):
    x = s0
    T = T0
    while T > Tf:
        print(T)
        x_linha = x.get_neighbour()
        delta = x_linha.get_energy() - x.get_energy()
        if delta > 0:
            x = x_linha
        else:
            r = random()
            p = math.exp(-abs(delta)/T)
            print('x: {}, x_l: {}, delta: {}, T: {}, p: {}'.format(x.energy, x_linha.energy, -delta, T, p))
            if r < p:
                print('R: {}'.format(r))
                x = x_linha
        T = T * alfa
    return x


# ----- TEST -----
s0 = State(randint(0, 360), randint(0, 360), randint(0, 360), randint(0, 360), randint(0, 360), randint(0, 360))
# for x in range(0, 10):
print('Result: {}'.format(str(simulate(s0=s0, T0=999999, Tf=1, alfa=0.9999))))
