#<BEGIN: Constants>
VERSION = 'Alpha'
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
ImagePopHistory.csv (Table of Time Stamps generated into target directory)

#Executables
impop (#TODO alias) ==> python ImagePop.py

#Credits
Sol & Lowell
'''
#<END: Constants>


#<BEGIN: Imports>
import sys
import os
import collections
#<END: Imports>


#<BEGIN: Error Handling>
with open(README_FILENAME, 'w') as readme:
	#Ensures there is always an up-to-date readme available in the runtime directory
	readme.write(README)
	readme.flush()
	readme.truncate()
	
def help_display(x=None):
	print '<ImagePop.py help_display Function>' #TODO
	#print README #TODO
	print "<python ImagePop.py [mode] target_directory [args]>"
	#TODO
	if x is not None:
		print repr(x)
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
			if os.path.isfile(init_path):
				return True
				'''
				with open(init_path, 'r') as init_path_open:
					#TODO End of line char ??
					return init_path_open.read(len(VERSION)) == VERSION
				'''
	except Exception:
		return False
	finally:
		pass
	return False

def our_init(target_directory, x=DEFAULT_INIT_ARGS):
	if not is_initialized(target_directory):
		init_path = os.path.join(target_directory, INIT_FILENAME)
		with open(init_path, 'w') as init_path_open:
			init_path_open.write(VERSION)
			init_path_open.flush()
			init_path_open.truncate()

	check(is_initialized(target_directory))
	print 'Initialization of', target_directory, 'is complete!'
#<END: Initialization>


#<BEGIN: Run>
DEFAULT_RUN_ARGS = []

def our_run(target, x=DEFAULT_RUN_ARGS):
	try:
		import ImagePopLib as lib
	except Exception:
		#TODO Generate ImagePopLib.py 
		help_display('ImagePopLib.py not imported properly!')

	if not is_initialized(target):
		#TODO ask user about this?
		our_init(target)

	if len(x): #TODO Prevents empty calls to lib.run
		lib.run(target, x)
		#Should keep running until halting conditions are met

#<END: Run>


#<BEGIN: Other?>
#TODO
#<END: Other?>


#<BEGIN: Main>

#modes = dict()
modes = collections.defaultdict(lambda whatever: help_display)
modes['init'] = our_init
modes['run'] = our_run	

check(sys.argv[1] in modes)
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

	target= None
	target_args = ['i', '-i', '--i', 'input', '-input', '--input']
	x.reverse()
	if len(x):
		target = x.pop()
	y = list()

	while len(x):
		a = x.pop()
		if a in target_args:
			old_target = target
			try:
				target = x.pop()
				y.append(old_target)
			except Exception:
				target = old_target
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
MODE = modes[sys.argv[1]]
if MODE != help_display:
	MODE(*designate_target(our_args))
else:
	MODE()
#modes[sys.argv[1]](None)
#<END: Main>

sys.exit(0)
