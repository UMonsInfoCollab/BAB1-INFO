import sys, os

SYMBOLS = "0123456789ABCDEF"

input_base = int(input("Entrez la base d'entree: "))

if (input_base < 2) or (input_base > 16):
	sys.exit("Erreur: la base doit etre " \
			"comprise entre 2 et 16")

def convert_to_deci(word):
	val = 0
	size = len(word)
	for i in range(len(word)):
		val += SYMBOLS.index(word[i])*input_base**(size-i-1)

	return val

output_base = int(input("Entrez la base de sortie: "))

num = input("Entrez le nombre: ")
x = convert_to_deci(num) if output_base != 10 else int(num)

if (x < 0):
	sys.exit("Erreur: le nombre doit etre positif")

word = "0" if (x == 0) else ""
print("\n\tQuotient\tReste")
while (x != 0):
	q = int(x / output_base)
	r = int(x % output_base)
	print(f"{x}/{output_base}\t", q, "\t\t", r)
	word = "%c%s" % (SYMBOLS[r], word)
	x = q
print("\nEn base %d : %s" % (output_base, word))
os.system("pause")