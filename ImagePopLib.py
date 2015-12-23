#This is intended to be a library file for Sol and Lowell's ImagePop.py program.

#<BEGIN: Imports>
import sys
import os
import time
import imp
import csv
import numpy as np
#<END: Imports>


#<BEGIN: Error Handling>
def PRINT_ERR(x=None):
	if x is None:
		x = 'Generic'
	sys.stderr.write('\nError: '+repr(x)+'\n')
	return x

def hard_check(boolean, extra=None):
	assert boolean, PRINT_ERR(extra) #Harsh
	return boolean	#Can't return anything but True

def check(boolean, extra=None):
        if not boolean: 
		PRINT_ERR(extra)
	return boolean #Gentle

def is_str(x):
	return isinstance(x, str)

def is_filename(x):
	return is_str(x) and os.path.isfile(x)

def is_directory(x):
	return is_str(x) and os.path.isdir(x)

#<END: Error Handling>


#<BEGIN: Default Lib>
SOURCES = dict()

def DEMO(input_filepath, output_filepath, *args):
	with open(input_filepath, 'w') as temp:
		temp.write()
		temp.flush()
		temp.truncate()	



#<END: Default Lib>


#<BEGIN: Custom Config File>
CONFIG_LITERAL = '''
##Human Modifiable Portion of ImagePop.py's Config File
##Modify Carefully 

LOCK = '.ImagePopLock'

SEAL = '#Created by ImagePopLib.py... MODIFY AT YOUR OWN RISK!'

FILE_LIST_NAME = 'ImagePopIndex.txt'
OPERATION_LIST_NAME = 'ImagePopOperations.txt'
HISTORY_TABLE_NAME = 'ImagePopHistory.csv'

EXTERNAL_SOURCES = 'png.py' #None #myImagePopLib.py;lib2.py;etc.py 
#Must Each Expose Dict Called: Functions, or be None

WAIT_INTERVAL = 300 #seconds #Int Only!
#Duration to wait before checking files

STD_ERR = None #myImagePopErr.txt
#Allows superusers to rerout messages to log files

CLOBBER = True #False
#Allows files of the same name to be silently overwritten

#Robot Only Config File
#DO NOT MODIFY
ROBOT_FRIENDLY = True

'''
try:
	import ImagePopConfig as config
except Exception:
	PRINT_ERR('ImagePopConfig.py not found in current directory...')
	#TODO Find User Config?
	PRINT_ERR('Attempting to create default ImagePopConfig.py file in current directory...')
	with open("ImagePopConfig.py",'w') as config_file:
		config_file.write(CONFIG_LITERAL)
		config_file.flush()
	import ImagePopConfig as config
PRINT_ERR('ImagePopConfig.py imported successfully!')

for x in [config.LOCK, config.SEAL, config.FILE_LIST_NAME, config.OPERATION_LIST_NAME, config.HISTORY_TABLE_NAME]: 
	hard_check(is_str(x), 'Config: Must be string')
if not check(config.EXTERNAL_SOURCES is None or is_filename(config.EXTERNAL_SOURCES) or all(map(is_filename, config.EXTERNAL_SOURCES.split(';'))), 'Config: External Source Reset b/c Invalid'):
	if config.EXTERNAL_SOURCES is None:
		config.EXTERNAL_SOURCES = []
	elif ';' not in config.EXTERNAL_SOURCES:
		#import config.EXTERNAL_SOURCES.rstrip('.py') as cfg
		name = config.EXTERNAL_SOURCES.rstrip('.py')
		cfg=imp.load_module(name, *imp.find_module(name))#TODO close file??????????
		config.EXTERNAL_SOURCES = [cfg.Functions]
	else:
		temp = config.EXTERNAL_SOURCES
		config.EXTERNAL_SOURCES = []
		for temp_cfg in temp.split(';'):
			#import temp_cfg.rstrip('.py') as cfg
			name = temp_cfg.rstrip('.py')
			cfg=imp.load_module(name, *imp.find_module(name))#TODO close file??????????
			config.EXTERNAL_SOURCES.append(cfg.Functions)
else:
	config.EXTERNAL_SOURCES = []
