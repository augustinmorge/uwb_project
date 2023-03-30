from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def sawtooth2(x, d):
    return d*pi + (x+pi-d*pi) % (2*pi)-pi

def draw_circle(c,r,ax,col,alph=0.7,w=1): 
    e = Ellipse(xy=c, width=2*r, height=2*r, angle=0,linewidth = w)   
    ax.add_artist(e)
    e.set_clip_box(ax.bbox)
    e.set_alpha(alph)  # transparency
    e.set_fill(False)
    e.set_edgecolor(col)  

def path(a, b, r, epsa, epsb):

    ca = a[0:2]+epsa*r*array([[-sin(a[2, 0])], [cos(a[2, 0])]])
    cb = b[0:2]+epsb*r*array([[-sin(b[2, 0])], [cos(b[2, 0])]])
    plot([ca[0, 0], cb[0, 0]], [cb[1, 0], cb[1, 0]], 'black', 'o')
    draw_circle(ca, r, ax, 'green', 1)
    draw_circle(cb, r, ax, 'blue', 1)

    if epsa*epsb == -1: 
        l2 = 0.25*norm(cb-ca)**2-r**2
        if l2 < 0:
            L = float(inf)
            return L
        l = sqrt(l2)  
        alpha = epsb*arctan2(l, r)
    else: 
        l = 0.5*norm(cb-ca)
        alpha = -epsb*pi/2

    R = array([[cos(alpha), -sin(alpha)], [sin(alpha), cos(alpha)]])

    da = ca+r*R@(cb-ca)/norm(cb-ca)
    db = cb+epsa*epsb*(da-ca) 

    betaa = sawtooth2(angle(da-ca) - angle(a[0:2]-ca), epsa)
    betab = sawtooth2(angle(b[0:2]-cb) - angle(db-cb), epsb)
    draw_arc(ca, a[0:2], betaa, 'red')
    draw_arc(cb, b[0:2], -betab, 'red')
    plot([da[0, 0], db[0, 0]], [da[1, 0], db[1, 0]], 'red', linewidth=3)
    L = r*(abs(betaa)+abs(betab))+2*l 
    return L


def sim():
    
    L1 = path(a, b, r, 1, 1)
    L2 = path(a, b, r, -1, 1)  
    L3 = path(a, b, r, -1, -1) 
    L4 = path(a, b, r, 1, -1)  

    L = min([L1, L2, L3, L4])
    
    clear(ax)
    draw_tank(a, "black")
    draw_tank(b, "blue")
    
    if L == L1:
        path(a, b, r, 1, 1)
        sol = "LSL"
    if L == L2:
        path(a, b, r, -1, 1)
        sol = "RSL"
    if L == L3:
        path(a, b, r, -1, -1)
        sol = "RSR"
    if L == L4:
        path(a, b, r, 1, -1)
        sol = "LSR"
        
    ax.set_title(text+" la solution est "+sol)
    pause(4)
    
r = 10

text = "Simulation 1 :"
a, b, ech = array([[-25, 0, pi/2]]).T, array([[25, 0, pi/2]]).T, 50  
ax = init_figure(-ech, ech, -ech, ech)
sim()

text = "Simulation 2 :"
a, b, ech = array([[-40, 0, 1]]).T, array([[40, 0, pi/2]]).T, 60
ax = init_figure(-ech, ech, -ech, ech) 
sim()

text = "Simulation 3 :" 
a, b, ech = array([[-40, 0, 1]]).T, array([[40, 0, -pi/2]]).T, 60 
ax = init_figure(-ech, ech, -ech, ech)
sim()

text = "Simulation 4 :"
a, b, ech = array([[0, 0, 1.7]]).T, array([[3, 0, pi/2]]).T, 30 
ax = init_figure(-ech, ech, -ech, ech)
sim()



