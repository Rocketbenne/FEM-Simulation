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
    lower_boundaryX, upper_boundaryX : boundaries for the integral that integrates x
    lower_boundaryY, upper_boundaryY : boundaries for the integral that integrates y
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

    print(value)
    return value



gauss(5, lambda x: 2*x**2, 2, 4)
gauss2(5, 5,lambda x,y:x**2+y,1,2,5,4)





