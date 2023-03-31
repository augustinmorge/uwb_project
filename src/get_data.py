#!/usr/bin/python3
import time
import socket
import json
import os

# Add the threading module
import threading

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

def read_data(data):
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

class Anchor:
    def __init__(self):
        self.anchors = {}
        self.lock = threading.Lock() # Create a lock object
    
    def update_anchor(self, id, time, range):
        with self.lock: # Acquire the lock before accessing the dictionary
            self.anchors[id] = {'Time':time, 'Range':range}

def main(anchors, data):
    t0 = time.time()

    while True:

        list = read_data(data)

        for one in list:

            if one["A"] == "1780":
                time_anchor1 = uwb_range_offset(float(one["T"]));
                data_anchor1 = uwb_range_offset(float(one["R"]));
                anchors.update_anchor(1780, time_anchor1, data_anchor1)

            if one["A"] == "1781":
                time_anchor2 = uwb_range_offset(float(one["T"]));
                data_anchor2 = uwb_range_offset(float(one["R"]));
                anchors.update_anchor(1781, time_anchor2, data_anchor2)

            if one["A"] == "1782":
                time_anchor3 = uwb_range_offset(float(one["T"]));
                data_anchor3 = uwb_range_offset(float(one["R"]));
                anchors.update_anchor(1782, time_anchor3, data_anchor3)

            if one["A"] == "1783":
                time_anchor4 = uwb_range_offset(float(one["T"]));
                data_anchor4 = uwb_range_offset(float(one["R"]));
                anchors.update_anchor(1783, time_anchor4, data_anchor4)


anchors = Anchor()
data, addr = connect_to_tag()

# Create a thread that runs the main function
main_thread = threading.Thread(target=main, args=(anchors,data,))

# Start the thread
main_thread.start()
