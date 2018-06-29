from matplotlib import pyplot as plt
import numpy as np

from kalman_filter.simple_copter import SimpleCopter
from kalman_filter.kalman_filters import only_omega_filter


def demo_run():
    true_alphas = []
    measured_omegas = []
    measured_axs = []
    measured_ays = []

    copter = SimpleCopter()
    for _ in range(1000):
        true_alphas.append(copter.alpha_x)
        omega, a_x, a_y = copter.sense()
        measured_omegas.append(omega)
        measured_axs.append(a_x)
        measured_ays.append(a_y)
        copter.step()

    figure, axes = plt.subplots(nrows=2, ncols=1, sharex=True, gridspec_kw={'height_ratios': (5, 1)})
    figure.set_figheight(8)
    figure.set_figwidth(10)

    ax1, ax2 = axes

    ax1.plot(true_alphas, label='Истиный угол')
    ax1.plot(measured_omegas, label='Измеренная скорость')
    ax2.set_ylabel('Угол/угловая скорость')

    ax2.plot(measured_axs, label='Измеренная проекция ax')
    ax2.plot(measured_ays, label='Измеренная проекция ay')
    ax2.set_xlabel('Время')
    ax2.set_ylabel('Вектор ускорения')

    for axis in axes:
        axis.grid()
        axis.legend()

    plt.show()


def only_omega_run():
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
    plt.plot(measured_omegas, label='Измеренная скорость')
    plt.plot(true_omegas, label='Истиная скорость')
    filtered_omegas = only_omega_filter(measurements=measured_omegas)
    plt.plot(filtered_omegas, label='Отфильтрованная скорость', c='r')
    plt.legend()
    plt.show()


def main():
    demo_run()


if __name__ == '__main__':
    main()
