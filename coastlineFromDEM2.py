"""
from osgeo import gdal
import numpy as np

# Path to the DEM raster file
dem_path = "pathtodem/demhellas100.tif"

# Open the DEM raster
dem_dataset = gdal.Open(dem_path, gdal.GA_ReadOnly)
if dem_dataset is None:
    print("Error: Unable to open DEM raster file")
    exit()

# Read the DEM raster as a numpy array
dem_array = dem_dataset.ReadAsArray()

# Get raster dimensions
rows, cols = dem_array.shape

# Create a new array for the boundary raster
boundary_array = np.zeros((rows, cols), dtype=np.float32)  # Initialize with zeros

# Define the value to assign to boundary pixels
boundary_value = -1

# Iterate through each pixel in the DEM array
for row in range(1, rows - 1):
    for col in range(1, cols - 1):
        # Check if the current pixel is 0
        if dem_array[row, col] == 0:
            continue  # Skip 0 valued pixels
        # Check if any neighboring pixel is 0
        if (dem_array[row - 1, col] == 0 or
                dem_array[row + 1, col] == 0 or
                dem_array[row, col - 1] == 0 or
                dem_array[row, col + 1] == 0):
            boundary_array[row, col] = boundary_value

# Create a new raster with the boundary array
output_path = "outputpath/aktogrammi100.tif"
driver = gdal.GetDriverByName("GTiff")
output_dataset = driver.Create(output_path, cols, rows, 1, gdal.GDT_Float32)
output_dataset.SetGeoTransform(dem_dataset.GetGeoTransform())
output_dataset.SetProjection(dem_dataset.GetProjection())
output_band = output_dataset.GetRasterBand(1)
output_band.WriteArray(boundary_array)

# Close the datasets
output_band = None
output_dataset = None
dem_dataset = None

print("Boundary raster created and saved to:", output_path)
"""

from osgeo import gdal
import numpy as np

# Path to the DEM raster file
dem_path = "pathtodem/demhellas100.tif"

# Open the DEM raster
dem_dataset = gdal.Open(dem_path, gdal.GA_ReadOnly)
if dem_dataset is None:
    print("Error: Unable to open DEM raster file")
    exit()

# Read the DEM raster as a numpy array
dem_array = dem_dataset.ReadAsArray()

# Get raster dimensions
rows, cols = dem_array.shape

# Create a new array for the boundary raster
boundary_array = np.full((rows, cols), -9999, dtype=np.float32)  # Initialize with NoData value

# Define the value to assign to boundary pixels
boundary_value = -1

# Iterate through each pixel in the DEM array
for row in range(1, rows - 1):
    for col in range(1, cols - 1):
        # Check if the current pixel is 0
        if dem_array[row, col] == 0:
            continue  # Skip 0 valued pixels
        # Check if any neighboring pixel is 0
        if (dem_array[row - 1, col] == 0 or
                dem_array[row + 1, col] == 0 or
                dem_array[row, col - 1] == 0 or
                dem_array[row, col + 1] == 0):
            boundary_array[row, col] = boundary_value

# Create a new raster with the boundary array
output_path = "outputpath/aktogrammi100.tif"
driver = gdal.GetDriverByName("GTiff")
output_dataset = driver.Create(output_path, cols, rows, 1, gdal.GDT_Float32)
output_dataset.SetGeoTransform(dem_dataset.GetGeoTransform())
output_dataset.SetProjection(dem_dataset.GetProjection())
output_band = output_dataset.GetRasterBand(1)
output_band.WriteArray(boundary_array)

# Set NoData value for the output raster
output_band.SetNoDataValue(-9999)

# Close the datasets
output_band = None
output_dataset = None
dem_dataset = None

print("Boundary raster created and saved to:", output_path)
