#!/usr/bin/env python
# -*- coding: utf-8 -*-

from termcolor import colored
import requests
from random import random, randint
import math


def clamp(minn, x, maxx):
    return max(minn, min(x, maxx))


class State:

    def __init__(self, phi1, theta1, phi2, theta2, phi3, theta3):
        self.energy = -math.inf

        self.angles = [clamp(0, phi1, 359), clamp(0, theta1, 359),
                       clamp(0, phi2, 359), clamp(0, theta2, 359),
                       clamp(0, phi3, 359), clamp(0, theta3, 359)]

    def get_energy(self):
        URL = 'http://localhost:8080/antenna/simulate?'

        URL += 'phi1={}&theta1={}&phi2={}&theta2={}&phi3={}&theta3={}'.format(self.angles[0], self.angles[1],
                                                                              self.angles[2], self.angles[3],
                                                                              self.angles[4], self.angles[5])
        r = requests.post(url=URL)
        self.energy = float(r.text.splitlines()[0])
        return self.energy

    def get_neighbours(self):
        step = 1
        states = [State(self.angles[0] + step, self.angles[1] + step, self.angles[2] + step,
                        self.angles[3] + step, self.angles[4] + step, self.angles[5] + step),
                  State(self.angles[0] - step, self.angles[1] - step, self.angles[2] - step,
                        self.angles[3] - step, self.angles[4] - step, self.angles[5] - step),
                  State(self.angles[0] + step, self.angles[1] - step, self.angles[2] + step,
                        self.angles[3] - step, self.angles[4] + step, self.angles[5] - step),
                  State(self.angles[0] - step, self.angles[1] + step, self.angles[2] - step,
                        self.angles[3] + step, self.angles[4] - step, self.angles[5] + step),
                  State(self.angles[0] + step, self.angles[1] + step, self.angles[2] + step,
                        self.angles[3] - step, self.angles[4] - step, self.angles[5] - step),
                  State(self.angles[0] - step, self.angles[1] - step, self.angles[2] - step,
                        self.angles[3] + step, self.angles[4] + step, self.angles[5] + step)]

        return states

    def get_random(self):
        rand_state = State(randint(0, 360), randint(0, 360), randint(0, 360),
                           randint(0, 360), randint(0, 360), randint(0, 360))
        while rand_state.angles == self.angles:
            rand_state = State(randint(0, 360), randint(0, 360), randint(0, 360),
                               randint(0, 360), randint(0, 360), randint(0, 360))
        return rand_state

    def __str__(self):
        return 'Energy:{}|ϕ1:{},θ1:{},ϕ2:{},θ2:{},ϕ3:{},θ3:{}'.format(colored(self.energy, 'green'),
                                                                      colored(self.angles[0], 'green'),
                                                                      colored(self.angles[1], 'green'),
                                                                      colored(self.angles[2], 'green'),
                                                                      colored(self.angles[3], 'green'),
                                                                      colored(self.angles[4], 'green'),
                                                                      colored(self.angles[5], 'green'))


# TODO: Review the probability p
def replace_neighbours_for_rands(state: State, T):
    output = []
    neighbours = state.get_neighbours()
    for n in neighbours:
        s_rand = state.get_random()
        delta = s_rand.get_energy() - state.get_energy()
        p = math.exp(delta/T)
        r = random()
        if r < p:
            output.append(s_rand)
        else:
            output.append(n)
    return output


def simulate(s0: State, T0, Tf, alfa):
    x = s0
    T = T0
    color = 'white'
    while T > Tf:
        next_states = replace_neighbours_for_rands(x, T)
        for s in next_states:
            delta = s.get_energy() - x.get_energy()
            if delta > 0:
                color = 'green'
                x = s
            print('x: {}, x_l: {}, delta: {}, T: {}'.format(x.energy, colored(s.energy, color), delta, T))
            color = 'white'
        T -= T * alfa
    return x


# ----- TEST -----
s0 = State(randint(0, 360), randint(0, 360), randint(0, 360), randint(0, 360), randint(0, 360), randint(0, 360))
best_antenna = simulate(s0=s0, T0=200, Tf=20, alfa=0.005)
print('Result: {}'.format(str(best_antenna)))

DEV_KEY = 'Equipe da Engenharia'
URL = 'https://aydanomachado.com/mlclass/02_Optimization.php?'

URL += 'phi1={}&theta1={}&phi2={}&theta2={}&phi3={}&theta3={}&dev_key={}'.format(best_antenna.angles[0],
                                                                                 best_antenna.angles[1],
                                                                                 best_antenna.angles[2],
                                                                                 best_antenna.angles[3],
                                                                                 best_antenna.angles[4],
                                                                                 best_antenna.angles[5], DEV_KEY)
r = requests.post(url=URL)
print('Server result: {}'.format(r.text.splitlines()))
