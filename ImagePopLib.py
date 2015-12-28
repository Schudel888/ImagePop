#This is intended to be a library file for Sol and Lowell's ImagePop.py program.

#<BEGIN: Imports>
import sys
import os
import time
import imp
import csv
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
	with open(output_filepath, 'wb') as temp:
		input_stat = os.stat(input_filepath)
		temp.writelines(map(str, input_stat))
		temp.flush()
		temp.truncate()	
SOURCES['demo']=DEMO

#TODO
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

WAIT_INTERVAL = 10 #seconds #Int Only!
#Duration to wait before checking files

LEASH_LENGTH = 10*60*1 #seconds #Int Only!
#Total amount of time the program is allowed to run before exiting

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

try:
	temp_sources = []
	if check(config.EXTERNAL_SOURCES is None or is_filename(config.EXTERNAL_SOURCES) or all(map(is_filename, config.EXTERNAL_SOURCES.split(';'))), 'Config: External Source Reset b/c Invalid'):
		if config.EXTERNAL_SOURCES is None:
			#config.EXTERNAL_SOURCES = []
			pass
		elif is_str(config.EXTERNAL_SOURCES) and ';' not in config.EXTERNAL_SOURCES:
			#import config.EXTERNAL_SOURCES.rstrip('.py') as cfg
			name = config.EXTERNAL_SOURCES.rstrip('.py')
			cfg=imp.load_module(name, *imp.find_module(name))#TODO close file??????????
			temp_sources.append(cfg.Functions)
		else:
			#temp = config.EXTERNAL_SOURCES
			#config.EXTERNAL_SOURCES = []
			for temp_cfg in temp.split(';'):
				#import temp_cfg.rstrip('.py') as cfg
				name = temp_cfg.rstrip('.py')
				cfg=imp.load_module(name, *imp.find_module(name))#TODO close file??????????
				temp_sources.append(cfg.Functions)
except Exception:
	pass
finally:
	temp_sources.append(SOURCES)
	config.EXTERNAL_SOURCES = temp_sources

if not check(isinstance(config.WAIT_INTERVAL, int) and (config.WAIT_INTERVAL > 10), 'Config: Wait set to 10s minimum'):
	config.WAIT_INTERVAL = 10
if not check(isinstance(config.LEASH_LENGTH, int) and (24*60*60 > config.LEASH_LENGTH > 1*1*60), 'Config: Leash set within 24h max and 60s min'):
	config.LEASH_LENGTH = 10*60
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
		return True
		'''
		with open(filepath, 'r') as temp:
			if config.SEAL == temp.read(len(config.SEAL)):
				return True
		'''
	return False

def write_sealed_text(filepath, lines=BLANK_TEXT):
	#Will Overwrite Files!
	filepath = request_filepath(filepath, is_sealed_text)
	with open(filepath, 'w') as temp:
		temp.write(config.SEAL)
		if is_str(lines):
			temp.write(lines)
		elif isinstance(lines, list):
			for line in lines: #filter(is_str, lines):
				temp.write(line+'\n')
		temp.flush()
		temp.truncate()
	hard_check(is_sealed_text(filepath), 'failed to create sealed text: '+filepath)
	return filepath 

def read_sealed_text(filepath, length=None):
	if not check(is_sealed_text(filepath), 'filepath is not a sealed text: '+filepath):
		return BLANK_TEXT
	with open(filepath, 'r') as temp:
		#if hard_check(config.SEAL == temp.read(len(config.SEAL)), 'Sealed file must begin with SEAL'):
		temp.seek(len(config.SEAL), 0) #Advances the file pointer passed seal
		if not (isinstance(length, int) and length > 0):
			return temp.read().splitlines()
		else:
			return temp.read(length)

