﻿def print_lol(the_list,level=0):
	for i in the_list:
		if isinstance(i,list):
			print_lol(i,level)
		else:
			for tab_stop in range(level):
				print("\t",end='')
			print(i)
