#!/usr/bin/python3

import os
import numpy as np
import matplotlib.pyplot as plt
from log_data_udp import plot_polynomial_regression
import serial
import datetime
date_str = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

doing_test = 1
nb_anchor = 1

def f_distance(id, d):
    """
    Calculates the distance between an anchor and a tag based on their coordinates.

    Args:
        id (int): the identifier of the anchor.
        d (float): the distance measured between the anchor A and the tag.

    Returns:
        float: the distance between the anchor and the tag.
    """
    coords = {
        1780: {"x": 1.29, "y": 12.543, "z": 1.348},
        1781: {"x": 0, "y": 0, "z": 1.342},
        1782: {"x": -3.167, "y": -11.36, "z": 1.213},
        1783: {"x": 1.1, "y": -28.066, "z": -1.502},
    }

    return np.sqrt(
        (coords[id]["x"] - coords[1780]["x"]) ** 2
        + (coords[id]["y"] - (coords[1780]["y"] - d)) ** 2
        + (coords[id]["z"] - np.sqrt((coords[1780]["z"] ** 2 - 0.2294 ** 2))) ** 2
    )

def load_data(data):
    ids = data[:,0]
    d_real = data[:,1]
    t = data[:,2]
    d_measured = data[:,3]
    RX = data[:,4]
    FP = data[:,5]
    Q = data[:,6]
    return(ids,d_real,t,d_measured,RX,FP,Q)

def f_cancel_adjust(cancel_adjust):
    if cancel_adjust:
        alpha = 2.334
        for i in range(new_RX.shape[0]): #rx in new_RX:
            if new_RX[i]/(1+alpha)-88*alpha > -88 and filename[-44:] != "2023_04_26_16_31_06_Test_multiple_points.csv":
                new_RX[i] = 1/(alpha+1)*(new_RX[i] - 88)
        for i in range(new_FP.shape[0]):
            if new_FP[i]/(1+alpha)-88*alpha > -88 and filename[-44:] != "2023_04_26_16_31_06_Test_multiple_points.csv":
                new_FP[i] = 1/(alpha+1)*(new_FP[i] - 88)

def plot_anchor_data(D, idx, new_d_real, new_RX, new_FP, new_Q, show_all):
    if show_all:
        means_RX = [np.mean(new_RX[(new_d_real == d)]) for d in D]
        means_FP = [np.mean(new_FP[(new_d_real == d)]) for d in D]
        means_Q = [np.mean(new_Q[(new_d_real == d)]) for d in D]

        plt.figure()
        plt.xlabel("Distance [m]")
        plt.ylabel("RX")
        plt.scatter(new_d_real, new_RX)                    
        plt.plot(D, means_RX, color = 'red')
        plt.title("RX - Anchor {}".format(idx))
        plt.grid()

        plt.figure()
        plt.xlabel("Distance [m]")
        plt.ylabel("FP")
        plt.scatter(new_d_real, new_FP)                    
        plt.plot(D, means_FP, color = 'red')
        plt.title("FP - Anchor {}".format(idx))
        plt.grid()

        plt.figure()
        plt.xlabel("Distance [m]")
        plt.ylabel("Q")
        plt.scatter(new_d_real, new_Q)                    
        plt.plot(D, means_Q, color = 'red')
        plt.title("Q - Anchor {}".format(idx))
        plt.grid()

        plt.figure()
        plt.xlabel("Distance [m]")
        plt.ylabel("RX - FP")
        plt.scatter(new_d_real, new_RX - new_FP)                    
        plt.plot(D, np.array(means_RX) - np.array(means_FP), color = 'red')
        plt.title("RX - FP - Anchor {}".format(idx))
        plt.grid()
    else:
        # do something else if show_all is False
        pass


