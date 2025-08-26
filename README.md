# Digital-Forensics--Metadata-tool
A lightweight digital forensics tool to extract, analyze, and organize metadata  from images, PDFs, and Word documents. Generates structured CSV/Excel reports  and interactive maps for GPS-tagged files.
## 🚀 Features
- Extract EXIF metadata from images (camera model, GPS, timestamp)
- Extract metadata from PDFs (author, title, producer)
- Extract metadata from DOCX files (author, created/modified dates)
- Save results in a clean **CSV report**
- Generate an interactive **HTML map** if GPS data is present

---

## 📂 Example Output
=== File Information ===
File Name,File Path,File Type,File Size (KB),Last Modified
test.jpg,/Users/.../test.jpg,.jpg,521.3,2025-01-21 11:23:10

=== Core Metadata ===
Author,Title,Created,Modified,Camera Model,DateTime,GPS Latitude,GPS Longitude
, , , ,iPhone 12,2025:08:26 10:32:44,12.9716,77.5946

=== Additional Metadata ===
Tag,Value
ExifImageWidth,3024
ExifImageLength,4032


---

## ⚙️ Installation
```bash
git clone https://github.com/YOUR_USERNAME/digital-forensics-metadata-tool.git
cd digital-forensics-metadata-tool
pip install -r requirements.txt
