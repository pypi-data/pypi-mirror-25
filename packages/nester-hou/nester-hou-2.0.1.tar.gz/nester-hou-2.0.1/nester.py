""" 这是 ”nester.py“ 模块, 提供了一个名为 print_lol 的函数 """
def print_lol(the_list):
	""" 这个函数取一个位置参数， 名为 the_list, 这可以是任何 Python 列表 """
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			print(each_item)
