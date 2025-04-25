# download_xml.py
import os
import requests
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

def get_latest_data_date(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        dates = [dm.attrib["date"] for dm in root.findall(".//donneesMarche")]
        dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
        return max(dates) if dates else None
    except Exception as e:
        print(f"Erreur de parsing XML {xml_path} : {e}")
        return None

def download_xml_files(start_year=2016, end_year=None, output_dir="xml"):
    if end_year is None:
        end_year = datetime.now().year

    current_year = datetime.now().year
    yesterday = datetime.now() - timedelta(days=1)

    os.makedirs(output_dir, exist_ok=True)

    for year in range(start_year, end_year + 1):
        filename = os.path.join(output_dir, f"prix_spot_{year}.xml")
        need_download = False

        if not os.path.exists(filename):
            print(f"Fichier manquant, téléchargement nécessaire : {filename}")
            need_download = True
        elif year == current_year:
            latest_date = get_latest_data_date(filename)
            if not latest_date or latest_date < yesterday:
                print(f"Données obsolètes ({latest_date.date() if latest_date else 'inconnue'}), mise à jour nécessaire : {filename}")
                need_download = True
            else:
                print(f"À jour : {filename} (jusqu'au {latest_date.date()})")
        else:
            print(f"Fichier existant pour {year}, non mis à jour : {filename}")

        if need_download:
            dateDeb = f"01/01/{year}"
            dateFin = f"31/12/{year}"
            url = f"https://eco2mix.rte-france.com/curves/getDonneesMarche?&dateDeb={dateDeb}&dateFin={dateFin}&mode=NORM"
            response = requests.get(url)

            if response.ok:
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"Téléchargé : {filename}")
            else:
                print(f"Erreur pour l'année {year} : {response.status_code}")

if __name__ == "__main__":
    download_xml_files()
