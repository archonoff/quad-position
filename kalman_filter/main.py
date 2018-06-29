from matplotlib import pyplot as plt
import numpy as np

from kalman_filter.simple_copter import SimpleCopter
from kalman_filter.kalman_filters import only_omega_filter


def demo_run():
    true_alphas = []
    true_omegas = []
    measured_alphas = []
    measured_omegas = []

    copter = SimpleCopter()
    for _ in range(1000):
        true_alphas.append(copter.alpha_x)
        true_omegas.append(copter.omega_z)
        alpha, omega = copter.sense()
        measured_alphas.append(alpha)
        measured_omegas.append(omega)
        copter.step()
    plt.figure(figsize=(10, 6))
    plt.grid()
    plt.xlabel('Время')
    plt.ylabel('Угол/угловая скорость')
    # plt.plot(measured_alphas, label='Измеренный угол')
    plt.plot(measured_omegas, label='Измеренная скорость')
    # plt.plot(true_alphas, label='Истиный угол')
    plt.plot(true_omegas, label='Истиная скорость')
    filtered_omegas = only_omega_filter(measurements=measured_omegas)
    plt.plot(filtered_omegas, label='Отфильтрованная скорость', c='r')
    plt.legend()
    plt.show()


def main():
    demo_run()


if __name__ == '__main__':
    main()