BLANK_TABLE = [[]] #TODO
BLANK_TIME = '0'*len(time.ctime(time.time())) #24
def is_sealed_table(filepath):
	if is_filename(filepath):
		return True
	'''
	if is_sealed_text(filepath):
		return True
		with open(filepath, 'rb') as csvfile:
			#dialect = csv.Sniffer().sniff(csvfile.read(1024))
			csvfile.seek(len(config.SEAL))
			reader = csv.reader(csvfile)#, dialect)
			row_len=None
			for row in reader:
				if row_len is None:
					row_len = len(row)
				elif len(row) != row_len:
						return False
				for element in row:
					if len(BLANK_TIME) != len(element):
						return False
		return True
	'''
	#TODO
	return False

def write_sealed_table(filepath, data=BLANK_TABLE):
	#TODO
	filepath = request_filepath(filepath, is_sealed_table)
	with open(filepath, 'wb') as csvfile:
		#csvfile.write(config.SEAL)
		writer = csv.writer(csvfile)
		writer.writerows(data)
		csvfile.flush()
		csvfile.truncate()

	#TODO
	hard_check(is_sealed_table(filepath), 'failed to create sealed table: '+filepath)
	return filepath
	
def read_sealed_table(filepath):
	if not check(is_sealed_table(filepath), 'filepath is not a sealed table: '+filepath):
		return BLANK_TABLE

	with open(filepath, 'rb') as csvfile:
		#dialect = csv.Sniffer().sniff(csvfile.read(1024))
		#csvfile.seek(len(config.SEAL))
		reader = csv.reader(csvfile)#, dialect)
		table_out = []
		for row in reader:
			table_out.append(row)
		if not len(table_out):
			return BLANK_TABLE
		return table_out
	#TODO Return contents of table !!!!
	
#<END: File Manipulation>


#<BEGIN: Locking>
OVERRIDE_LOCK = False
LOCK_WORD = 'Locked'
def ISLOCKED_DIRECTORY(target_directory):
	if not OVERRIDE_LOCK and is_filename(os.path.join(target_directory, config.LOCK)):
		#TODO might be too hard of a test
		return check(read_sealed_text(os.path.join(target_directory, config.LOCK), len(LOCK_WORD))==LOCK_WORD, 'Improper Lock File Found')
	else:
		return False

def LOCK_DIRECTORY(target_directory):
	#if not ISLOCKED_DIRECTORY(target_directory):
	print 'Locking:', target_directory
	write_sealed_text(os.path.join(target_directory, config.LOCK), lines=LOCK_WORD)
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
			hard_check(OVERRIDE_LOCK, 'Lock must be overridden if it is not working properly...')
		print 'Unlocked:', target_directory
#<END: Locking>



#<Begin: Runtime Main>

INDEX_FILES = (config.FILE_LIST_NAME, config.OPERATION_LIST_NAME, config.HISTORY_TABLE_NAME, config.LOCK, 'ImagePopInit.txt', 'ImagePopReadme.txt') #TODO
INDEX_VARS = [BLANK_TEXT, BLANK_TEXT, BLANK_TABLE]

#RECURSION_DEPTH = 0
def properly_indexed(target_directory):
	#global RECURSION_DEPTH
	targeted = lambda x: os.path.join(target_directory, x)

	path0 = targeted(INDEX_FILES[0])
	path1 = targeted(INDEX_FILES[1])
	path2 = targeted(INDEX_FILES[2])
	#print path0, path1, path2

	def remake_all():
		#RECURSION_DEPTH += 1
		#hard_check(RECURSION_DEPTH < 5, 'properly_indexed recurred too much')
		write_sealed_text(path0, lines=BLANK_TEXT)
		write_sealed_text(path1, lines=BLANK_TEXT)
		write_sealed_table(path2, data=BLANK_TABLE)

	if not (is_sealed_text(path0) and is_sealed_text(path1) and is_sealed_table(path2)):
		remake_all()	
		return properly_indexed(target_directory)
	
	INDEX_VARS[0] = read_sealed_text(path0)
	INDEX_VARS[1] = read_sealed_text(path1)
	INDEX_VARS[2] = read_sealed_table(path2)
	
	if (INDEX_VARS[2]!=BLANK_TABLE or INDEX_VARS[1]!=BLANK_TEXT or INDEX_VARS[0]!=BLANK_TEXT):
		len0 = len(INDEX_VARS[0])
		len1 = len(INDEX_VARS[1])
		size2 = len(INDEX_VARS[2])*len(INDEX_VARS[2][0]) #TODO DANGER
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
	
	#RECURSION_DEPTH = 0
	return possible_targets #THIS IS EVERYTHING, even directories and weird stuff

