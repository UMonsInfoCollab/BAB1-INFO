import Cache
import os

with_colorama = False

try:
	import colorama
	from colorama import Fore, Back, Style
	with_colorama = True
	colorama.init()
except ImportError:
	print("C'est plus beau si vous avez le package 'colorama' installé.")
	ask_again = True
	while ask_again:
		ask_again = False
		response = input("Souhaitez-vous l'installer maintenant? (Y/N) ")
		if response.upper() == "Y":
			os.system("pip3 install colorama")
			try:
				import colorama
				from colorama import Fore, Back, Style
				with_colorama = True
				colorama.init()
			except ImportError:
				print("Impossible d'importer colorama. Veuillez vérifier que le package est installé et réessayez.")

		elif response.upper() == "N":
			pass

		else:
			ask_again = True


archi = None
mem_size = None
num_lines = None
line_size = None
dump_strat = None

def setParameters(params):
	global archi
	global mem_size
	global num_lines 
	global line_size 
	global dump_strat

	archi = int(params[1])
	mem_size = int(params[2])
	num_lines = int(params[3])
	line_size = int(params[4])

	p5 = params[5]

	if p5.upper() == "LRU":
		dump_strat = Cache.LRU
	elif p5.upper() == "LFU":
		dump_strat = Cache.LFU
	elif p5.upper() == "FIFO":
		dump_strat = Cache.FIFO
	elif p5.upper() == "RAND":
		dump_strat = Cache.RAND
	else:
		raise Exception(f"Unsupported dump strategy: {p5}.")


def main():
	cache = None
	file = "instr.txt"

	content = []
	with open(file, "r") as f:
		content = f.read()

	content = list(content.split("\n"))

	parameters = content[0:6]

	setParameters(parameters)

	if parameters[0].upper() == "DM":
		cache = Cache.DirectMappedCache(archi, mem_size, num_lines, line_size, dump_strat)
	elif parameters[0].upper() == "2WA":
		cache = Cache.SetAssociativeCache(archi, mem_size, num_lines, line_size, Cache.TWO_WAY, dump_strat)
	elif parameters[0].upper() == "4WA":
		cache = Cache.SetAssociativeCache(archi, mem_size, num_lines, line_size, Cache.FOUR_WAY, dump_strat)
	elif parameters[0].upper() == "FA":
		cache = Cache.FullyAssociativeCache(archi, mem_size, num_lines, line_size, Cache.FULLY, dump_strat)
	else:
		raise Exception(f"Unsupported cache structure: {parameters[0].upper()}.")

	instructions = content[6::]

	#print()
	#print(f"{Back.WHITE+ Fore.BLACK}Cache State before instruction:\n", str(cache), f"{Style.RESET_ALL}\n\n\n") if with_colorama else print("Cache State before instruction:\n", str(cache), "\n\n\n")
	
	for _line in instructions:
		line = _line.rstrip()
		if not "#" in line:
			instr = line[2::]
			result = cache.touch(instr)
			if result == Cache.COMP_MISS:
				print(f"{Fore.CYAN + instr + Style.RESET_ALL}: {Fore.YELLOW}COMPULSORY MISS{Style.RESET_ALL}", "\n") if with_colorama else print(f"{instr}: COMPULSORY MISS", "\n")
			elif result == Cache.CONF_MISS:
				print(f"{Fore.CYAN + instr + Style.RESET_ALL}: {Fore.RED}CONFLICT MISS{Style.RESET_ALL}", "\n") if with_colorama else print(f"{instr}: CONFLICT MISS", "\n")
			elif result == Cache.CAPA_MISS:
				print(f"{Fore.CYAN + instr +Style.RESET_ALL}: {Fore.MAGENTA}CAPACITY MISS{Style.RESET_ALL}", "\n") if with_colorama else print(f"{instr}: CAPACITY MISS", "\n")
			elif result == Cache.HIT:
				print(f"{Fore.CYAN + instr + Style.RESET_ALL}: {Fore.GREEN}HIT{Style.RESET_ALL}", "\n") if with_colorama else print(f"{instr}: HIT", "\n")

	print(f"{Back.WHITE+ Fore.BLACK}Cache State after instruction:\n", str(cache), f"{Style.RESET_ALL}\n\n\n") if with_colorama else print("Cache State after instruction:\n", str(cache), "\n\n\n")

if __name__ == '__main__':
	main()