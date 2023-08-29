import os
import numpy as np
import matplotlib.pyplot as plt

def display_offsets(file_path):
    data = np.genfromtxt(file_path, delimiter=';', skip_header=1, dtype=str)

    dates = data[:, 0]
    
    for i in range(dates.shape[0]):
        dates[i] = dates[i][:10]
        
    thresholds = data[:, 1].astype(float)
    anchors = np.arange(1780, 1784)
    offsets = data[:, 2:].astype(float)

    unique_thresholds = np.unique(thresholds)

    # Création d'une liste de tuples (date, données)
    date_data_pairs = list(zip(dates, thresholds, offsets))

    # Tri des données par date (du plus ancien au plus récent)
    date_data_pairs.sort(key=lambda x: (x[0][-4:], x[0][3:5], x[0][:2]))

    for threshold in unique_thresholds:
        plt.figure(figsize=(10, 6))
        for i, anchor in enumerate(anchors):
            mask = (thresholds == threshold)
            data_subset = np.array([data for (date, _, data) in date_data_pairs if date in dates[mask]])
            plt.plot([date for (date, _, _) in date_data_pairs if date in dates[mask]], data_subset[:, i], 'o-', label=f"Anchor {anchor}")

        plt.xlabel("Date")
        plt.ylabel("Offset [cm]")
        plt.title(f"Evolution des Offsets d'ancres (pas: {threshold} cm)")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, "offset.txt")
    display_offsets(file_path)
    