ARG_CACHE = dict()
def arg_match(arg):
	#print arg
	#print config.EXTERNAL_SOURCES
	#print ARG_CACHE
	#Returns the library function for a given arg, or None
	if arg in ARG_CACHE:
		return ARG_CACHE[arg]
	for source in config.EXTERNAL_SOURCES:
		if arg in source:
			ARG_CACHE[arg] = source[arg]
			return ARG_CACHE[arg]
	return None

def session(target_directory, parsed_args):
	#string
	#list of strings
	#list of strings #TODO Don't worry about these for now
	targeted = lambda x: os.path.join(target_directory, x)

	#print 'Session: entering properly_indexed'
	#CHECKS FOR SAVED INDEX FILES AND RETURNS A LIST OF ONLY POTENTIAL TARGET FILES
	assert is_directory(target_directory)
	potential_targets = properly_indexed(target_directory) #This function is recursive!! DANGEROUS!!

	index_of_cache = dict()
	def index_of(str_filename, str_argname=None):
		if str_argname is None:
			if str_filename not in index_of_cache:
				try:
					index_of_cache[str_filename] = INDEX_VARS[0].index(str_filename)
				except Exception:
					index_of_cache[str_filename] = None
			return index_of_cache[str_filename]
		else:
			if (str_filename, str_argname) not in index_of_cache:
				try:
					index_of_cache[(str_filename, str_argname)] = INDEX_VARS[0].index(str_filename), 1+INDEX_VARS[1].index(str_argname)
				except Exception:
					index_of_cache[(str_filename, str_argname)] = None
			return index_of_cache[(str_filename, str_argname)]
	
	#TODO
	#INDEX_VARS[1] ?= parsed_args #WRONG
	#old_parsed_args = read_sealed_text(targeted(INDEX_FILES[1]))
	for new_column_name in list(set(parsed_args) - set(INDEX_VARS[1])):
		INDEX_VARS[1].append(new_column_name)
		if INDEX_VARS[2] != BLANK_TABLE:
			for row in INDEX_VARS[2]:
				#TODO~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~ ~ ~ ~  ~ ~  ~~~  ~~ ~  ~
				row.append(BLANK_TIME)

	for arg in parsed_args:
		output_directory = targeted(arg)
		if not is_directory(output_directory):
			try:
				os.mkdir(output_directory)
			except OSError:
				#Should mean it exists already #TODO
				PRINT_ERR('Output directory not properly recognized: '+output_directory)

	#print 'Session: entering potential_targets'
	BLANK_TIME_ROW = [BLANK_TIME]*len(INDEX_VARS[1])

	for potential_target in potential_targets:
		if (potential_target not in INDEX_VARS[0]) and is_filename(targeted(potential_target)): 
			if INDEX_VARS[2]==BLANK_TABLE:
				INDEX_VARS[2] = []
			INDEX_VARS[0].append(potential_target)
			#new_row = [time.asctime(time.strptime(time.ctime( os.stat(targeted(potential_target)).st_mtime )))]
			new_row = [time.ctime( os.stat(targeted(potential_target)).st_mtime )]
			new_row.extend(BLANK_TIME_ROW)
			INDEX_VARS[2].append(new_row)

	#print 'Session: entering rownum'
	#for rownum,filename in enumerate(INDEX_VARS[0]):
	for filename in INDEX_VARS[0]:

		if not is_filename(targeted(filename)):
			#This means the input is gone	
			#TODO but can be ignored	
			continue

		#print 'Session: entering input_modified'
		#First check the input timestamp. If it's been modified, invalidate all others	
		input_modified = time.strptime(time.ctime( os.stat(targeted(filename)).st_mtime ))
		if input_modified > time.strptime( INDEX_VARS[2][index_of(filename)][0] ):
			INDEX_VARS[2][index_of(filename)] = [time.asctime(input_modified)]
			INDEX_VARS[2][index_of(filename)].extend(BLANK_TIME_ROW)

		#Now check all output timestamps; if they are newer than the input or blank, queue them
		#for (argnum,arg) in enumerate(INDEX_VARS[1]):
		for arg in parsed_args:
			index = index_of(filename, arg)
			output_modified_old = INDEX_VARS[2][index[0]][index[1]] #INDEX_VARS[2][rownum][1+argnum]

			output_filename = os.path.join(target_directory, arg, filename)
			if is_filename(output_filename):
				output_modified = time.strptime(time.ctime( os.stat(output_filename).st_mtime ))
			else:
				output_modified = BLANK_TIME
		
			if (output_modified_old == BLANK_TIME) or (time.strptime(output_modified_old) != output_modified) or (output_modified < input_modified):
				#print 'old',output_modified_old
				#print 'new',output_modified
				#print 'in',time.asctime(input_modified)
				try:

					#TODO HERE IS WHERE THE MEAT OF THE PROGRAM HAPPENS!
					
					arg_match(arg)(targeted(filename), output_filename)   #TODO-___________________________________________


					#INDEX_VARS[2][rownum][1+argnum]=time.ctime( os.stat(output_filename).st_mtime )
					INDEX_VARS[2][index[0]][index[1]] =time.ctime( os.stat(output_filename).st_mtime )

					print 'Session:', arg, targeted(filename)

				except Exception as e:
					#TODO		
					#PRINT_ERR('Session: '+arg+' '+targeted(filename))
					PRINT_ERR(e)
				finally:
					pass
					#SAVE FILES CAREFULLY
	'''
	print INDEX_VARS[0]
	print INDEX_VARS[1]
	print INDEX_VARS[2]
	#sys.exit(1)
	'''
	write_sealed_text(targeted(INDEX_FILES[0]), lines=INDEX_VARS[0])
	write_sealed_text(targeted(INDEX_FILES[1]), lines=INDEX_VARS[1])
	write_sealed_table(targeted(INDEX_FILES[2]), data=INDEX_VARS[2])
	return

