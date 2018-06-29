import numpy as np


def angular_1d_filter(measurements, dt=1):
    pass


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
