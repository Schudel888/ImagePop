
#Imports
from astropy.io import fits 
import matplotlib
import matplotlib.pyplot as pl

def fits_to_png(name_of_fits_file, name_of_png_file):


	hdulist = fits.open(name_of_fits_file, mode='readonly', memmap=True)
	hdu = hdulist[0]
	data = hdu.data

	assert data.ndim == 2


	pl.imshow(data, cmap = matplotlib.cm.Greys_r)
	#pl.grid(True)
	pl.savefig(name_of_png_file, format='png')
 	pl.close()


	return #DONE Return Nothing



Functions = dict()
Functions['png'] = fits_to_png


