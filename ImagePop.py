#<BEGIN: Constants>
VERSION = 0.01
README_FILENAME = 'ImagePopReadme.txt'
INIT_FILENAME = 'ImagePopInit.txt'

README = '''
#Usage
#TODO


#Version '''+str(VERSION)+'''

#Python (Supplied)
ImagePop.py (Must be in PATH)
ImagePopLib.py (Must be in PATH #TODO->Generating?)

#Python (Generated)
ImagePopConfig.py (Will be generated into runtime directory, if not user made)
'''+INIT_FILENAME+''' (Will be generated into target directory, if not already)

#Python (User Made)
ImagePopConfig.py (Can be supplied in the runtime directory)
UserLib1.py;UserLib2.py;etc.py (Can be linked via EXTERNAL_SOURCES in ImagePopConfig.py)

#Text (Generated)
'''+README_FILENAME+''' (Will be generated into runtime directory)
ImagePopIndex.txt (Ordered File List generated into target directory)
ImagePopOperations.txt (Ordered Command List generated into target directory)
ImagePopTable.npy (Table of Time Stamps generated into target directory)

#Executables
impop (#TODO aliasing)

#Credits
Sol & Lowell
'''
#<END: Constants>


#<BEGIN: Imports>
import sys
import os
#<END: Imports>


#<BEGIN: Error Handling>
with open(README_FILENAME, 'w') as readme:
	readme.write(README)
	readme.flush()
	readme.truncate() #Truncates to current location #TODO?
	
def help_display(x=None):
	print 'ImagePop.py: help_display()' #TODO
	print README #TODO
	#print "IMAGE_POP.PY USAGE: \npython image_pop.py [flags] [functions]"
	#print "example_user@input_directory:python image_pop.py -i input_directory -o output_directory g1 g2 so1 so2"
	sys.exit(1) #Safe Helpful Exit

def check(xbool):
	if not xbool:
		help_display()

check(__name__ == "__main__")
check(len(sys.argv) > 1)
#<END: Error Handling>


#<BEGIN: Initialization>
DEFAULT_INIT_ARGS=[]

def is_initialized(target_directory):
	try:
		if isinstance(target_directory, str) and isinstance(INIT_FILENAME, str):
			init_path = os.path.join(target_directory, INIT_FILENAME)
			if os.path.is_file(init_path):
				with open(init_path, 'r') as init_path_open:
					#TODO End of line char ??
					return float(init_path_open.readline()) == VERSION
	except Exception:
		return False
	return False

def our_init(target_directory, x=DEFAULT_INIT_ARGS):
	if not is_initialized(target_directory):
		init_path = os.path.join(target_directory, INIT_FILENAME)
		with open(init_path, 'w') as init_path_open:
			init_path_open.write(str(VERSION))
			init_path_open.flush()
			init_path_open.truncate()

	check(is_initialized(target_directory))
	print 'Initialization of', target_directoy, 'is complete!'
#<END: Initialization>


#<BEGIN: Run>
DEFAULT_RUN_ARGS = []

def our_run(target, x=DEFAULT_RUN_ARGS):
	try:
		import ImagePopLib as lib
	except Exception:
		#TODO Generate ImagePopLib.py 
		help_display()

	if not is_initialized(target):
		#TODO ask user about this?
		our_init(target)

	lib.run(target, x)
	#Should keep running until halting conditions are met

#<END: Run>


#<BEGIN: Other?>
#TODO
#<END: Other?>


#<BEGIN: Main>

modes = dict()
modes['init'] = our_init
modes['run'] = our_run	
modes['h'] = help_display
modes['-h'] = help_display
modes['--h'] = help_display
modes['help'] = help_display
modes['-help'] = help_display
modes['--help'] = help_display

check(sys.argv[1] in modes)
'''
our_args = []
if len(sys.argv) > 2:
'''
our_args = sys.argv[2:]	

def designate_target(x):
	def verify_target(directory):
		if directory is None:
			#TODO
			return False
		check(isinstance(directory, str))
		if os.path.isdir(directory):
			if is_initialized(directory):
				print 'This directory has already been initialized for ImagePop functions!'
			print 'Use this directory?: '+directory
			confirm = raw_input('Enter to confirm, or type a new path: ')
			if not len(confirm):
				return True
			else:
				return verify_target(confirm)
		else:
			return False

	target_args = ['i', '-i', '--i', 'input', '-input', '--input']
	target = None
	x.reverse()
	y = list()

	while len(x):
		a = x.pop()
		if a in target_args:
			try:
				target = x.pop()
			except Exception:
				target = None
		else:
			y.append(a)
	x = y
	if verify_target(target):
		return target, x
	else:
		gotcwd = os.getcwd()
		check(verify_target(gotcwd))
		return gotcwd, x
	
#TODO->Better handle empty our_args
modes[sys.argv[1]](*designate_target(our_args))
#modes[sys.argv[1]](None)
#<END: Main>

sys.exit(0)
