# run_all.py
import download_xml
import convert_xml_to_csv
import merge_csv_files

if __name__ == "__main__":
    download_xml.download_xml_files()
    convert_xml_to_csv.convert_xml_to_csv()
    merge_csv_files.merge_csv_files()
