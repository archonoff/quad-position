import numpy as np


def angular_1d_filter(measurements, dt=1):
    np.set_printoptions(precision=3, suppress=True)

    def get_F(X: np.matrix):
        F = np.matrix([[1, dt, dt**2, 0, 0],
                       [0,  1,    dt, 0, 0],
                       [0,  0,     1, 0, 0],
                       [0,  0,     0, 1, 0],
                       [0,  0,     0, 0, 1]])
        return F

    state_size = 5

    X = np.matrix([[0.01],
                   [0.01],
                   [0.01],
                   [0.01],
                   [0.01]])
    F = get_F(X)
    H = np.matrix([[1, 0, 0, 0, 0],
                   [0, 1, 0, 0, 0],
                   [0, 0, 0, 1, 0],
                   [0, 0, 0, 0, 1]])

    I = np.matrix(np.identity(state_size))
    P = I * 1000

    Q = F * F.T * .0001
    R = np.matrix([[100,    0,    0,    0],
                   [  0, 1000,    0,    0],
                   [  0,    0, 0.01,    0],
                   [  0,    0,    0, 0.01]])

    filtered_alphas = []
    filtered_axs = []
    filtered_ays = []
    for measurement in measurements:
        omega, a_x, a_y = measurement
        alpha = np.arctan(a_x / a_y)

        F = get_F(X)

        # Predict
        X = F * X
        P = F * P * F.T + Q

        # Update
        Z = np.matrix([[alpha, omega, a_x, a_y]]).T
        Y = Z - H * X
        S = H * P * H.T + R
        K = P * H.T * np.linalg.pinv(S)

        X = X + K * Y
        P = (I - K * H) * P

        filtered_alphas.append(X[0, 0])
        filtered_axs.append(X[3, 0])
        filtered_ays.append(X[4, 0])

    return filtered_alphas, filtered_axs, filtered_ays


def only_omega_filter(measurements, dt=1):
    # F = np.matrix([[1, dt],
    #                [0, 1]])
    # H = np.matrix([[1, 0]])
    # I = np.matrix(np.identity(2))
    # P = I * 1000
    # Q = F * F.T * .005
    # R = np.matrix(np.identity(1)) * 3
    #
    # X = np.matrix([[0.],
    #                [0.]])

    F = np.matrix([[1, dt, dt**2],
                   [0, 1, dt],
                   [0, 0, 1]])
    H = np.matrix([[1, 0, 0]])
    I = np.matrix(np.identity(3))
    P = I * 1000
    Q = F * F.T * .000001
    Q = I * .000000001
    R = np.matrix(np.identity(1)) * 4

    X = np.matrix([[0.],
                   [0.],
                   [0.]])

    filtered_omegas = []
    for measurement in measurements:
        # Predict
        X = F * X
        P = F * P * F.T + Q

        # Update
        Z = np.matrix([[measurement]])
        Y = Z - H * X
        S = H * P * H.T + R
        K = P * H.T * np.linalg.pinv(S)

        X = X + K * Y
        P = (I - K * H) * P

        filtered_omegas.append(X[0, 0])

    return filtered_omegas
