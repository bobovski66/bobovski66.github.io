import numpy as np

def raised_cosine_bump(r, a, b):
    y = np.zeros_like(r)
    mask = (r>=a) & (r<=b)
    x = (r[mask]-a)/(b-a)
    y[mask] = 0.5*(1.0 - np.cos(np.pi*x))
    return y

def positive_energy_profile(r, r1, r2, sigma, tail_scale, w0, c0=0.15, cinf=0.15):
    bump = np.exp(-0.5*((r - 0.5*(r1+r2))/sigma)**2)
    bump *= raised_cosine_bump(r, r1, r2)
    tail = np.exp(-((np.maximum(r - r2, 0.0))/tail_scale)**2)
    core = np.exp(-(r/np.maximum(r1,1e-9))**2)
    w = w0*(c0*core + bump + cinf*tail)
    return w

def cumulative_trapz(y, x):
    out = np.zeros_like(y)
    dx = np.diff(x)
    avg = 0.5*(y[1:] + y[:-1])
    out[1:] = np.cumsum(avg*dx)
    return out

def build_radial(r, r1, r2, sigma_shell, tau_tail, w0, delta_N, rN):
    w = positive_energy_profile(r, r1, r2, sigma_shell, tau_tail, w0)
    m = 4.0*np.pi * cumulative_trapz(w*(r**2), r)
    Lambda = 1.0/(1.0 - 2.0*m/np.maximum(r, 1e-9))
    N = 1.0 - delta_N*np.exp(-(r/np.maximum(rN,1e-9))**2)
    N = 1.0 - (1.0 - N)*np.exp(-((np.maximum(r - r2, 0.0))/np.maximum(tau_tail,1e-9))**2)
    return {"w": w, "m": m, "Lambda": Lambda, "N": N}
