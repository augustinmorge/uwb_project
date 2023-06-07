import numpy as np
import os
import qrunch


#Importing the data
file_path = os.path.dirname(os.path.abspath(__file__))
trames_path1 = file_path + "\poto1.nma"
trames_path2 = file_path + "\poto2.nma"
trames_path3 = file_path + "\poto3.nma"
trames_path4 = file_path + "\poto4.nma"

trames1 = np.genfromtxt(trames_path1, delimiter = ',', dtype = 'str', skip_footer = 3)
trames2 = np.genfromtxt(trames_path2, delimiter = ',', dtype = 'str', skip_footer = 3)
trames3 = np.genfromtxt(trames_path3, delimiter = ',', dtype = 'str', skip_footer = 3)
trames4 = np.genfromtxt(trames_path4, delimiter = ',', dtype = 'str', skip_footer = 3)


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
    for key in data.keys():
        if key != 'dtype':
            matrix = data[key]

            #Rognage
            matrix = matrix[matrix.shape[0]//2:]

            iterations = np.arange(matrix.shape[0])

            # Calculer et afficher la valeur moyenne
            mean_value = np.mean(matrix)
            print(f"Mean value of {key}: {mean_value}")

            # Étiquettes des axes et titre du graphique
            plt.figure()
            plt.plot(iterations, matrix)
            plt.xlabel("Iterations")
            plt.ylabel("Matrix Value")
            plt.title(f"Graph of {key}")

    # Afficher le graphique
    plt.show()

    import simplekml

    # Coordonnées moyennes avec les clés correspondantes
    mean_coordinates = {
        'poteau_1': (48.899990591549304, 2.0646127605633806),
        'poteau_2': (48.900155000000005, 2.064709795555555),
        'poteau_3': (48.90029975517242, 2.0642782655172414),
        'poteau_4': (48.900285720763726, 2.063957785202864)
    }

    # Créer un objet KML
    kml = simplekml.Kml()

    # Ajouter les coordonnées moyennes comme des marqueurs avec les noms de clés
    for key, coordinate in mean_coordinates.items():
        lat, lon = coordinate
        kml.newpoint(name=key, coords=[(lon, lat)])

    # Sauvegarder le fichier KML
    kml.save(file_path + "/mean_coordinates.kml")