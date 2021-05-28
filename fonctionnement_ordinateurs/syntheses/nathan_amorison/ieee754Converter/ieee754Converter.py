#encoding: utf-8

import math
import os

def abs(x):
	if x < 0:
		return -x
	else:
		return x

def convert_int_to_bin(num:int):
	"""
	Simple fonction de convertion d'un nombre décimal vers du binaire.
	Possibilité d'utiliser cette fonction pour convertir vers de l'hexadécimal si on change la valeur de la variable 'base'.
	Elle est utilisée ici pour récupérer la partie de la mantisse associée à la partie entière du nombre à convertir.
	Ca permettra également de trouver la valeur de e.

	Paramètres:
		num: int
			nombre entier décimal à convertir.

	Retour:
		Un String correspondant à la valeur binaire.
	"""
	SYMBOLS = "0123456789ABCDEF"
	if num < 0:
		raise ValueError("impossible to convert negative number")

	x = num
	base = 2

	word = "0" if x == 0 else ""

	while (x != 0):
		q = int(x / base)
		r = int(x % base)
		word = "%c%s" % (SYMBOLS[r], word)
		x = q

	return word

def complete(word, size):
	new_word = word
	for i in range(size - len(word)):
		new_word = "0" + new_word

	return new_word

def get_m_part(num, maximum = 52):
	"""
	Fonction permettant de récupérer la partie de la mantisse associée à la partie décimale du nombre à convertir.

	Paramètres:
		num: float, double
			nombre permettant de récupérer la suite de la mantisse.
		maximum: int, optionnel
			nombre maximum de valeurs binaires dans la mantisse retournée (permet de stopper le calcul si le nombre est infiniment précis).
			il n'est pas nécessaire d'avoir un nombre d'occurence plus grand que le nombre de bits formant la mantisse.

	Retour:
		Tuple contenant la seconde partie de la mantisse et la séquence de répétition. S'il n'y a pas de répétion, la seconde valeur du tuple est None.
	"""
	x = num
	i = maximum
	already = []
	word, rep = ("", None)
	while(i>0 and x != 0):
		if x in already:
			#permet de stopper la boucle s'il y aura une répétition dans l'algorithme de calcul
			rep = already[already.index(x)::]
			break
		already.append(x)
		x = x*2
		word += "1" if x >= 1.0 else "0"
		if x >= 1:
			x -= 1
		i -= 1

	return (word, rep)

def get_ieee754(num, E = None, M = None, B = None, bits = None):
	"""
	Fonction convertissant le réel en nombre binaire sous la norme ieee754.

	Paramètres:
		num: double, float
			Réel à convertir.
		E: int, optionnel
			Taille de e.
		M: int, optionnel
			Taille de la mantisse.
		B: int, optionnel
			Valeur du biais.
		bits: int, optionnel
			Taille prédéfinie sur 32 ou 64 bits.

	Retour:
		Convertion.
	"""
	s = 1 if num < 0 else 0 #set du bit de signe
	partie_int = abs(int(num)) #récupération de la partie entière du nombre à convertir
	partie_dec = abs(num) - partie_int #récupération de la partie décimale du nombre à convertir

	#paramétrage des valeurs de E, M et B
	if not E and not M and not B and not bits:
		#si aucun paramètre n'a été donné, la valeur par défaut est sur 64bits
		bits = 64

	if not B and E and M:
		B = 2**(E-1) - 1

	if bits == 64:
		E = 11
		M = 52
		B = 1023

	if bits == 32:
		E = 8
		M = 23
		B = 127

	#valeur binaire de la partie entière permettant le calcul de la première partie de la mantisse et de la valeur de e
	word = convert_int_to_bin(partie_int)

	n = 0
	x_prim = abs(num)
	if x_prim < 1:
		while x_prim < 1:
			x_prim *= 2
			n -= 1

	elif x_prim >= 2:
		while x_prim >= 2:
			x_prim /= 2
			n += 1

	e = n + B

	if e >= 2**E - 1:
		return "Le nombre ne peut pas être représenté"

	elif e <= 0:
		#dénormalisé
		e = "000"
		m = abs(num) * (2**(M-1+B))
		word =  str(s) + e + str(complete(convert_int_to_bin(m), M))
		return word

	else:
		#normalisé
		m = (x_prim-1)*(2**M)
		word =  str(s) + str(complete(convert_int_to_bin(e), E)) + str(complete(convert_int_to_bin(m), M))
		return word

def getValueFromBin(word):
	val = 0
	size = len(word)
	for i in range(len(word)):
		if word[i] == "1":
			val += 2**(size-i-1)

	return val

def ieee754(word, E = None, M = None, B = None, bits = None):
	if not E and not M and not B and not bits:
		bits = 64

	if not B and E and M:
		B = 2**(E-1) - 1

	if bits == 64:
		E = 11
		M = 52
		B = 1023

	if bits == 32:
		E = 8
		M = 23
		B = 127

	mot = word.replace(" ","")
	s = getValueFromBin(mot[0])
	e = getValueFromBin(mot[1:E+1])
	m = getValueFromBin(mot[E+1::])
	
	#vérification des valeurs spéciales
	if e == 2**E - 1:
		if m == 0:
			if s == 0:
				return math.inf
			else:
				return -math.inf
		else:
			return math.nan


	x = ((-1)**s) #paramétrage du signe
	if e != 0:
		#valeur normalisée
		y = (1 + m/(2**M))
		z = (2**(e-B))
	else:
		#valeur dénormalisée
		y = m/(2**M)
		z = (2**(1-B))
	
	return x*y*z


if __name__ == '__main__':
	#input_word
	try:
		input_word = float(input("input number: "))
	except ValueError:
		print("Please, enter valid float values.\n")
		os.system("pause")
		exit()

	E = input("\nE (if you want value for 32 and/or 64bits, just enter without writing anything): ")
	if (E == ""):
		test64 = get_ieee754(input_word) # get convertion of input on 64bits
		print("output 64bits:", test64)
		print("read value:", ieee754(test64), "\n") # get back the number to see if it's ok

		test32 = get_ieee754(input_word, bits = 32) # get convertion of input on 32bits
		print("output 32bits:", test32)
		print("read value:", ieee754(test32, bits = 32), "\n") # get back the number to see if it's ok

	else:
		try:
			E = int(E)
			B = int(input("B: "))
			M = int(input("M: "))

			#example if you know E M B
			test = get_ieee754(input_word, E = E, M = M, B = B)
			print(f"\noutput {1+E+M}bits:", test)
			print("read value:", ieee754(test, E = E, M = M, B = B), "\n")

		except ValueError:
			print("Please, enter valid integers for E B M values.\n")
			os.system("pause")
			exit()


	os.system("pause")