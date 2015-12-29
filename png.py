
#Imports
from astropy.io import fits 
import matplotlib
import matplotlib.pyplot as pl

def fits_to_png(name_of_fits_file, name_of_png_file):


	hdulist = fits.open(name_of_fits_file, mode='readonly')#, memmap=True)
	hdu = hdulist[0]
	data = hdu.data

	assert data.ndim == 2

	ACTUAL_PNG_FILENAME = name_of_png_file+'.png'


	pl.imshow(data, cmap = matplotlib.cm.Greys_r, origin='lower')
	#pl.grid(True)
	pl.savefig(ACTUAL_PNG_FILENAME, format='png', dpi=600)
 	pl.close()

 	hdulist.close()

 	with open(name_of_png_file, 'w') as placeholder:
 		placeholder.write(ACTUAL_PNG_FILENAME)

	return #DONE Return Nothing

def fits_to_contour_png(name_of_fits_file, name_of_png_file):


	hdulist = fits.open(name_of_fits_file, mode='readonly')#, memmap=True)
	hdu = hdulist[0]
	data = hdu.data

	assert data.ndim == 2

	ACTUAL_PNG_FILENAME = name_of_png_file+'.png'


	pl.contour(data, origin='lower')
	#pl.grid(True)
	pl.savefig(ACTUAL_PNG_FILENAME, format='png',dpi=600)
 	pl.close()

 	hdulist.close()

 	with open(name_of_png_file, 'w') as placeholder:
 		placeholder.write(ACTUAL_PNG_FILENAME)

	return #DONE Return Nothing

Functions = dict()
Functions['png'] = fits_to_png
Functions['png_contour'] = fits_to_contour_png


