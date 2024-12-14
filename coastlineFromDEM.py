from osgeo import gdal
import numpy as np

dem_path = "pathtodem\\dem.tif"
dem_dataset = gdal.Open(dem_path, gdal.GA_ReadOnly)
if dem_dataset is None:
    print("Error: Unable to open DEM raster file")
    exit()
dem_array = dem_dataset.ReadAsArray()
rows, cols = dem_array.shape
boundary_array = np.copy(dem_array)
boundary_value = -1
for row in range(rows):
    for col in range(cols):
        if dem_array[row, col] == dem_dataset.GetRasterBand(1).GetNoDataValue():
            continue 
        if (row == 0 or row == rows - 1 or col == 0 or col == cols - 1):
            boundary_array[row, col] = boundary_value
        else:
            is_edge_pixel = False
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if dem_array[row + i, col + j] == dem_dataset.GetRasterBand(1).GetNoDataValue():
                        is_edge_pixel = True
                        break
                if is_edge_pixel:
                    break
            if is_edge_pixel:
                boundary_array[row, col] = boundary_value
output_path = "outputpath\\aktogrammi.tif"
driver = gdal.GetDriverByName("GTiff")
output_dataset = driver.Create(output_path, cols, rows, 1, gdal.GDT_Float32)
output_dataset.SetGeoTransform(dem_dataset.GetGeoTransform())
output_dataset.SetProjection(dem_dataset.GetProjection())
output_band = output_dataset.GetRasterBand(1)
output_band.WriteArray(boundary_array)
output_band = None
output_dataset = None
dem_dataset = None

print("Boundary raster created and saved to:", output_path)
