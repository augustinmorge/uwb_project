from roblib import *
from sympy import *
from sympy.diffgeom import *

def L(F,g,i=1):
    if size(g)==2 :
        return Matrix([[L(F,g[0],i)],[L(F,g[1],i)]])
    if i==1 :
        return LieDerivative(F,g)
    return L(F,L(F,g,i-1))

def build_rhophi():
    C = CoordSystem('C', Patch('P',Manifold('M',5)), ["x1","x2","x3","x4","x5"])
    x1, x2, x3, x4, x5 = C.coord_functions()
    E = C.base_vectors()
    v1, a2 = symbols("v1 a2")
    Fx = x5*cos(x3)*E[0] + x5*sin(x3)*E[1] + x5*sin(x3-x4)*E[3]
    Gx1, Gx2 = E[2], E[4]
    Hx1, Hx2 = x1-cos(x4), x2-sin(x4)
    
    z3 = x5*cos(x3-x4)
    A = Matrix([[L(Gx1,z3), L(Gx2,z3)],
                [L(Gx1,L(Fx,x4)), L(Gx2,L(Fx,x4))]])
    b = Matrix([L(Fx,z3), L(Fx,x4,2)])
    
    rho = lambdify((x1,x2,x3,x4,x5,v1,a2), A.inv()*(Matrix([v1,a2])-b))
    phi = lambdify((x1,x2,x3,x4,x5,v1), Matrix([Hx1,Hx2,z3,v1,x4,x5*sin(x3-x4)]))
    
    return rho, phi

def psi(y1,y2):
    return y2, -(1*(y1**2)-1)*y2-y1

def build_bet():
    C = CoordSystem('C', Patch('P',Manifold('M',6)), ["z1","z2","z3","z4","z5","z6"])
    z1, z2, z3, z4, z5, z6 = C.coord_functions()
    E = C.base_vectors()
    Fz = z3*cos(z5)*E[0] + z3*sin(z5)*E[1] + z4*E[2] + z6*E[4]
    Gz1, Gz2 = E[3], E[5]
    Hz = Matrix([z1, z2])
    e = L(Fz,Hz) - Matrix(psi(z1,z2))
    de = L(Fz,Hz,2) - L(Fz,psi(z1,z2))
    Lgz = L(Gz1,L(Fz,Hz,2)).row_join(L(Gz2,L(Fz,Hz,2)))
    bet = lambdify((z1, z2, z3, z4, z5, z6), -Lgz.inv()*(L(Fz,Hz,3)-L(Fz,psi(z1,z2),2)+e+2*de))
    return bet

x = np.array([[0,0,0,0,1]]).T
v1, dt, sc = 0, 0.02, 3
ax = init_figure(-sc,sc,-sc,sc)
rho, phi = build_rhophi()
bet = build_bet()
for k in range(0,500):
    clear(ax)
    x1, x2, x3, x4, x5 = x[0:5,0]
    draw_field(ax,psi,-sc,sc,-sc,sc,0.3)
    draw_tank_trailer(x1, x2, x3, x4, x5)
    z = phi(x1, x2, x3, x4, x5, v1)
    a = bet(*z)
    a1, a2 = a[0:2,0,0]
    v1 += a1*dt
    u = rho(x1, x2, x3, x4, x5, v1, a2)
    u1, u2 = u[0:2,0]
    x = x + np.array([[x5*np.cos(x3)],[x5*np.sin(x3)],[u1],[x5*np.sin(x3-x4)],[u2]])*dt
    
    