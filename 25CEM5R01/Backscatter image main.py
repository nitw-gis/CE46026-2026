conda --version
conda create -n nisar_env python=3.10
conda activate nisar_env
pip install numpy
pip install matplotlib
pip install rasterio
pip install h5py
python nisar_processing.py
conda install gdal -c conda-forge
pip install polsartools
import polsartools as pst
def main():
	infile = r"D:\NISAR_L2_PR_GSLC_010_165_D_100_2005_DHDH_M_20260120T155930_20260120T155950_X05010_N_P_J_001.h5"
	pst.import_nisar_gslc(infile,azlks=20,rglks=10,mat='T3')
if __name__ == '__main__':
	main()