if not check(isinstance(config.WAIT_INTERVAL, int) and (config.WAIT_INTERVAL > 10), 'Config: Wait set to 10s minimum'):
	config.WAIT_INTERVAL = 10
hard_check(config.STD_ERR is None or is_filename(config.STD_ERR), 'Config: Invalid Error Log File') #TODO
if not check(isinstance(config.CLOBBER, bool), 'Config: Clobber must be a boolean'):
	config.CLOBBER = False
hard_check(config.ROBOT_FRIENDLY, 'Config: Not Robot Friendly')

#TODO config verification
#<END: Custom Config File>


#<Begin: File Manipulation>
def request_filepath(filepath, istype=None):
	hard_check(is_str(filepath), 'filepath must be string: '+filepath)
	if not is_filename(filepath):
		return filepath
	elif config.CLOBBER and istype is not None and istype(filepath):
		return filepath
	else:
		temp = raw_input(filepath+' exists. [Enter] to overwrite, or type new filepath: ')
		if len(temp):
			return request_filepath(temp)
		else:
			return filepath

BLANK_TEXT = [] #TODO
def is_sealed_text(filepath):
	if is_filename(filepath):
        	with open(filepath, 'r') as temp:
                	if config.SEAL == temp.read(len(config.SEAL)):
				return True
	return False

def write_sealed_text(filepath, lines=BLANK_TEXT):
	#Will Overwrite Files!
	filepath = request_filepath(filepath, is_sealed_text)
	with open(filepath, 'w') as temp:
		temp.write(config.SEAL)
		if is_str(lines):
			temp.write(lines)
		elif isinstance(lines, list):
			temp.writelines(filter(is_str, lines))
		temp.flush()
		temp.truncate()
	hard_check(is_sealed_text(filepath), 'failed to create sealed text: '+filepath)
	return filepath 

def read_sealed_text(filepath):
	if not check(is_sealed_table(filepath), 'filepath is not a sealed text: '+filepath):
		return BLANK_TEXT
	with open(filepath, 'r') as temp:
		#if hard_check(config.SEAL == temp.read(len(config.SEAL)), 'Sealed file must begin with SEAL'):
		temp.seek(len(config.SEAL), 0) #Advances the file pointer passed seal
		return temp.readlines() #TODO

BLANK_TABLE = [[]] #TODO
BLANK_TIME = '0'*len(time.ctime(time.time()))
def is_sealed_table(filepath):
	#return True
	#TODO
	return False

def write_sealed_table(filepath, data=BLANK_TABLE):
	#TODO
	filepath = request_filepath(filepath, is_sealed_table)
	#TODO
	hard_check(is_sealed_table(filepath), 'failed to create sealed table: '+filepath)
	return filepath
	
def read_sealed_table(filepath):
	if not check(is_sealed_table(filepath), 'filepath is not a sealed table: '+filepath):
		return BLANK_TABLE
	#TODO Return contents of table !!!!
	
#<END: File Manipulation>


#<BEGIN: Locking>
OVERRIDE_LOCK = False
LOCK_WORD = 'Locked'
def ISLOCKED_DIRECTORY(target_directory):
        if not OVERRIDE_LOCK:
                #TODO might be too hard of a test
                return check(read_sealed_text(os.path.join(target_directory, config.LOCK))[0]==LOCK_WORD, 'Improper Lock File Found')
        else:
                return False

def LOCK_DIRECTORY(target_directory):
        if not ISLOCKED_DIRECTORY(target_directory):
                print 'Locking:', target_directory
                write_sealed_text(os.path.join(target_directory, config.LOCK), lines=[LOCK_WORD])
        print 'Locked:', target_directory

def UNLOCK_DIRECTORY(target_directory):
        if ISLOCKED_DIRECTORY(target_directory):
                print 'Unlocking', target_directory
                try:
                        os.remove(os.path.join(target_directory, config.LOCK))
                except Exception:
                        PRINT_ERR(target_directory+' not unlocked properly!')
                        if not OVERRIDE_LOCK and not len(raw_input('Override locking procedures for this session? [yes]/no ')):
                                OVERRIDE_LOCK=True
                        hard_check(OVERRIDE_LOCK)
        print 'Unlocked:', target_directory
