import time


def T(A):
    res = [[0 for _ in range(len(A))] for _ in range(len(A[0]))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            res[j][i] = A[i][j]
    return res


def dot(A, B):
    res = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(A[0])):
                res[i][j] += A[i][k] * B[k][j]
    return res


def add_subtract(A, B, sign):
    res = [[0 for _ in range(len(A[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            res[i][j] = A[i][j] + sign * B[i][j]
    return res


def add(A, B):
    return add_subtract(A, B, 1)


def subtract(A, B):
    return add_subtract(A, B, -1)


# Kalman filter functions predict and update
# Copied and simplified from filterpy, R. Labbe
# https://github.com/rlabbe/filterpy
def predict(x, P, F, Q):
    x = dot(F, x)
    P = add(dot(dot(F, P), T(F)), Q)
    return x, P


def update(x, P, z, R, H):
    Hx = dot(H, x)
    y = subtract(z, Hx)
    S = add(dot(dot(H, P), T(H)), R)
    K = dot(dot(P, T(H)), [[1.0 / S[0][0]]])
    x = add(x, dot(K, y))
    KH = dot(K, H)
    I_KH = subtract([[1, 0], [0, 1]], KH)
    P = add(dot(dot(I_KH, P), T(I_KH)), dot(dot(K, R), T(K)))
    return x, P


def calculate_altitude(pressure_pa, qnh_pa):
    return 44330.0 * (1.0 - (pressure_pa / qnh_pa) ** 0.1903)


class Vario:
    '''
    Usage example:
    
    vario = Vario()
    vario.qnh_pa = 102300  # set qnh in Pa
    
    # setting the current pressure
    # triggers a calculation of altitude and speed
    vario.pressure = 98400  
    
    # use the calculated values
    a = vario.altitude
    s = vario.speed
    '''
    def __init__(self):
        self.qnh_pa = 101325.0  # Pa
        self.altitude = 430.0  # m
        self.speed = 0.0  # m/s

        self._pressure = 101325.0  # Pa
        self._last_update = time.time() - 0.1  # s

        self._z = [[self.altitude]]
        self._x = [[self.altitude], [0]]
        self._F = [[1, 1], [0, 1]]
        self._H = [[1, 0]]
        self._P = [[1000, 0], [0, 1000]]
        self._R = [[5e-3]]
        self._Q = [[2.5e-07, 5.0e-06], [5.0e-06, 1.0e-04]]

    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    def pressure(self, value):
        this_update = time.time()
        self._pressure = value

        self._z = [[calculate_altitude(self._pressure, self.qnh_pa)]]  # m
        self._x, self._P = predict(self._x, self._P, self._F, self._Q)
        self._x, self._P = update(self._x, self._P, self._z, self._R, self._H)

        self.altitude = self._x[0][0]  # m
        self.speed = self._x[1][0] / (this_update - self._last_update)  # m/s

        self._last_update = this_update
