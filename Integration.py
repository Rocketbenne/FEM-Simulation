import numpy as np

def dNi_(xi, eta):
    """
        :parameter
        xi, eta : points for integration
        :returns
        J: Jacobian matrix
    """

    dNi_dxi = np.array([-0.25 * (1 - xi), -0.25 * (1 + xi), 0.25 * (1 + xi), 0.25 * (1 - xi)])
    dNi_deta = np.array([-0.25 * (1 - eta), 0.25 * (1 - eta), 0.25 * (1 + eta), -0.25 * (1 + eta)])
    return dNi_dxi, dNi_deta


def Jacobian(xi, eta , glob_coords):
    """
       :parameter
       xi, eta : points for integration
       glob_coords : global coordinates
       :returns
       J: Jacobian matrix
    """
    dNi_dxi, dNi_deta = dNi_(xi, eta)
    J = np.zeros((2, 2))
    J[0, 0] = dNi_dxi[0]*glob_coords[0][0] + dNi_dxi[1]*glob_coords[1][0] + dNi_dxi[2]*glob_coords[2][0] + dNi_dxi[3]*glob_coords[3][0]
    J[0, 1] = dNi_dxi[0]*glob_coords[0][1] + dNi_dxi[1]*glob_coords[1][1] + dNi_dxi[2]*glob_coords[2][1] + dNi_dxi[3]*glob_coords[3][1]
    J[1, 0] = dNi_deta[0]*glob_coords[0][0] + dNi_deta[1]*glob_coords[1][0] + dNi_deta[2]*glob_coords[2][0] + dNi_deta[3]*glob_coords[3][0]
    J[1, 1] = dNi_deta[0] * glob_coords[0][1] + dNi_deta[1] * glob_coords[1][1] + dNi_deta[2] * glob_coords[2][1] + dNi_deta[3] * glob_coords[3][1]

    return J


def stiffnessMatrix(order,coords,mat_tensor):
    """
     :parameter
     order: order of the stiffness matrix
     coords: global coordinates of the Elements
     mat_tensor: material tensor should be 2x2 ?
     :returns
     Ke: stiffness matrix of each element
     """
    xi,weight1 = np.polynomial.legendre.leggauss(order)
    eta, weight2 = np.polynomial.legendre.leggauss(order)
    Ke = np.zeros((4,4))
    for i in range(order):
        for j in range(order):
            J = Jacobian(xi[i],eta[j],coords)
            detJ = np.linalg.det(J)
            invJ = np.linalg.inv(J)


            global_Na = np.zeros(4)
            global_Nb = np.zeros(4)
            dN_dxi, dN_deta = dNi_(xi[i], eta[j])
            for k in range(4):
                global_Na[k] = invJ[0, 0] * dN_dxi[k] + invJ[0, 1] * dN_deta[k]
                global_Nb[k] = invJ[1, 0] * dN_dxi[k] + invJ[1, 1] * dN_deta[k]
            B = np.array([global_Na, global_Nb])

            Ke += (B.T @ mat_tensor @ B) * detJ * weight1[i] * weight2[j]
    return Ke


def Na(xi, eta, node):
    if node == 1:
        return 0.25 * (1 - xi) * (1 - eta)
    elif node == 2:
        return 0.25 * (1 + xi) * (1 - eta)
    elif node == 3:
        return 0.25 * (1 + xi) * (1 + eta)
    elif node == 4:
        return 0.25 * (1 - xi) * (1 + eta)

    return 0


def rhs(order, glob_coords, rho):
    xi, weight1 = np.polynomial.legendre.leggauss(order)  #could do it with one but this is clearer
    eta, weight2 = np.polynomial.legendre.leggauss(order)
    fe = np.zeros(4)
    for i in range(order):
        for j in range(order):
            J = Jacobian(xi[i],eta[j],glob_coords)
            detJ = np.linalg.det(J)

            N = np.array([Na(xi[i], eta[j], 1), Na(xi[i], eta[j], 2), Na(xi[i], eta[j], 3), Na(xi[i], eta[j], 4)])
            fe += N * rho * detJ * weight1[i] * weight2[j]
    return fe
