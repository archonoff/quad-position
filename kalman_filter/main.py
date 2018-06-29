from matplotlib import pyplot as plt

from kalman_filter.simple_copter import SimpleCopter


def main():
    alphas = []
    omegas = []
    copter = SimpleCopter()
    for _ in range(1000):
        # print(copter.alpha_x)
        alphas.append(copter.alpha_x)
        omegas.append(copter.omega_z)
        copter.step()
    plt.grid()
    plt.plot(alphas)
    plt.plot(omegas)
    plt.show()


if __name__ == '__main__':
    main()