if doing_test:

    udp = input("udp ? (y/n)").lower()
    while udp not in ['y', 'n']:
        udp = input("Press [y] or [n]").lower()

    if udp == 'y':
        from log_data_udp import *
        data, addr = connect_to_tag()

        print("Start test..")
        file = open(f"{THIS_FOLDER}/udp/{date_str}_Serial_Test_multiple_points.csv", "w")
        file.write("n°anchor; d_real [m]; time [ms]; d_measured [m]; RX [dbm]; FP [dbm]; Q;\n")

        D = main(file, data)

        file.close()

    else:
        from log_data_serial import *
        ser = serial.Serial('COM5', 115200)

        print("Start test..")
        file = open(f"{THIS_FOLDER}/serial/{date_str}_Serial_Test_multiple_points.csv", "w")
        file.write("n°anchor; d_real [m]; time [ms]; d_measured [m]; RX [dbm]; FP [dbm]; Q;\n")

        D = main(file, ser)

        file.close()

else:
    filenames = []
    # filenames = [f"{THIS_FOLDER}/udp/2023_04_27_14_17_12_Test_multiple_points.csv"]
    # filenames = [f"{THIS_FOLDER}/udp/2023_05_02_15_09_14_Test_multiple_points.csv"]
    # filenames = [f"{THIS_FOLDER}/udp/2023_05_03_16_12_38_Test_multiple_points.csv"]
    filenames = [f"{THIS_FOLDER}/serial/2023_05_03_16_12_38_Serial_Test_multiple_points.csv"] 
    # filenames = [f"{THIS_FOLDER}/serial/2023_05_09_15_42_31_Serial_Test_multiple_points.csv"] #Proche de la première ancre 2023_05_03_16_12_38_Serial_Test_multiple_points
    # filenames = [f"{THIS_FOLDER}/serial/2023_05_09_15_55_34_Serial_Test_multiple_points.csv"] #Loin de la première ancre

    show_all = 0
    cancel_adjust = 0
    add_filter = 1
    add_offset = 0
    
    for filename in filenames:
        data = np.genfromtxt(filename, delimiter=';', skip_header=1)
        ids,d_real,t,d_measured,RX,FP,Q = load_data(data)
        
        L_new_d_measured = []; L_D_mean_mes = []; L_new_d_real = []; L_D = []

        for idx in np.unique(ids):

            D_mean_real = []
            D_mean_mes = []

            false_value = np.abs(d_measured[ids == idx] - f_distance(idx,d_real)[ids == idx]) > 2
            if not add_filter : false_value[1:] = False

            indices = np.where(np.abs(d_measured[ids == idx] - f_distance(idx,d_real)[ids == idx]) > 2)
            
            new_ids = ids[ids == idx][~false_value]
            new_d_real = d_real[ids == idx] 
            new_d_real = f_distance(idx,new_d_real)[~false_value]
            D = np.unique(new_d_real)

            new_t = t[ids == idx][~false_value]
            new_d_measured = d_measured[ids == idx][~false_value]
            
            # Add offset when we start
            if add_offset : new_d_measured = new_d_measured + (np.mean(new_d_real[new_d_real == D[0]] - new_d_measured[new_d_real == D[0]]))
            
            new_RX = RX[ids == idx][~false_value]
            new_FP = FP[ids == idx][~false_value]
            new_Q = Q[ids == idx][~false_value]

            f_cancel_adjust(cancel_adjust)
            
            for d in D:
                D_mean_mes.append(np.mean(new_d_measured[new_d_real == d]))
                
            D_mean_mes = np.array(D_mean_mes)

            L_new_d_measured.append(new_d_measured)
            L_D_mean_mes.append(D_mean_mes)
            L_new_d_real.append(new_d_real)
            L_D.append(D)

            print(f"Résidus = {(D_mean_mes - D)}")
            print(f"Ecart-type des résidus = {np.std(D_mean_mes - D)}")
            print(f"Moyenne des résidus = {np.mean(D_mean_mes - D)}\n")

            plot_anchor_data(D, idx, new_d_real, new_RX, new_FP, new_Q, show_all=False)
            
        ### DISPLAY
        fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
        fig.suptitle(filename.split("/")[-1])
        for i in range(2):
            for j in range(2):
                ax = axs[i,j]
                idx = 2*i + j
                ax.set_xlabel("Distance (m)")
                ax.set_ylabel("Measured Range (m)")
                ax.set_title("Anchor n°{}".format(80 + idx))
                ax.set_xlim([0, int(np.max(D)+5)])
                ax.set_ylim([0, int(np.max(D)+5)])
                ax.scatter(L_new_d_measured[idx], L_new_d_real[idx], label = 'data', s = 0.4)
                ax.plot(range(0,int(np.max(D))+5),range(0,int(np.max(D))+5))
                plot_polynomial_regression(ax, L_D_mean_mes[idx], L_D[idx], [1])
    plt.show()


    mean_res_error = []
    mean_res_error_at = []
    VAL = range(2,len(D)+2)
    import copy
    for val in VAL:
        m_r_e = 0
        m_r_e_at = 0
        # fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
        # fig.suptitle(f"after transfo, val = {val}")
        coeffs_ini = [];

        for i in range(2):
            for j in range(2):
                idx = 2*i + j
                ai, bi = [np.polyfit(L_D_mean_mes[idx][:val], L_D[idx][:val], degree) for degree in [1]][0].flatten()
                m_r_e += np.linalg.norm(L_D_mean_mes[idx] - L_D[idx])
                m_r_e_at += np.linalg.norm(ai*L_D_mean_mes[idx] + bi - L_D[idx])

                # #display
                # ax = axs[i,j]
                # ax.set_xlabel("Distance (m)")
                # ax.set_ylabel("Measured Range (m)")
                # ax.set_title("Anchor n°{}".format(80 + idx))
                # ax.set_xlim([0, int(np.max(D)+5)])
                # ax.set_ylim([0, int(np.max(D)+5)])
                # ax.scatter(ai*L_new_d_measured[idx] + bi, L_new_d_real[idx], label = 'data', s = 0.4)
                # ax.plot(range(0,int(np.max(D))+5),range(0,int(np.max(D))+5))
                # plot_polynomial_regression(ax, ai*L_D_mean_mes[idx] + bi, L_D[idx], [1])

        mean_res_error_at.append(m_r_e_at/4)
        mean_res_error.append(m_r_e/4)

    plt.figure()
    plt.title("Moyenne des résidus")
    plt.xlabel("valeurs initiales prises")
    plt.ylabel("Erreurs")
    plt.ylim([0,10])
    plt.plot(VAL,mean_res_error,label='before transfo')
    plt.plot(VAL,mean_res_error_at, label = 'after transfo')
    plt.legend()
    plt.show()

    try : 
        val = int(input("How many values for calibration ?"))
    except :
        val = 10

    fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
    fig.suptitle(filename[-44:])
    for i in range(2):
        for j in range(2):
            ax = axs[i,j]
            idx = 2*i + j
            ai, bi = [np.polyfit(L_D_mean_mes[idx][:val], L_D[idx][:val], degree) for degree in [1]][0].flatten()
            ax.set_xlabel("Distance (m)")
            ax.set_ylabel("Measured Range (m)")
            ax.set_title("Anchor n°{}".format(80 + idx))
            ax.set_xlim([0, int(np.max(D)+5)])
            ax.set_ylim([0, int(np.max(D)+5)])
            ax.scatter(L_new_d_measured[idx], L_new_d_real[idx], label = 'data bc', s = 0.4)
            ax.scatter(ai*L_new_d_measured[idx]+bi, L_new_d_real[idx], label = 'after bc', s = 0.4)
            ax.plot(range(0,int(np.max(D))+5),range(0,int(np.max(D))+5))
            plot_polynomial_regression(ax, L_D_mean_mes[idx], L_D[idx], [1], label='before calibration')
            plot_polynomial_regression(ax, ai*L_D_mean_mes[idx]+bi, L_D[idx], [1],label='after calibration')

            print(f"Résidus = {(ai*L_D_mean_mes[idx]+bi - L_D[idx])}")
            print(f"Ecart-type des résidus = {np.std(ai*L_D_mean_mes[idx]+bi - L_D[idx])}")
            print(f"Moyenne des résidus = {np.mean(ai*L_D_mean_mes[idx]+bi - L_D[idx])}\n")
    plt.show()