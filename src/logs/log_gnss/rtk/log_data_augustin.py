import numpy as np
import os
import qrunch


#Importing the data
file_path = os.path.dirname(os.path.abspath(__file__))
trames_path1 = file_path + "/chariot_rtk.nma"
trames_path2 = file_path + "/chariot_rtk_82untruc.nma"
trames_path3 = file_path + "/chariot_rtk_milieu.nma"
trames_path4 = file_path + "/chariot_rtk_rouge.nma"

# Fonction pour filtrer les lignes commençant par "$GPGGA"
def filter_lines(lines):
    filtered_lines = []
    for line in lines:
        if line.startswith("$GPGGA"):
            filtered_lines.append(line.split(","))
    return filtered_lines

# Lire les fichiers et filtrer les lignes commençant par "$GPGGA"
trames1 = np.array(filter_lines(np.genfromtxt(trames_path1, dtype='str')))
trames2 = np.array(filter_lines(np.genfromtxt(trames_path2, dtype='str')))
trames3 = np.array(filter_lines(np.genfromtxt(trames_path3, dtype='str')))
trames4 = np.array(filter_lines(np.genfromtxt(trames_path4, dtype='str')))


#Extracting NMEA data
def NMEA_data(trames):
    type_trame = trames[:, 0]
    utc = trames[:, 1]
    lat = trames[:, 2] #N
    lon = trames[:, 4] #E
    type_pos = np.float64(trames[:, 6])
    nb_sat = np.float64(trames[:, 7])
    sigma_h = np.float64(trames[:, 8])
    alt = np.float64(trames[:, 9])
    alt_geoide = np.float64(trames[:, 11])

    utc_vis = ['' for _ in range(len(utc))]
    lat_deg = ['' for _ in range(len(lat))]
    lat_dms = ['' for _ in range(len(lat))]
    lon_deg = ['' for _ in range(len(lon))]
    lon_dms = ['' for _ in range(len(lon))]

    for i in range(len(utc)):
        utc_vis[i] += utc[i][0:2] + 'h' + utc[i][2:4] + 'm' + utc[i][4:6] + '.' + utc[i][7:] + 's'
        lat_deg[i] += lat[i][0:2] + '.' + str(np.float64(lat[i][2:])/60)[2:8]
        lon_deg[i] += lon[i][0:3] + '.' + str(np.float64(lon[i][3:])/60)[2:8]
        lat_dms[i] += lat[i][0:2] + '°' + lat[i][2:4] + "'" + str(np.float64('0.' + lat[i][5:])*60)[0:4] + '"'
        lon_dms[i] += lon[i][0:3] + '°' + lon[i][3:5] + "'" + str(np.float64('0.' + lon[i][6:])*60)[0:4] + '"' 
        lat_deg[i] = np.float64(lat_deg[i])
        lon_deg[i] = np.float64(lon_deg[i])

    return(utc, lat, lon, lat_deg, lon_deg, nb_sat, sigma_h, alt, alt_geoide)

def NMEA_qrunch(trames_path):
    return(qrunch.load_gnssnmea(trames_path))

def create_kml_file(filename, coordinates):
    kml_template = """<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
        <Document>
            <Placemark>
                <name>Mean Coordinates</name>
                <Point>
                    <coordinates>{lon},{lat}</coordinates>
                </Point>
            </Placemark>
        </Document>
    </kml>
    """

    with open(filename, "w") as file:
        for coordinate in coordinates:
            lat, lon, _ = coordinate  # Ignorer l'altitude
            kml_data = kml_template.format(lat=lat, lon=lon)
            file.write(kml_data)


