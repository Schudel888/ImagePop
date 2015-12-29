#Imports
from __future__ import division
from astropy.io import fits
from scipy import ndimage as snd
import warnings
import numpy as np

def min_max_mean(arr):
	return np.min(arr),np.max(arr),np.mean(arr)

def norm(arr):
	arr_min, arr_max, arr_mean = min_max_mean(arr)
	return np.divide(np.subtract(arr, arr_min), (arr_max-arr_min))

def min_max_mean_norm(arr):
	arr_min, arr_max, arr_mean = min_max_mean(arr)
	return arr_min, arr_max, arr_mean, ((arr-arr_min)/(arr_max-arr_min))

def gaussian_c0(arr,sigma=1):
	return snd.filters.gaussian_filter(arr, sigma=sigma,mode='constant',cval=0.0)
'''
def c_me(arr, alt=None):
	if arr.ndim == 2:
		if alt ==None:
			plt.contour(arr) 
		else:
			plt.imshow(arr)
	elif arr.ndim == 1:
		plt.plot(arr) #plt.hist(arr)
	else:
		return
	plt.show()
	plt.cla()
	plt.clf()
	plt.close()
'''

def pipeline(arr, dnorm=True, snorm=True, sigma=1, mode='mult'):
	ALLOWED_MODES = dict()
	ALLOWED_MODES['linear']=lambda a,b:a+b
	ALLOWED_MODES['hypot']=lambda a,b:np.hypot(a,b)
	ALLOWED_MODES['mult']=lambda a,b:a*b
	ALLOWED_MODES['gauss']=lambda a,b:gaussian_c0(a*b)
	
	d_min,d_max,d_mean,d_norm = min_max_mean_norm(arr)

	#ALL Gaussian-ing must be done ONLY to d_norm
	s = gaussian_c0(d_norm, sigma=sigma)
	s_min,s_max,s_mean,s_norm = min_max_mean_norm(s)

	if dnorm: 
		D=d_norm
	else:
		D=arr

	if snorm:
		S=s_norm
	else:
		S=s
			
	indices = np.where(S==0)
	S[indices]=1
	D[indices]=0
	A = norm(D/S)
	A_gau = norm(gaussian_c0(A))
	return norm(ALLOWED_MODES[mode](A,A_gau))

def circle(r=2):
	r=int(r)
	assert r>0
	d = 2*r+1
	return np.hypot(*(r-np.indices((d,d))))<=(r+0.1) #TODO Fudge

def max_selector(norm_image, res=4, MAX=100):
	#norm_image is a 2D array with values in the range [0,1]
	#resolution is the distance two point sources must be away from eachother to be separated
	assert norm_image.ndim == 2
	norm_image=np.copy(norm_image) #don't mess with originals
	
	waterline = np.mean(norm_image)
	norm_image[:res][:].fill(waterline) #zero out 'frame'
	norm_image[-res:][:].fill(waterline)
	norm_image[:][:res].fill(waterline)
	norm_image[:][-res:].fill(waterline)
	cutout=circle(res)
	point_list = []
	while np.max(norm_image)>waterline and len(point_list)<MAX:
		xy = norm_image.argmax()
		y = int(xy/norm_image.shape[1])
		x = int(xy%norm_image.shape[1])
		#TODO SHOULD THIS BE SHAPE 0 or 1? 
		#print xy, x, y
		point_list.append((x,y))
		norm_image[y-res:y+res+1,x-res:x+res+1][cutout]=waterline
	return point_list

def list_to_table(list_of_tuples, col_dtypes):
	#TODO
	columns = np.rec.array(list_of_tuples, dtype=col_dtypes)

	return fits.TableHDU.from_columns(columns, header=None) #TODO ~~~~~~~~~~~~~~~~~~~~~~~~~   ~~~~~~~~~~~~~~~~~~~

#Begin<Starfind>
def starfind(input_filename, output_filename):

	def REAL_DEAL(image):	
		primary = np.copy(image)	
		processed_image = pipeline(primary, dnorm=True, snorm=True, sigma=1, mode='gauss')
		
		primary[processed_image<=0.1].fill(0.0) #TODO Fudge
		master = image*processed_image
		return fits.HDUList(fits.PrimaryHDU(master))
		
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")	

		input_hdulist = fits.open(input_filename, mode='readonly')#, memmap=True)
		input_hdu = input_hdulist[0]
		input_data = input_hdu.data
					
		output_hdulist = REAL_DEAL(input_data)
		#TODO ~~ ~ ~ ~ ~ ~~  ~~ ~~  ~ ~~ ~~  ~  ~  ~ ~ ~ ~ ~ ~  ~~ ~ ~ ~ ~~  ~ ~  ~~  ~~ ~ ~ ~  ~ ~ ~~  ~~ ~ ~ ~~ ~  ~ ~~ ~  ~
		output_hdulist.append( list_to_table( max_selector( norm(input_data), res=4, MAX=100), [('x', 'i4'),('y', 'i4')]))

		output_hdulist.writeto(output_filename, clobber=True)

		input_hdulist.close()
		output_hdulist.close()
	
	return #DONE Return Nothing

#End<Starfind>

Functions =dict()
Functions['sf']=starfind
#Functions['starfind']=starfind
