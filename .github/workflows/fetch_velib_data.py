import requests
import pandas as pd
import json

# URLs des API Velib
info_url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json"
status_url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json"

# IDs des stations que vous souhaitez interroger
station_ids = [102722579, 66505511, 484889494, 54000555, 66491389, 378626842]  # Remplacez par les IDs des stations souhaitées

# Fonction pour récupérer les données JSON depuis une URL
def fetch_json(url):
    response = requests.get(url)
    response.raise_for_status()  # Vérifie si la requête a réussi
    return response.json()

# Fonction pour extraire les informations d'une station spécifique
def get_station_info(info_data, status_data, station_ids):
    # Convertir les données JSON en DataFrames
    info_df = pd.DataFrame(info_data['data']['stations'])
    status_df = pd.DataFrame(status_data['data']['stations'])

    # Filtrer les informations des stations
    info_stations = info_df[info_df['station_id'].isin(station_ids)]
    status_stations = status_df[status_df['station_id'].isin(station_ids)]

    # Fusionner les DataFrames sur 'station_id'
    merged_df = pd.merge(info_stations, status_stations, on='station_id')
    return merged_df

# Fonction principale pour orchestrer les étapes
def main():
    # Récupérer les données JSON des deux APIs
    info_data = fetch_json(info_url)
    status_data = fetch_json(status_url)

    # Obtenir les informations des stations spécifiées
    station_data_df = get_station_info(info_data, status_data, station_ids)
    stations_info = []
    if not station_data_df.empty:
        for _, row in station_data_df.iterrows():
            station_info = {
                "station_id": row['station_id'],
                "name": row['name'],
                "latitude": row['lat'],
                "longitude": row['lon'],
                "num_bikes_available": row['num_bikes_available'],
                "num_docks_available": row['num_docks_available'],
                "rental_methods": row.get('rental_methods', []),
                "rental_uris": row.get('rental_uris', {}),
                "is_renting": row.get('is_renting', 0),
                "is_returning": row.get('is_returning', 0),
                "is_installed": row.get('is_installed', 0)
            }
            stations_info.append(station_info)

        # Sauvegarder les informations dans un fichier JSON
        file_name = 'stations_info.json'
        with open(file_name, 'w') as json_file:
            json.dump(stations_info, json_file, indent=4)
        print(f"Les informations des stations ont été sauvegardées dans '{file_name}'")
    else:
        print(f"Aucune station trouvée avec les IDs {station_ids}")

if __name__ == "__main__":
    main()
