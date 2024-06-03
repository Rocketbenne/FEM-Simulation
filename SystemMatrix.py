import numpy as np

def local_Shit(x1,x2,y1,y2):
    N1 = 1/4[1-xi-eta+eta*xi]
    N2 = 1/4[1+xi-eta-eta*xi]
    N3 = 1/4[1+xi+eta+eta*xi]
    N4 = 1/4[1-xi+eta-eta*xi]

    Ni = N1+N2+N3+N4

    inv_J = np.invert(Ni)
    det_J = x1*y2-x2*y2