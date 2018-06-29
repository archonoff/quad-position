from math import sin, cos


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

    def __init__(self):
        self.alpha_func = lambda t: 30 * sin(t)
        self.omega_func = lambda t: 30 * cos(t)

    def step(self):
        self.t += self.dt
        self.alpha_x = self.alpha_func(self.t)
        self.omega_z = self.omega_func(self.t)
        self.a_x = ''
        self.a_y = ''
