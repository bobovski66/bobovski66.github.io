import numpy as np

def sph_to_cart(R, TH, PH):
    X = R * np.sin(TH) * np.cos(PH)
    Y = R * np.sin(TH) * np.sin(PH)
    Z = R * np.cos(TH)
    return X, Y, Z

def build_shell_from_psi(psi, TH, PH, r_in_base=10.0, bulge_amp=3.0, thickness0=4.0, thk_scale=2.0):
    R_inner = r_in_base + bulge_amp * psi
    T_shell = thickness0 + thk_scale * psi
    R_outer = R_inner + T_shell
    return R_inner, R_outer

def write_obj_trimesh(path, X, Y, Z):
    Ntheta, Nphi = X.shape
    verts = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1)
    faces = []
    for i in range(Ntheta-1):
        for j in range(Nphi-1):
            v00 = i*Nphi + j
            v01 = i*Nphi + (j+1)
            v10 = (i+1)*Nphi + j
            v11 = (i+1)*Nphi + (j+1)
            faces.append((v00, v10, v11))
            faces.append((v00, v11, v01))
    for i in range(Ntheta-1):
        j = Nphi-1
        v00 = i*Nphi + j
        v01 = i*Nphi + 0
        v10 = (i+1)*Nphi + j
        v11 = (i+1)*Nphi + 0
        faces.append((v00, v10, v11))
        faces.append((v00, v11, v01))
    with open(path, "w", encoding="utf-8") as f:
        f.write("# warp shell surface\n")
        for v in verts:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for (a,b,c) in faces:
            f.write(f"f {a+1} {b+1} {c+1}\n")

def write_ascii_stl_double(path, Xo, Yo, Zo, Xi, Yi, Zi):
    def faces_from_grid(X, Y, Z):
        Ntheta, Nphi = X.shape
        tris = []
        def tri(p0, p1, p2): tris.append((p0, p1, p2))
        def idx(i,j): return i*Nphi + j
        V = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1)
        for i in range(Ntheta-1):
            for j in range(Nphi-1):
                tri(idx(i,j), idx(i+1,j), idx(i+1,j+1))
                tri(idx(i,j), idx(i+1,j+1), idx(i,j+1))
            j = Nphi-1
            tri(idx(i,j),   idx(i+1,j),   idx(i+1,0))
            tri(idx(i,j),   idx(i+1,0),   idx(i,0))
        return V, tris
    Vo, Fo = faces_from_grid(Xo, Yo, Zo)
    Vi, Fi = faces_from_grid(Xi, Yi, Zi)
    with open(path, "w", encoding="utf-8") as f:
        f.write("solid warp_shell_double\n")
        for (V,F) in [(Vo,Fo), (Vi,Fi)]:
            for (a,b,c) in F:
                f.write("  facet normal 0 0 0\n")
                f.write("    outer loop\n")
                f.write(f"      vertex {V[a][0]} {V[a][1]} {V[a][2]}\n")
                f.write(f"      vertex {V[b][0]} {V[b][1]} {V[b][2]}\n")
                f.write(f"      vertex {V[c][0]} {V[c][1]} {V[c][2]}\n")
                f.write("    endloop\n")
                f.write("  endfacet\n")
        f.write("endsolid warp_shell_double\n")
