#!/usr/bin/python3
from roblib import array, cos, sin, inv, sawtooth, scatter, norm, plot, arctan2, vstack, diag, mvnrnd1, sqrtm, eig
from roblib import Ellipse, eye, log, init_figure, draw_tank, pause, clear, plt
from roblib import pi, linspace, zeros, sqrt, arange, eulermat, eulerderivative
from numpy import linalg, random
import numpy as np


def draw_ellipse0(ax, c, Γ, a, col,coledge='black'):  # classical ellipse (x-c)T * invΓ * (x-c) <a^2
    # draw_ellipse0(ax,array([[1],[2]]),eye(2),a,[0.5,0.6,0.7])
    A = a * sqrtm(Γ)
    w, v = eig(A)
    v1 = array([[v[0, 0]], [v[1, 0]]])
    v2 = array([[v[0, 1]], [v[1, 1]]])
    f1 = A @ v1
    f2 = A @ v2
    φ = (arctan2(v1[1, 0], v1[0, 0]))
    α = φ * 180 / 3.14
    e = Ellipse(xy=c, width=2 * norm(f1), height=2 * norm(f2), angle=α)
    ax.add_artist(e)
    e.set_clip_box(ax.bbox)

    e.set_alpha(0.7)
    e.set_facecolor(col)
    e.set_edgecolor(coledge)

    # e.set_fill(False)
    # e.set_alpha(1)
    # e.set_edgecolor(col)

def draw_ellipse_cov(ax,c,Γ,η, col ='blue',coledge='black'): # Gaussian confidence ellipse with artist
    #draw_ellipse_cov(ax,array([[1],[2]]),eye(2),0.9,[0.5,0.6,0.7])
    if (linalg.norm(Γ)==0):
        Γ=Γ+0.001*eye(len(Γ[1,:]))
    a=sqrt(-2*log(1-η))
    draw_ellipse0(ax, c, Γ, a,col,coledge)

def legende(ax):
    ax.set_title('Filtre de Kalman')
    ax.set_xlabel('x')
    ax.set_ylabel('y')

## Old functions

def g_old(x, Xhat):
    global Wps
    x=x.flatten()
    wp_detected = False
    H = zeros((1,5))
    y = zeros((1,1))
    Beta = []
    global col
    for i in range(Wps.shape[1]):
        a=Wps[:,i].flatten() #wps(i) in (xi,yi)
        da = a-(x[0:2]).flatten()
        dist = norm(da)
        if dist < 15: #On considère qu'on a capté la balise
            plot(array([a[0],x[0]]),array([a[1],x[1]]),"red",1)

            δ = arctan2(da[1],da[0])
            Hi = array([[-sin(δ),cos(δ), 0, 0, 0]])
            yi = [[-sin(δ)*a[0] + cos(δ)*a[1]]]
            if not wp_detected:
                    H = Hi; y = yi
            else:
                H = vstack((H,Hi)); y = vstack((y,yi))
            Beta.append(0.011)

            wp_detected = True

    if not wp_detected: col.append('blue')
    else: col.append('red')
    Γβ = diag(Beta)
    if len(Beta) != 0:
        y = y + mvnrnd1(Γβ)

    return H, y, Γβ, wp_detected
