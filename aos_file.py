import struct
import json, sys, os

print("AOS archive unpacker 1.0\nAuthor: DmitrySenpai\n")

def extract_files_from_archive(archive_path):
    with open(archive_path, 'rb') as f:
        data = f.read()

    vxl_start = data.find(b'VXL\x00')
    if vxl_start == -1:
        raise ValueError("VXL file not found in the archive")

    ugc_start = data.find(b'UGC\x00', vxl_start + 4)
    if ugc_start == -1:
        raise ValueError("UGC file not found in the archive")

    vxl_data = data[vxl_start:ugc_start]

    ugc_data = data[ugc_start:]

    vxl_payload_start = 8
    vxl_payload = vxl_data[vxl_payload_start:]

    with open(os.path.splitext(archive_path)[0] + '.vxl', 'wb') as vxl_file:
        vxl_file.write(vxl_payload)

    ugc_json_start = ugc_data.find(b'{')
    if ugc_json_start == -1:
        raise ValueError("JSON data not found in UGC file")

    ugc_json_data = ugc_data[ugc_json_start:]

    with open(os.path.splitext(archive_path)[0] + '.ugc', 'wb') as ugc_json_file:
        ugc_json_file.write(ugc_json_data)

    try:
        ugc_json = json.loads(ugc_json_data.decode('utf-8'))
        with open(os.path.splitext(archive_path)[0] + '.ugc', 'w') as ugc_json_file:
            json.dump(ugc_json, ugc_json_file, indent=4)
        print("UGC JSON data extracted and saved")
    except json.JSONDecodeError as e:
        print(f"Failed to decode UGC JSON: {e}")

    print("Files extracted successfully.")

if len(sys.argv) == 1:
    print("Specify the path to the AOS file!")
    sys.exit()

if not os.path.isfile(sys.argv[1]):
    print("File not found")
    sys.exit()

extract_files_from_archive(sys.argv[1])