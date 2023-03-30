#!/usr/bin/python3
import time
import socket
import json
import keyboard
import numpy as np
import matplotlib.pyplot as plt
import os

# Modules pour l'interpolation
from scipy import stats
from scipy.interpolate import interp1d
from sklearn.metrics import r2_score

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def connect_to_tag():
    hostname = socket.gethostname()
    UDP_IP = socket.gethostbyname(hostname)
    print("***Local ip:" + str(UDP_IP) + "***")
    UDP_PORT = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.listen(1)  # 接收的连接数
    print("En attente de connexion...")
    data, addr = sock.accept()
    print("Connected !")

    return data, addr

# def read_data():
#     line = data.recv(1024).decode('UTF-8')
#     uwb_list = []

#     try:
#         uwb_data = json.loads(line)
#         print(uwb_data)

#         uwb_list = uwb_data["links"]
#         # for uwb_archor in uwb_list:
#         #     print(uwb_archor)

#     except:
#         print(line)
#     print("")

# #     return uwb_list
    
def read_data():
    data.setblocking(False)
    try:
        line = data.recv(1024).decode('UTF-8')
    except BlockingIOError:
        return []  # retourne une liste vide si aucun donnée n'est disponible

    # print("Received data:", line) # Ajout d'une instruction de débogage
    
    uwb_list = []

    try:
        uwb_data = json.loads(line)
        print(uwb_data)

        uwb_list = uwb_data["links"]
        # for uwb_archor in uwb_list:
        #     print(uwb_archor)

    except:
        print("Error decoding JSON:", line) # Ajout d'une instruction de débogage
    # print("Current uwb_list:", uwb_list) # Ajout d'une instruction de débogage

    return uwb_list



def uwb_range_offset(uwb_range):

    temp = uwb_range
    return temp

def write_data(f, data):
    ch = ""
    for d in range(len(data)-1):
        ch += str(d) + ";"
    ch += str(data[-1]) + "\n"
    f.write(ch)


def main():
    t0 = time.time()

    #Fichier pour sauvegarder les données
    date_str = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    f = open(f"{THIS_FOLDER}/log_long/Long_log_{date_str}.csv","w")
    # f = open(f"{THIS_FOLDER}/log_long/TO_DELETE.csv","w")
    f.write(f"Num of Anchor; Time [ms]; Data Anchor\n")
    relaunch = False
    while True:

        list = read_data()

        for one in list:

            if one["A"] == "1780":
                time_anchor1 = uwb_range_offset(float(one["T"]));
                data_anchor1 = uwb_range_offset(float(one["R"])); 
                t0 = time.time()
                f.write("1780 ; "+ str(time_anchor1) + ";"+ str(data_anchor1) + "\n")

            if one["A"] == "1781":
                time_anchor2 = uwb_range_offset(float(one["T"]));
                data_anchor2 = uwb_range_offset(float(one["R"])); 
                t0 = time.time()
                f.write("1781 ; "+ str(time_anchor2) + ";"+ str(data_anchor2) + "\n")

            if one["A"] == "1782":
                time_anchor3 = uwb_range_offset(float(one["T"]));
                data_anchor3 = uwb_range_offset(float(one["R"])); 
                t0 = time.time()
                f.write("1782 ; "+ str(time_anchor3) + ";"+ str(data_anchor3) + "\n")

            if one["A"] == "1783":
                time_anchor4 = uwb_range_offset(float(one["T"]));
                data_anchor4 = uwb_range_offset(float(one["R"])); 
                t0 = time.time()
                f.write("1783 ; "+ str(time_anchor4) + ";"+ str(data_anchor4) + "\n")
        
        if time.time() - t0 > 30:
            break

        f.flush()

if __name__ == '__main__':
    import datetime
    
    while True:
        data, addr = connect_to_tag()
        main()
        print("Relaunching..")