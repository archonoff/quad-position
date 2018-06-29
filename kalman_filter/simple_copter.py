from math import sin, cos
import numpy as np


class SimpleCopter:
    t = 0
    dt = 0.01
    alpha_x = 0
    omega_z = 0
    a_x = 0
    a_y = 0
    a_z = 0
    alpha_func = None
    omega_func = None

    measure_noise = 2

    def __init__(self):
        self.alpha_func = lambda t: 30 * sin(t)
        self.omega_func = lambda t: 30 * cos(t)
        # self.alpha_func = lambda t: 0
        # self.omega_func = lambda t: 0

    def step(self):
        self.t += self.dt
        self.alpha_x = self.alpha_func(self.t)
        self.omega_z = self.omega_func(self.t)
        self.a_x = ''
        self.a_y = ''

    def sense(self):
        noise_alpha_x = np.random.normal(0, self.measure_noise)
        noise_omega_z = np.random.normal(0, self.measure_noise)
        return self.alpha_x + noise_alpha_x, self.omega_z + noise_omega_z
