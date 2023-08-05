
import sys
from termcolor import cprint, colored

# text = colored("Hello", "red", attrs = ["blink"])
# print(text)

# cprint('hello word', 'green', "on_red")

def output():
	print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
	print_red_on_cyan('Hello, World!')
	print_red_on_cyan('Hello, Universe!')

	for i in range(10):
	    cprint(i, 'magenta', end=' ')

	cprint("Attention!", 'red', attrs=['bold'], file=sys.stderr)

def ultimate_main():
	print("Ultimate!!!")