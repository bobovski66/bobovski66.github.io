import numpy as np
from hamiltones.screen import axisymmetric_psi, smooth_cap_psi
from hamiltones.radial import build_radial
from hamiltones.mesh import sph_to_cart, build_shell_from_psi, write_obj_trimesh, write_ascii_stl_double
from hamiltones.plotting import plot_radial, plot_psi_heatmap, plot_wireframes

mode       = 'axisymmetric'   # 'spherical' or 'axisymmetric'
theta0_deg = 30.0; kappa=8.0; eps_phi=0.25; m_phi=4
r_max=50.0; r1, r2 = 12.0, 18.0; sigma_shell=2.5; tau_tail=6.0; w0=1.2e-4
delta_N=0.15; rN=r1
r_in_base=10.0; bulge_amp=3.0; thickness0=4.0; thk_scale=2.0
Nr, Ntheta, Nphi = 4000, 240, 360

theta = np.linspace(0.0, np.pi, Ntheta); phi = np.linspace(0.0, 2*np.pi, Nphi)
TH, PH= np.meshgrid(theta, phi, indexing='ij')
theta0 = np.deg2rad(theta0_deg)
if mode == 'spherical':
    PSI = smooth_cap_psi(TH, theta0, kappa)
else:
    PSI = axisymmetric_psi(TH, PH, theta0, kappa, eps_phi, m_phi)

r = np.linspace(1e-6, r_max, Nr)
rad = build_radial(r, r1, r2, sigma_shell, tau_tail, w0, delta_N, rN)
plot_radial(r, rad['w'], rad['m'], rad['Lambda'], rad['N'], save_prefix='outputs/radial')
plot_psi_heatmap(PSI, theta, phi, save_path='outputs/psi_heatmap.png')
R_inner, R_outer = build_shell_from_psi(PSI, TH, PH, r_in_base=r_in_base, bulge_amp=bulge_amp,
                                        thickness0=thickness0, thk_scale=thk_scale)
Xi, Yi, Zi = sph_to_cart(R_inner, TH, PH)
Xo, Yo, Zo = sph_to_cart(R_outer, TH, PH)
plot_wireframes(Xo, Yo, Zo, Xi, Yi, Zi, save_path='outputs/warp_shell_wireframe.png')
write_obj_trimesh('outputs/warp_shell_outer.obj', Xo, Yo, Zo)
write_obj_trimesh('outputs/warp_shell_inner.obj', Xi, Yi, Zi)
write_ascii_stl_double('outputs/warp_shell_double.stl', Xo, Yo, Zo, Xi, Yi, Zi)
print('Done. Outputs in ./outputs')
