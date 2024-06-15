import numpy as np

def gauss(n, func, lower_boundary, upper_boundary):
    """
    :parameter
    n: number of points
    func: function
    lower_boundary, upper_boundary : boundaries for the integral
    :returns
    value: the numerical value of the integral
    """
    x, w = np.polynomial.legendre.leggauss(n)
    temp = (upper_boundary-lower_boundary)/2
    value = np.sum(w*func(temp * x + (upper_boundary+lower_boundary)/2))*temp
    #print(value)

    return value


def gauss2(n, m, func, lower_boundaryX, upper_boundaryX, lower_boundaryY, upper_boundaryY):
    """
    :parameter
    n: number of points
    m: number of points
    func: function
    lower_boundaryX, upper_boundaryX : boundaries for the integral that integrates x        0,1
    lower_boundaryY, upper_boundaryY : boundaries for the integral that integrates y        0,1
    :returns
    value: the numerical value of the double integral
    """
    xi, wi = np.polynomial.legendre.leggauss(n)
    xj, wj = np.polynomial.legendre.leggauss(m)

    J = (upper_boundaryX-lower_boundaryX)/2*(upper_boundaryY-lower_boundaryY)/2
    newXi = lambda x: (upper_boundaryX-lower_boundaryX)/2*x + (upper_boundaryX + lower_boundaryX)/2
    newXj = lambda x: (upper_boundaryY-lower_boundaryY)/2*x + (upper_boundaryY + lower_boundaryY)/2

    value = 0.0
    for i in range(n):
        for j in range(m):
            Xi = newXi(xi[i])
            Xj = newXj(xj[j])
            value += J*wi[i]*wj[j]*func(Xi, Xj)

    return value

def dNi_(xi, eta):
    """
        :parameter
        xi, eta : points for integration
        :returns
        J: Jacobian matrix
    """
    dNi_deta = np.array([-0.25 * (1 - xi), -0.25 * (1 + xi), 0.25 * (1 + xi), 0.25 * (1 - xi)])
    dNi_dxi = np.array([-0.25 * (1 - eta), 0.25 * (1 - eta), 0.25 * (1 + eta), -0.25 * (1 + eta)])
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

    #print(J)

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
            #print(J)
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

    #print(Ke)
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
            #print(J)
            detJ = np.linalg.det(J)


            N = np.array([Na(xi[i], eta[j], 1), Na(xi[i], eta[j], 2), Na(xi[i], eta[j], 3), Na(xi[i], eta[j], 4)])
            fe += N * rho * detJ * weight1[i] * weight2[j]
    return fe


#Jacobian(1,1,np.zeros((4,2)))
#matrix = np.array([[1, 2], [4, 5], [7, 8], [9,10]])
#node_coords = np.array([[0, 20], [10, 20], [0, 0], [10, 0]])
#mat_tensor = np.array([[1, 2], [4, 5]])
#stiffnessMatrix(4,matrix,mat_tensor)
#print(rhs(4,node_coords,1))