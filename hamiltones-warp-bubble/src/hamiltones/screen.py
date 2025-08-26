import numpy as np

def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))

def smooth_cap_psi(theta, theta0, kappa):
    return sigmoid(kappa*(np.cos(theta) - np.cos(theta0)))

def axisymmetric_psi(theta, phi, theta0, kappa, eps_phi=0.0, m_phi=0):
    base = smooth_cap_psi(theta, theta0, kappa)
    if eps_phi and m_phi:
        mod  = 1.0 + eps_phi*np.cos(m_phi*phi)
        out  = base*mod
    else:
        out = base
    return np.clip(out, 0.0, None)

def shape_field(psi, a=6.0, b=0.0):
    return sigmoid(a*psi + b)