#<END: Locking>



#<Begin: Runtime Main>

INDEX_FILES = (config.FILE_LIST_NAME, config.OPERATION_LIST_NAME, config.HISTORY_TABLE_NAME)
INDEX_VARS = (BLANK_TEXT, BLANK_TEXT, BLANK_TABLE)

RECURSION_DEPTH = 0
def properly_indexed(target_directory):
	targeted = lambda x: os.path.join(target_directory, x)

	path0 = targeted(INDEX_FILES[0])
	path1 = targeted(INDEX_FILES[1])
	path2 = targeted(INDEX_FILES[2])

	def remake_all():
		RECURSION_DEPTH += 1
		hard_check(RECURSION_DEPTH < 5, 'properly_indexed recurred too much')
		write_sealed_text(path0, lines=BLANK_TEXT)
		write_sealed_text(path1, lines=BLANK_TEXT)
		write_sealed_table(path2, lines=BLANK_TABLE)

	are_sealed = (is_sealed_text(path0) and is_sealed_text(path1) and is_sealed_table(path2))
	
	if not are_sealed:
		remake_all()	
		return properly_indexed(target_directory)
	
	INDEX_VARS[0] = read_sealed_text(path0)
	INDEX_VARS[1] = read_sealed_text(path1)
	INDEX_VARS[2] = read_sealed_table(path2)
	
	are_empty = (INDEX_VARS[2]==BLANK_TABLE and INDEX_VARS[1]==BLANK_TEXT and INDEX_VARS[0]==BLANK_TEXT)
	
	if not are_empty:
		len0 = len(INDEX_VARS[0])
		len1 = len(INDEX_VARS[1])
		size2 = len(INDEX_VARS[2])*len(INDEX_VARS[2][0]) #TODO DANGER~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		if len0*(len1+1) != size2:
			remake_all()
			return properly_indexed(target_directory)
	
        #TODO More Checks?
	#TODO Add IGNORED Types of files? Config variable?

	possible_targets = os.listdir(target_directory)
	for fn in INDEX_FILES:
		try:
			possible_targets.remove(fn)
		except Exception:
			remake_all()
			return properly_indexed(target_directory)
	
	RECURSION_DEPTH = 0
	return possible_targets #THIS IS EVERYTHING, even directories and weird stuff

ARG_CACHE = dict()
def arg_match(arg):
	#Returns the library function for a given arg, or None
	if arg in ARG_CACHE:
		return ARG_CACHE[arg]
	for source in config.EXTERNAL_SOURCES:
		if arg in source:
			ARG_CACHE[arg] = source[arg]
			return ARG_CACHE[arg]
	ARG_CACHE[arg]=None
	return ARG_CACHE[arg]

