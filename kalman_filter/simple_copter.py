from math import sin, cos, atan2, pi
import numpy as np


class SimpleCopter:
    t = 0
    dt = 0.01
    alpha_x = 0
    omega_z = 0
    a_x = 0
    a_y = 0
    alpha_func = None
    omega_func = None

    measure_omega_noise = 0.08
    measure_a_noise = 0.1

    def __init__(self):
        self.alpha_func = lambda t: sin(t)
        self.omega_func = lambda t: cos(t)

    def step(self):
        self.t += self.dt
        self.a_x = sin(self.alpha_x)
        self.a_y = cos(self.alpha_x)
        self.alpha_x = self.alpha_func(self.t)
        self.omega_z = self.omega_func(self.t)

    def sense(self):
        noise_omega_z = np.random.normal(0, self.measure_omega_noise)
        noise_ax = np.random.normal(0, self.measure_a_noise)
        noise_ay = np.random.normal(0, self.measure_a_noise)
        return self.omega_z + noise_omega_z, self.a_x + noise_ax, self.a_y + noise_ay

    def alpha_from_a(self):
        return atan2(self.a_x, self.a_y)
