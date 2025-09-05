import os
import glob

# Search for GDAL DLL files
search_paths = [
    r'C:\OSGeo4W64\bin\gdal*.dll',
    r'C:\OSGeo4W\bin\gdal*.dll', 
    r'C:\Program Files\GDAL\gdal*.dll',
    r'C:\Program Files\PostgreSQL\*\bin\gdal*.dll',
    r'C:\*.dll'
]

print("Searching for GDAL libraries...")
for pattern in search_paths:
    files = glob.glob(pattern)
    if files:
        print(f"Found GDAL at: {files[0]}")
        break
else:
    print("GDAL not found in common locations")
    print("Please search for 'gdal*.dll' manually")