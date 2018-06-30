import numpy as np


def angular_1d_filter(measurements, dt=1):
    np.set_printoptions(precision=3, suppress=True)

    gamma = 1

    def unpack_X(X: np.matrix):
        alpha = X[0, 0]
        w = X[1, 0]
        e = X[2, 0]
        a_x = X[3, 0]
        a_y = X[4, 0]
        return alpha, w, e, a_x, a_y

    def get_F(X: np.matrix):
        alpha, w, e, a_x, a_y = unpack_X(X)

        root = np.sqrt(a_x**2 + a_y**2)
        acos = np.cos(w * dt + e * dt**2)
        asin = np.sin(w * dt + e * dt**2)

        # F = np.matrix([[0, 0, 0, a_y / (a_x**2 + a_y**2), -a_x / (a_x**2 + a_y**2)],
        F = np.matrix([[1, dt, dt**2, 0, 0],
                       [0,  1,    dt, 0, 0],
                       [0,  0,     1, 0, 0],
                       [0,  acos * root * dt, acos * root * dt**2, a_x * asin / root + 1, a_y * asin / root],
                       [0,  -asin * root * dt, -asin * root * dt**2, a_x * acos / root, a_y * acos / root + 1]])
        return F

    def f(X: np.matrix):
        alpha, w, e, a_x, a_y = unpack_X(X)

        root = np.sqrt(a_x**2 + a_y**2)

        X[0, 0] = gamma * alpha + w * dt + (1 - gamma) * np.arctan(a_x / a_y)       # fixme нездоровая фантазия
        X[1, 0] = w + e * dt
        X[2, 0] = e
        X[3, 0] = a_x * np.sin(w * dt) * root
        X[4, 0] = a_y * np.cos(w * dt) * root

        return X

    def get_H(X: np.matrix):
        alpha, w, e, a_x, a_y = unpack_X(X)

        root = np.sqrt(a_x**2 + a_y**2)

        # H = np.matrix([[0, 1, 0, 0, 0],
        #                [np.cos(alpha) * root, 0, 0, a_x * np.sin(alpha) / root, a_y * np.sin(alpha) / root],
        #                [-np.sin(alpha) * root, 0, 0, a_x * np.cos(alpha) / root, a_y * np.cos(alpha) / root]])

        H = np.matrix([[0, 1, 0, 0, 0],
                       [0, 0, 0, 1, 0],
                       [0, 0, 0, 0, 1]])
        return H

    def h(X: np.matrix):
        alpha, w, e, a_x, a_y = unpack_X(X)

        root = np.sqrt(a_x**2 + a_y**2)

        Z = np.matrix([[w],
                       [np.sin(alpha) * root],
                       [np.cos(alpha) * root]])
        return Z

    state_size = 5
    measurements_size = 3

    X = np.matrix([[0.01],
                   [0.01],
                   [0.01],
                   [0.01],
                   [0.01]])
    F = get_F(X)
    H = get_H(X)

    I = np.matrix(np.identity(state_size))
    P = I * 1000

    Q = F * F.T * .12
    R = np.matrix([[0.064,    0,    0],
                   [0, 0.01,    0],
                   [0,    0, 0.01]])

    filtered_alphas = []
    filtered_axs = []
    filtered_ays = []
    for measurement in measurements:
        omega, a_x, a_y = measurement

        F = get_F(X)

        # Predict
        X = f(X)
        # print(X)
        P = F * P * F.T + Q

        # Update
        Z = np.matrix([[*measurement]]).T
        Y = Z - H * X
        # Y = Z - h(X)
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