def session(target_directory, parsed_args, unparsed_pargs):
	#string
	#list of strings
	#list of strings #TODO Don't worry about these for now

	targeted = lambda x: os.path.join(target_directory, x)

	#CHECKS FOR SAVED INDEX FILES AND RETURNS A LIST OF ONLY POTENTIAL TARGET FILES
	potential_targets = properly_indexed(target_directory) #This function is recursive!! DANGEROUS!!
	
	#TODO______________________________________________________________________________________________
	INDEX_VARS[1] = parsed_args
	
	for potential_target in potential_targets:
		if (potential_target not in INDEX_VARS[0]) and is_filepath(targeted(potential_target)): 
			INDEX_VARS[0].append(potential_target)
			new_row = [time.asctime(time.strptime(time.ctime( os.stat(targeted(potential_target)).st_mtime )))]
			new_row.extend([BLANK_TIME]*len(INDEX_VARS[1]))
			INDEX_VARS[2].append(new_row)

	for rownum,(filename, table_row) in enumerate(zip(INDEX_VARS[0],INDEX_VARS[2])):

		if not is_filepath(targeted(filename)):
			#This means the input is gone	
			#TODO but can be ignored	
			continue

		#First check the input timestamp. If it's been modified, invalidate all others	
		input_modified = time.strptime(time.ctime( os.stat(targeted(filename)).st_mtime ))
		if input_modified > time.strptime( table_row[0] ):
			table_row[1:] = BLANK_TIME
			table_row[0] = time.asctime(input_modified)

		#Now check all output timestamps; if they are newer than the input or blank, queue them
		for argnum,(arg, output_modified_old) in enumerate(zip(INDEX_VARS[1],table_row[1:])):
			
			output_filename = os.path.join(target_directory, arg, filename)
			if is_filepath(output_filename):
				output_modified = time.strptime(time.ctime( os.stat(output_filename).st_mtime ))
			else:
				output_modified = BLANK_TIME
		
			if (output_modified_old == BLANK_TIME) or (output_modified_old != output_modified) or (output_modified < input_modified):

				try:
					arg_match(arg)(filename, output_filename)
					INDEX_VARS[2][rownum][1+argnum]=time.strptime(time.ctime( os.stat(output_filename).st_mtime ))
				except Exception as e:
					#TODO		
					PRINT_ERR(e)
				finally:
					pass
					#SAVE FILES CAREFULLY
	
	write_sealed_text(targeted(INDEX_FILES[0]), lines=INDEX_VARS[0])
	write_sealed_text(targeted(INDEX_FILES[1]), lines=INDEX_VARS[1])
	write_sealed_table(targeted(INDEX_FILES[2]), lines=INDEX_VARS[2])
	return

def try_to_parse_args(*args):
	parsed = []
	unparsed = []
	for arg in args:
		if (arg_match(arg) is not None):
			parsed.append(arg)
		else:
			unparsed.append(arg)
	return parsed, unparsed

def sleep_timer(sleep_time=config.WAIT_INTERVAL, subinterval=config.WAIT_INTERVAL/100.0):
	start = time.time()
	sleep_time = float(sleep_time)
	if not check(sleep_time > 0.0, 'sleep_timer must be given a positive number'):
		sleep_time = config.WAIT_INTERVAL
	end = start+sleep_time
	end_message = 'Program will resume automatically after: '+time.asctime(end)
	print end_messag

	subinterval = float(subinterval)
	if not check(sleep_time > subinterval > 0.0, 'sleep_timer subinterval must be small and positive'):
		subinterval = config.WAIT_INTERVAL/100.0

	intervals = int(sleep_time/subinterval)

	interrupt_message = 'Program idle: ' #TODO 'Press enter to interact...'
	interrupt_char_0 = '~\r'
	interrupt_char_1 = '-\r'
	def is_interrupted(within):
		sys.stdout.write(interrupt_message+interrupt_char_0)
		sys.stdout.flush()
		#TODO interactive
		assert float(within)>0.0
		time.sleep(float(within))
		sys.stdout.write(interrupt_message+interrupt_char_1)
		sys.stdout.flush()
	
	#flicker messsage using projected wake time
	for i in range(intervals):
		if is_interrupted(subinterval/2.0) or time.time()>end:
			break
		else:
			timer.sleep(subinterval/2.0)
	print ''
	return 

#TODO Make it so the program has an overall LEASH
LEASH_START = time.time()
LEASH_LENGTH = 60*60*1 #1hour
def leash_allows():
	return time.time() < LEASH_START+LEASH_LENGTH
	
def run(target_directory, *args):
	hard_check(is_directory(target_directory), "Invalid Directory: "+target_directory)
	LOCK_DIRECTORY(target_directory)
	try:
		parsed_args, unparsed_args = try_to_parse_args(args) 
		if len(parsed_args):
			PRINT_ERR('Run understood: '+','.join(parsed_args))
		if len(unparsed_args):
			PRINT_ERR('Run did not understand: '+','.join(unparsed_args))
		#Catches args in config.EXTERNAL_SOURCES
		
		#TODO
		#Does work, then goes idle, then repeats, until LEASH
		while(leash_allows()):
			#TODO
			session(target_directory, parsed_args, unparsed_args)
			#TODO
			sleep_timer()
			#TODO

	except Exception as e:
		#TODO
		PRINT_ERR(e)
	finally:
		UNLOCK_DIRECTORY(target_directory)	
		#TODO
#<END: Runtime Main>




