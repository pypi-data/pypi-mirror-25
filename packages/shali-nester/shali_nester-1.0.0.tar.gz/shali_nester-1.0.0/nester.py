# Created by shali 
# To print the items of a nested list be it as many nested things

def print_list_items(input_list):
	for each_item in input_list:
		if(isinstance(each_item,list)):
			print_list_items(each_item)
		else:
			print(each_item)