import sys


def help_display(x=None):
	print 'this is the lib help message' #TODO
	#print "IMAGE_POP.PY USAGE: \npython image_pop.py [flags] [functions]"
	#print "example_user@input_directory:python image_pop.py -i input_directory -o output_directory g1 g2 so1 so2"
	#sys.exit(1) #Safe Helpful Exit
	raise Exception()	

def check(xbool):
	if not xbool:
		help_display()

check(__name__ != "__main__")
#check(len(sys.argv) > 1)

'''
def our_config(user_conf=None):
	try:
		if x is None:
			import ImagePopConfig
		else:
			import user_conf as ImagePopConfig
	except Exception:
		print "error message"
		sys.exit(2)#TODO
'''

def init_check(directory):
	pass #TODO

def our_init(target, x=[]):
	if not init_check(target):
		pathname = os.path.join(target, )
		with open('ImagePopInit.txt', 'w') as trailhead:

	pass #TODO

def our_run(target, x=[]):
	if not init_check(target):
		our_init(target)
		our_run(target, x)
	else:
		pass #TODO

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

our_args = []
if len(sys.argv) > 2:
	our_args = sys.argv[2:]	


def designate_target(x):
	import os
	def verify_target(directory):
		if os.path.isdir(directory):
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
		pwd = os.getcwd()
		check(verify_target(pwd))
		return pwd, x
	



modes[sys.argv[1]](*designate_target(our_args))

sys.exit(0)
