# merge_csv_files.py
import os
import csv

def merge_csv_files(csv_dir="csv", output_file="prix_spot_complet.csv"):
    files = [f for f in os.listdir(csv_dir) if f.endswith(".csv")]
    files.sort()

    header_written = False
    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        writer = None
        for file in files:
            with open(os.path.join(csv_dir, file), newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader)
                if not header_written:
                    writer = csv.writer(outfile, delimiter=";")
                    writer.writerow(header)
                    header_written = True
                for row in reader:
                    # Remplacer les points décimaux par des virgules dans les valeurs numériques
                    new_row = []
                    for value in row:
                        if value is None or value == '':
                            new_row.append('')
                        else:
                            try:
                                float_val = float(value)
                                value = f"{float_val:.2f}".replace('.', ',')
                            except ValueError:
                                pass  # Ne pas modifier les champs non numériques
                            new_row.append(value)
                    writer.writerow(new_row)

    print(f"Fichier fusionné avec ; et , : {output_file}")

if __name__ == "__main__":
    merge_csv_files()
