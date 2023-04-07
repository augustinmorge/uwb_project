#!/usr/bin/python3
import time
import socket
import json
import keyboard
import numpy as np
import matplotlib.pyplot as plt
import os

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

    return data, addr, sock


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


def main(t_start):
    t0 = time.time()

    #Fichier pour sauvegarder les données
    date_str = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    f = open(f"{THIS_FOLDER}/Long_log_{date_str}.csv","w")
    # f = open(f"{THIS_FOLDER}/TO_DELETE.csv","w")
    f.write(f"Num of Anchor; Time [ms]; Data Anchor; dbm\n")
    relaunch = False
    while True:

        list = read_data()

        for one in list:

            if one["A"] == "1780":
                # time_anchor1 = time.time() - t_start # uwb_range_offset(float(one["T"]));
                time_anchor1 = uwb_range_offset(float(one["T"]));
                data_anchor1 = uwb_range_offset(float(one["R"])); 
                dbm_anchor1 = float(one["dbm"])
                t0 = time.time()
                if data_anchor1 != 0:
                    f.write("1780 ; "+ str(time_anchor1) + ";"+ str(data_anchor1) + ";" + str(dbm_anchor1) + "\n")

            if one["A"] == "1781":
                # time_anchor2 = time.time() - t_start
                time_anchor2 = uwb_range_offset(float(one["T"]));
                data_anchor2 = uwb_range_offset(float(one["R"])); 
                dbm_anchor2 = float(one["dbm"])
                t0 = time.time()
                if data_anchor2 != 0:
                    f.write("1781 ; "+ str(time_anchor2) + ";"+ str(data_anchor2) + ";" + str(dbm_anchor2) + "\n")

            if one["A"] == "1782":
                # time_anchor3 = time.time() - t_start
                time_anchor3 = uwb_range_offset(float(one["T"]));
                data_anchor3 = uwb_range_offset(float(one["R"])); 
                dbm_anchor3 = float(one["dbm"])
                t0 = time.time()
                if data_anchor3 != 0:
                    f.write("1782 ; "+ str(time_anchor3) + ";"+ str(data_anchor3) + ";" + str(dbm_anchor3) + "\n")

            if one["A"] == "1783":
                # time_anchor4 = time.time() - t_start
                time_anchor4 = uwb_range_offset(float(one["T"]));
                data_anchor4 = uwb_range_offset(float(one["R"])); 
                dbm_anchor4 = float(one["dbm"])
                t0 = time.time()
                if data_anchor4 != 0:
                    f.write("1783 ; "+ str(time_anchor4) + ";"+ str(data_anchor4) + ";" + str(dbm_anchor4) + "\n")
        
        f.flush()

        # if time.time() - t0 > 1:
        #     connect_to_tag()
        #     t0 = time.time()


if __name__ == '__main__':
    import datetime
    data, addr, sock = connect_to_tag()
    print("Connected !")
    t_start = time.time()
    main(t_start)
    sock.close()
    print("Disconnected.")