def try_to_parse_args(args):
	parsed = []
	unparsed = []
	for arg in args:
		if (arg_match(arg) is not None):
			parsed.append(arg)
		else:
			unparsed.append(arg)
	return list(set(parsed)), list(set(unparsed))

def sleep_timer(sleep_time=config.WAIT_INTERVAL, subinterval=config.WAIT_INTERVAL/100.0):
	start = time.time()
	sleep_time = float(sleep_time)
	if not check(sleep_time > 0.0, 'sleep_timer must be given a positive number'):
		sleep_time = config.WAIT_INTERVAL
	end = start+sleep_time
	end_message = 'Program will resume automatically after: '+time.ctime(end)
	print end_message

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
			time.sleep(subinterval/2.0)
	print ''
	return 

#TODO Make it so the program has an overall LEASH
LEASH_START = time.time()
def leash_allows():
	return time.time() < LEASH_START+config.LEASH_LENGTH
	
def run(target_directory, args):
	hard_check(is_directory(target_directory), "Invalid Directory: "+target_directory)
	LOCK_DIRECTORY(target_directory)
	#try:
	parsed_args, unparsed_args = try_to_parse_args(args) 
	if len(parsed_args):
		PRINT_ERR('Run understood: '+','.join(parsed_args))
	if len(unparsed_args):
		PRINT_ERR('Run did not understand: '+','.join(unparsed_args))
	#Catches args in config.EXTERNAL_SOURCES
	
	#TODO
	#Does work, then goes idle, then repeats, until LEASH
	#print "Entering main while loop"
	while(leash_allows()):
		#TODO
		#print 'Entering Session'
		session(target_directory, parsed_args)
		#TODO
		#print 'Entering sleep timer()'
		sleep_timer()
		#TODO

	try:
		pass
	except Exception as e:
		#TODO
		PRINT_ERR(e)
	finally:
		UNLOCK_DIRECTORY(target_directory)	
		#TODO
#<END: Runtime Main>




