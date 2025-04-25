# convert_xml_to_csv.py
import os
import csv
import xml.etree.ElementTree as ET
from collections import defaultdict

def convert_xml_to_csv(xml_dir="xml", csv_dir="csv"):
    os.makedirs(csv_dir, exist_ok=True)

    for file in os.listdir(xml_dir):
        if not file.endswith(".xml"):
            continue

        year = file.split("_")[-1].replace(".xml", "")
        xml_path = os.path.join(xml_dir, file)
        csv_path = os.path.join(csv_dir, f"prix_spot_{year}.csv")

        tree = ET.parse(xml_path)
        root = tree.getroot()

        data_by_date_hour = defaultdict(lambda: defaultdict(lambda: None))
        countries = set()

        for donnees in root.findall(".//donneesMarche"):
            date = donnees.attrib["date"]
            for type_ in donnees.findall("type"):
                pays = type_.attrib["perimetre"]
                countries.add(pays)
                for valeur in type_.findall("valeur"):
                    heure = int(valeur.attrib["periode"])
                    prix = valeur.text
                    data_by_date_hour[(date, heure)][pays] = prix

        countries = sorted(countries)
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "heure"] + countries)

            for (date, heure) in sorted(data_by_date_hour):
                row = [date, heure]
                for pays in countries:
                    row.append(data_by_date_hour[(date, heure)].get(pays))
                writer.writerow(row)

        print(f"Fichier CSV généré : {csv_path}")

if __name__ == "__main__":
    convert_xml_to_csv()
