#!/usr/bin/python3
import time
import socket
import json
import os

# Add the threading module
import threading
mutex = threading.Lock()

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
    
    def update_anchor(self, id, time, range, coords):
        with self.lock: # Acquire the lock before accessing the dictionary
            mutex.acquire()
            self.anchors[id] = {'Time':time, 'Range': range, 'Coords': coords}
            mutex.release()

tot = 0
m_data = 0
def get_data(anchors, data):
    global m_data, tot
    while True:
        read_data(data)

if __name__ == "__main__":
    # Start the threads
    anchors = Anchor()
    
    data, addr = connect_to_tag()

    # # Create a thread that runs the get_data function
    # get_data_thread = lambda : get_data(anchors, data)
    # t_get_data = threading.Thread(target=get_data)

    # # Start the thread
    # t_get_data.start()

    # Create a thread that runs the get_data function
    get_data_thread = threading.Thread(target=get_data, args=(anchors,data,))

    # Start the thread
    get_data_thread.start()