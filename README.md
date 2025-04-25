Utilisation : 

 1 - télécharger les fichiers des données de marché depuis 2016 (format xml) dans le dossier xml (si déja existant : pas de téléchargement, si mise à jour nécessaire pour l'année en cours : téléchargement à nouveau)
python download_xml.py

 2 - convertir les fichiers xml en csv et les déplacer dans le dossier csv
python convert_xml_to_csv.py

 3 - assembler les csv ensemble dnas le fichier prix_spot_complet.csv
python merge_csv_files.py

 1, 2 et 3
python run_all.py

