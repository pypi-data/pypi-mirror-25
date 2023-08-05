import numpy as np
from scipy.integrate import tplquad


def phi1(s, t, u, zeta, Z=2):
    return np.exp(-zeta * s)


def phi1_du(s, t, u, zeta, Z=2):
    return 0.0


def phi1_dt(s, t, u, zeta, Z=2):
    return 0.0


def phi1_ds(s, t, u, zeta, Z=2):
    return -zeta * np.exp(-zeta * s)


def H11_vpm(t, u, s, zeta=1.6875, Z=2):
    return np.exp(-2 * s * zeta) * (s * s - t * t - 4.0 * s * u * Z + (s - t) * (s + t) * u * zeta * zeta)


def S11_vpm(t, u, s, zeta=1.6875, Z=2):
    return u * (s * s - t * t) * phi1(s, t, u, zeta) * phi1(s, t, u, zeta)


def expected_phi1(zeta):
    # this is how we 3-d integrate
    S11_int, error = tplquad(S11_vpm,
                             0.0, np.inf,
                             lambda x: 0.0, lambda x: x,
                             lambda x, y: 0.0, lambda x, y: y,
                             args=(zeta, 2.0))
    H11_int, error = tplquad(H11_vpm,
                             0.0, 50.0,
                             lambda x: 0.0, lambda x: x,
                             lambda x, y: 0.0, lambda x, y: y,
                             args=(zeta, 2.0))
    return H11_int / S11_int

############################## PHI 2 ########################


def phi2(s, t, u, zeta, Z=2):
    return np.exp(-zeta * s) * u


def phi2_du(s, t, u, zeta, Z=2):
    return np.exp(-zeta * s)


def phi2_dt(s, t, u, zeta, Z=2):
    return 0.0


def phi2_ds(s, t, u, zeta, Z=2):
    return -zeta * np.exp(-zeta * s) * u

############################## PHI 3 ########################


def phi3(s, t, u, zeta, Z=2):
    return np.exp(-zeta * s) * t * t


def phi3_du(s, t, u, zeta, Z=2):
    return 0.0


def phi3_dt(s, t, u, zeta, Z=2):
    return 2.0 * np.exp(-zeta * s) * t


def phi3_ds(s, t, u, zeta, Z=2):
    return -zeta * np.exp(-zeta * s) * t * t

############################## PHI 4 ########################


def phi4(s, t, u, zeta, Z=2):
    return np.exp(-zeta * s) * s


def phi4_du(s, t, u, zeta, Z=2):
    return 0.0


def phi4_dt(s, t, u, zeta, Z=2):
    return 0.0


def phi4_ds(s, t, u, zeta, Z=2):
    return np.exp(-zeta * s) * (1.0 - s * zeta)

############################## PHI 5 ########################


def phi5(s, t, u, zeta, Z=2):
    return np.exp(-zeta * s) * s * s


def phi5_du(s, t, u, zeta, Z=2):
    return 0.0


def phi5_dt(s, t, u, zeta, Z=2):
    return 0.0


def phi5_ds(s, t, u, zeta, Z=2):
    return np.exp(-zeta * s) * s * (2.0 - s * zeta)

############################## PHI 6 ########################


def phi6(s, t, u, zeta, Z=2):
    return np.exp(-zeta * s) * u * u


def phi6_du(s, t, u, zeta, Z=2):
    return 2.0 * u * np.exp(-zeta * s)


def phi6_dt(s, t, u, zeta, Z=2):
    return 0.0


def phi6_ds(s, t, u, zeta, Z=2):
    return -zeta * u * u * np.exp(-zeta * s)

############################## PHI 7 ########################


def phi7(s, t, u, zeta, Z=2):
    return np.exp(-zeta * s) * s * u


def phi7_du(s, t, u, zeta, Z=2):
    return u * np.exp(-zeta * s)


def phi7_dt(s, t, u, zeta, Z=2):
    return 0.0


def phi7_ds(s, t, u, zeta, Z=2):
    return np.exp(-zeta * s) * (u - s * u * zeta)

############################## PHI 8 ########################


def phi8(s, t, u, zeta, Z=2):
    return np.exp(-zeta * s) * t * t * u


def phi8_du(s, t, u, zeta, Z=2):
    return t * t * np.exp(-zeta * s)


def phi8_dt(s, t, u, zeta, Z=2):
    return 2.0 * t * u * np.exp(-zeta * s)


def phi8_ds(s, t, u, zeta, Z=2):
    return -t * t * u * zeta * np.exp(-zeta * s)

############################## PHI 9 ########################


def phi9(s, t, u, zeta, Z=2):
    return np.exp(-zeta * s) * u * u * u


def phi9_du(s, t, u, zeta, Z=2):
    return 3.0 * u * u * np.exp(-zeta * s)


def phi9_dt(s, t, u, zeta, Z=2):
    return 0.0


def phi9_ds(s, t, u, zeta, Z=2):
    return -u * u * u * zeta * np.exp(-zeta * s)

############################## PHI 10 ########################


def phi10(s, t, u, zeta, Z=2):
    return np.exp(-zeta * s) * t * t * u * u


def phi10_du(s, t, u, zeta, Z=2):
    return 2.0 * t * t * u * np.exp(-zeta * s)


def phi10_dt(s, t, u, zeta, Z=2):
    return 2.0 * t * u * u * np.exp(-zeta * s)


def phi10_ds(s, t, u, zeta, Z=2):
    return -t * t * u * u * zeta * np.exp(-zeta * s)


def H11_pm():
    return -2 - 2 + 5.0 / 4.0


def H12_pm():
    H_12a = (4096.0 / 64827.0) * np.sqrt(2) * 2
    H_12b = (4096.0 / 64827.0) * np.sqrt(2) * 2
    H_12 = (1.0 / np.sqrt(2)) * (H_12a + H_12b)
    return H_12


def H22_pm():
    return  (2 * J22_pm() + 2 * K22_pm())


def J22_pm():
    return -5.0 / 2.0 + (17.0 / 81.0) * 2


def K22_pm():
    return (16.0 / 729.0) * 2


def H0():
    H = np.zeros((2, 2))
    H[0, 0] = H11_pm() - 5.0 / 4.0
    H[1, 1] = -5.0 / 2.0
    return H


def H1(lam):
    H = np.zeros((2, 2))
    H[0, 0] = 5.0 / 4.0 * lam
    H[0, 1] = H12_pm() * lam
    H[1, 0] = H12_pm() * lam
    H[1, 1] = 2 * (J22_pm() + 5.0 / 2.0) + 2 * K22_pm()
    return H


def H_lambda(lam):
    return H0() + H1(lam)


def ci_hamiltonian():
    # precomputed integrals
    H = np.zeros((2, 2))

    H[0, 0] = H11_pm()
    H[0, 1] = H12_pm()
    H[1, 0] = H12_pm()
    H[1, 1] = H22_pm()
    return H
