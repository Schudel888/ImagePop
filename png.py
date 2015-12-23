#png tester
def png(input_filepath, output_filepath, *args):
	with open(output_filepath, 'w') as temp:
		temp.write('png of: '+input_filepath)
		temp.flush()
		temp.truncate()	


Functions = dict()
Functions['png'] = png
