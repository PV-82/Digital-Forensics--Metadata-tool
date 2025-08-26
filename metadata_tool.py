import os
import exifread
import PyPDF2
import docx
import pandas as pd
import folium
from datetime import datetime


# ---------------------------
# Metadata Extraction Functions
# ---------------------------

def extract_image_metadata(filepath):
    metadata = {}
    with open(filepath, 'rb') as f:
        tags = exifread.process_file(f, details=False)  # details=False keeps output smaller
        for tag, value in tags.items():
            # Convert to clean string and avoid long binary dumps
            val = str(value)
            if len(val) > 120:
                val = val[:120] + "…"
            metadata[tag] = val

        # Extract GPS if available
        if "GPS GPSLatitude" in tags and "GPS GPSLongitude" in tags:
            lat = convert_to_degrees(tags["GPS GPSLatitude"].values)
            lon = convert_to_degrees(tags["GPS GPSLongitude"].values)
            metadata["GPS Latitude"] = lat
            metadata["GPS Longitude"] = lon
        if "Image Model" in tags:
            metadata["Camera Model"] = str(tags["Image Model"])
        if "EXIF DateTimeOriginal" in tags:
            metadata["DateTime"] = str(tags["EXIF DateTimeOriginal"])
    return metadata


def convert_to_degrees(value):
    """Helper to convert EXIF GPS coordinates to degrees"""
    d = float(value[0].num) / float(value[0].den)
    m = float(value[1].num) / float(value[1].den)
    s = float(value[2].num) / float(value[2].den)
    return d + (m / 60.0) + (s / 3600.0)


def extract_pdf_metadata(filepath):
    metadata = {}
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        if reader.metadata:
            for key, value in reader.metadata.items():
                metadata[key.strip("/")] = str(value)
    return metadata


def extract_docx_metadata(filepath):
    metadata = {}
    doc = docx.Document(filepath)
    props = doc.core_properties
    metadata["Author"] = props.author
    metadata["Last Modified By"] = props.last_modified_by
    metadata["Created"] = str(props.created)
    metadata["Modified"] = str(props.modified)
    metadata["Title"] = props.title
    return metadata


# ---------------------------
# Organized Report Function
# ---------------------------

def save_report(metadata, filepath, output_csv="metadata_report.csv"):
    # Get basic file info
    file_info = {
        "File Name": os.path.basename(filepath),
        "File Path": os.path.abspath(filepath),
        "File Type": os.path.splitext(filepath)[-1],
        "File Size (KB)": round(os.path.getsize(filepath) / 1024, 2),
        "Last Modified": datetime.fromtimestamp(os.path.getmtime(filepath))
    }

    # Core metadata fields to highlight
    core_keys = [
        "Author", "Last Modified By", "Created", "Modified",
        "Producer", "Creator", "Title", "Camera Model",
        "DateTime", "GPS Latitude", "GPS Longitude"
    ]

    # Prepare structured dict
    core_data = {k: metadata.get(k, "") for k in core_keys}

    # Extras: anything not in core_keys
    extras = {k: v for k, v in metadata.items() if k not in core_keys}

    # Build dataframes
    df_file = pd.DataFrame([file_info])
    df_core = pd.DataFrame([core_data])
    df_extras = pd.DataFrame(list(extras.items()), columns=["Tag", "Value"])

    # Save nicely structured CSV
    with open(output_csv, "w", encoding="utf-8") as f:
        f.write("=== File Information ===\n")
    df_file.to_csv(output_csv, mode="a", index=False)
    with open(output_csv, "a", encoding="utf-8") as f:
        f.write("\n=== Core Metadata ===\n")
    df_core.to_csv(output_csv, mode="a", index=False)
    with open(output_csv, "a", encoding="utf-8") as f:
        f.write("\n=== Additional Metadata ===\n")
    df_extras.to_csv(output_csv, mode="a", index=False)

    print(f"[+] Organized metadata saved to {output_csv}")


# ---------------------------
# Map Generator
# ---------------------------

def generate_map(metadata, output_html="metadata_map.html"):
    if "GPS Latitude" in metadata and "GPS Longitude" in metadata:
        lat, lon = metadata["GPS Latitude"], metadata["GPS Longitude"]
        map_obj = folium.Map(location=[lat, lon], zoom_start=15)
        folium.Marker([lat, lon], popup="Image Location").add_to(map_obj)
        map_obj.save(output_html)
        print(f"[+] Map saved to {output_html}")


# ---------------------------
# Main Function
# ---------------------------

def extract_metadata(filepath):
    ext = os.path.splitext(filepath)[-1].lower()
    if ext in [".jpg", ".jpeg", ".png", ".tiff"]:
        return extract_image_metadata(filepath)
    elif ext == ".pdf":
        return extract_pdf_metadata(filepath)
    elif ext == ".docx":
        return extract_docx_metadata(filepath)
    else:
        return {"Error": "Unsupported file type"}


if __name__ == "__main__":
    filepath = input("Enter file path: ").strip()
    metadata = extract_metadata(filepath)

    print("\n[+] Extracted Metadata:")
    for k, v in metadata.items():
        print(f"{k}: {v}")

    save_report(metadata, filepath)
    generate_map(metadata)
