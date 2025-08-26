import numpy as np
import matplotlib.pyplot as plt

def plot_radial(r, w, m, Lambda, N, save_prefix=None):
    plt.figure(figsize=(8,5), dpi=140); plt.plot(r, w); plt.xlabel('r'); plt.ylabel('w(r)'); plt.title('Energy Density w(r)');
    if save_prefix: plt.savefig(f"{save_prefix}_w.pdf", bbox_inches='tight'); plt.show()
    plt.figure(figsize=(8,5), dpi=140); plt.plot(r, m); plt.xlabel('r'); plt.ylabel('m(r)'); plt.title("Enclosed Mass m(r) = 4π ∫ w r'^2 dr'");
    if save_prefix: plt.savefig(f"{save_prefix}_m.pdf", bbox_inches='tight'); plt.show()
    plt.figure(figsize=(8,5), dpi=140); plt.plot(r, Lambda); plt.xlabel('r'); plt.ylabel('Λ(r)'); plt.title('Metric Function Λ(r)');
    if save_prefix: plt.savefig(f"{save_prefix}_Lambda.pdf", bbox_inches='tight'); plt.show()
    plt.figure(figsize=(8,5), dpi=140); plt.plot(r, N); plt.xlabel('r'); plt.ylabel('N(r)'); plt.title('Time-Rate Function N(r)');
    if save_prefix: plt.savefig(f"{save_prefix}_N.pdf", bbox_inches='tight'); plt.show()

def plot_psi_heatmap(PSI, theta_grid, phi_grid, save_path=None):
    plt.figure(figsize=(8,5), dpi=140)
    plt.imshow(PSI, origin='lower', extent=[phi_grid[0], phi_grid[-1], theta_grid[0], theta_grid[-1]], aspect='auto')
    plt.xlabel('φ'); plt.ylabel('θ'); plt.title('Screen Potential ψ(θ, φ)');
    plt.colorbar();
    if save_path: plt.savefig(save_path, bbox_inches='tight');
    plt.show()

def plot_wireframes(Xo, Yo, Zo, Xi, Yi, Zi, save_path=None):
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    import numpy as np
    fig = plt.figure(figsize=(6,6), dpi=140); ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(Xo, Yo, Zo, rstride=5, cstride=9, linewidth=0.35)
    ax.plot_wireframe(Xi, Yi, Zi, rstride=5, cstride=9, linewidth=0.35)
    M = np.max(np.sqrt(Xo**2 + Yo**2 + Zo**2))
    ax.set_box_aspect((1,1,1)); ax.set_xlim(-M, M); ax.set_ylim(-M, M); ax.set_zlim(-M, M)
    ax.set_title('Warp Shell Mockup (inner + outer)')
    if save_path: plt.savefig(save_path, bbox_inches='tight')
    plt.show()