if __name__ == "__main__":
    #Manual method
    print("----- Saving the manual data -----")
    _, _, _, lat_deg1, lon_deg1, _, _, alt1, _ = NMEA_data(trames1)
    _, _, _, lat_deg2, lon_deg2, _, _, alt2, _ = NMEA_data(trames2)
    _, _, _, lat_deg3, lon_deg3, _, _, alt3, _ = NMEA_data(trames3)
    _, _, _, lat_deg4, lon_deg4, _, _, alt4, _ = NMEA_data(trames4)
    np.savez(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gnss_data_augustin.npz"), lat1=lat_deg1, lon1=lon_deg1, alt1=alt1, lat2=lat_deg2, lon2=lon_deg2, alt2=alt2, lat3=lat_deg3, lon3=lon_deg3, alt3=alt3, lat4=lat_deg4, lon4=lon_deg4, alt4=alt4, dtype=float)
    print("----- Data saved -----")

    import matplotlib.pyplot as plt

    # Charger le fichier .npz
    data = np.load(file_path + '/gnss_data_augustin.npz',allow_pickle=True)

    # Afficher la taille de chaque matrice
    P = {}

    for key in data.keys():
        P[key] = ''
    
    for key in data.keys():
        if key != 'dtype':
            matrix = data[key]

            #Rognage
            # matrix = matrix[matrix.shape[0]//2:]
            mask = (np.abs(matrix - np.mean(matrix)) > np.std(matrix))
            matrix_masked = matrix[~mask]

            iterations = np.arange(matrix.shape[0])
            iterations_masked = np.arange(matrix_masked.shape[0])

            # Calculer et afficher la valeur moyenne
            mean_value = np.mean(matrix_masked)
            print(f"Mean value of {key}: {mean_value}")
            print(f"{matrix_masked.shape[0]/matrix.shape[0]*100}% of values taken\n")
            P[key] = mean_value

            # Étiquettes des axes et titre du graphique
            plt.figure()
            plt.plot(iterations, matrix, label = 'data')
            plt.plot(iterations_masked, matrix_masked, label = 'data_masked')
            # plt.plot(iterations, np.abs(matrix - np.mean(matrix)), label = 'std')
            # plt.plot(iterations, -np.abs(matrix - np.mean(matrix)), label = '-std')
            plt.xlabel("Iterations")
            plt.ylabel("Matrix Value")
            plt.title(f"Graph of {key}")

    # # Afficher le graphique
    # plt.legend()
    # plt.show()

    import simplekml

    # Coordonnées moyennes avec les clés correspondantes
    mean_coordinates = {
        '0x1783': (P['lat1'], P['lon1']),
        '0x1782': (P['lat2'], P['lon2']),
        '0x1781': (P['lat3'], P['lon3']),
        '0x1780': (P['lat4'], P['lon4'])
    }

    # Créer un objet KML
    kml = simplekml.Kml()

    # Ajouter les coordonnées moyennes comme des marqueurs avec les noms de clés
    for key, coordinate in mean_coordinates.items():
        lat, lon = coordinate
        kml.newpoint(name=key, coords=[(lon, lat)])

    # Sauvegarder le fichier KML
    # kml.save(file_path + "/mean_coordinates.kml")


    import pyproj

    # Coordonnées "ex"
    alt_gnss = -0.177
    alt_uwb = -1.738
    alt_tag = -1.606
    red_b = 0.85
    offset = -(alt_uwb - alt_gnss) # // - (alt_tag - alt_gnss); //La difference d'altitude entre l'antenne GNSS et l'antenne UWB

    A1780_ex = np.array([48 + 53.99496/60, 2 + 3.88899/60, 93.01])
    A1781_ex = np.array([48 + 53.99035/60, 2 + 3.92370/60, 91.88])
    A1782_ex = np.array([48 + 54.02159/60, 2 + 3.85325/60, 91.50])
    A1783_ex = np.array([48 + 54.01516/60, 2 + 3.83476/60, 91.65])

    # Coordonnées "th"
    A1783_th = np.array([P['lat1'], P['lon1'], P['alt1']])
    A1782_th = np.array([P['lat2'], P['lon2'], P['alt2']])
    A1781_th = np.array([P['lat3'], P['lon3'], P['alt3']])
    A1780_th = np.array([P['lat4'], P['lon4'], P['alt4']])

    print("theoriques (mean):\n",A1780_th)
    print(A1781_th)
    print(A1782_th)
    print(A1783_th,"\n")

    print("une valeure (exp):\n",A1780_ex)
    print(A1781_ex)
    print(A1782_ex)
    print(A1783_ex,"\n")

    print((A1780_ex[0]-48)*60, (A1780_ex[1]-2)*60)
    print((A1781_ex[0]-48)*60, (A1781_ex[1]-2)*60)
    print((A1782_ex[0]-48)*60, (A1782_ex[1]-2)*60)
    print((A1783_ex[0]-48)*60, (A1783_ex[1]-2)*60)

    # Fonction pour convertir les coordonnées géographiques en coordonnées cartésiennes
    def geodetic_to_cartesian(lat, lon, alt):
        transformer = pyproj.Transformer.from_crs('EPSG:4326', 'EPSG:3857', always_xy=True)
        x, y, z = transformer.transform(lon, lat, alt)
        return x, y, z

    # Convertir les coordonnées "ex" en coordonnées cartésiennes
    A1780_ex_cartesian = geodetic_to_cartesian(A1780_ex[0], A1780_ex[1], A1780_ex[2])
    A1781_ex_cartesian = geodetic_to_cartesian(A1781_ex[0], A1781_ex[1], A1781_ex[2])
    A1782_ex_cartesian = geodetic_to_cartesian(A1782_ex[0], A1782_ex[1], A1782_ex[2])
    A1783_ex_cartesian = geodetic_to_cartesian(A1783_ex[0], A1783_ex[1], A1783_ex[2])

    # Convertir les coordonnées "th" en coordonnées cartésiennes
    A1780_th_cartesian = geodetic_to_cartesian(A1780_th[0], A1780_th[1], A1780_th[2])
    A1781_th_cartesian = geodetic_to_cartesian(A1781_th[0], A1781_th[1], A1781_th[2])
    A1782_th_cartesian = geodetic_to_cartesian(A1782_th[0], A1782_th[1], A1782_th[2])
    A1783_th_cartesian = geodetic_to_cartesian(A1783_th[0], A1783_th[1], A1783_th[2])

    # Calculer la norme
    diff_A1780 = np.linalg.norm(np.array(A1780_th_cartesian) - np.array(A1780_ex_cartesian))
    diff_A1781 = np.linalg.norm(np.array(A1781_th_cartesian) - np.array(A1781_ex_cartesian))
    diff_A1782 = np.linalg.norm(np.array(A1782_th_cartesian) - np.array(A1782_ex_cartesian))
    diff_A1783 = np.linalg.norm(np.array(A1783_th_cartesian) - np.array(A1783_ex_cartesian))

    print("\ndiff:")
    print(diff_A1780)
    print(diff_A1781)
    print(diff_A1782)
    print(diff_A1783)