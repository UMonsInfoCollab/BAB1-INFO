import math
import random


HIT = 0
COMP_MISS = 1	# compulsory miss
CONF_MISS = 2	# conflict miss
CAPA_MISS = 3	# capacity miss

LRU = 0
RAND = 1
FIFO = 2
LFU = 3

TWO_WAY = 2
FOUR_WAY = 4
FULLY = -1

class Converter:
	_SYMBOLS = "0123456789ABCDEF"

	def convert_to_deci(word, base = 16):
		val = 0
		size = len(word)
		for i in range(len(word)):
			#print(f"\nDEBUG: {word[i]}\n")
			val += Converter._SYMBOLS.index(word[i])*base**(size-i-1)

		return val

	def convert_from_deci(x, base = 2):
		word = "0" if (x == 0) else ""
		while (x != 0):
			q = int(x / base)
			r = int(x % base)
			
			word = "%c%s" % (Converter._SYMBOLS[r], word)
			x = q
		return word

	def complete(word, size):
		new_word = (size - len(word))*"0"
		new_word += word
		return new_word

	def convert(word, input_base, output_base):
		return Converter.convert_from_deci(Converter.convert_to_deci(word, input_base), output_base)


class Cell:
	def __init__(self, tag, set, offset, id = 1):
		self.tag = tag
		self.set = set
		self.offset = offset

		self.id = id

	def increment(self):
		self.id+=1

	def decrement(self):
		self.id-=1

	def getValue(self):
		return self.tag + self.set + self.offset

	def getSet(self):
		return self.set

	def hasSameSet(self, other):
		return self.set == other.set

	def getId(self):
		return self.id

	def resetId(self):
		self.id = 0

	def next(self, offset):
		word = self.tag+self.set+self.offset
		val = Converter.convert_to_deci(word, base = 2)
		next_val = val + offset
		new_word = Converter.convert_from_deci(next_val)
		return Cell(new_word[::len(self.tag)], new_word[len(self.tag):len(self.tag)+len(self.set)], new_word[len(self.tag)+len(self.set)::])

	def __eq__(self, other):
		return self.getValue() == other.getValue()

	def getLine(self):
		line = []
		line_size = 2**len(self.offset)
		offset_size = len(self.offset)
		for i in range(line_size):
			offset = Converter.complete(Converter.convert_from_deci(i), offset_size)
			cell = Cell(self.tag, self.set, offset)
			line.append(cell)
		return line

	def __str__(self):
		return Converter.convert(self.getValue(), 2, 16)

	def __repr__(self):
		return Converter.convert(self.getValue(), 2, 16)

class AbstractCache:
	def __init__(self, archi, mem_size, n_lines, line_size, associativity, dump_strat):
		self.archi = archi
		self.mem_size = mem_size
		self.n_lines = n_lines
		self.line_size = line_size
		self.associativity = associativity

		self.offset_size = int(math.log(line_size, 2))
		self.set_size = int(math.log(mem_size/(associativity*line_size), 2))
		self.tag_size = archi - self.set_size - self.offset_size

		self.dump_strat = dump_strat

		self._cells = {}

	def checkForValue(self, data):
		set = data.getSet()
		if set in self._cells.keys():
			#set already stored in cache
			for associativity_lines in self._cells[set]:
				if data in associativity_lines:
					#data already stored in cache
					return HIT

			#data not in cache BUT set already in
			#CONF MISS
			return CONF_MISS

		else:
			#set not in cache yet
			return COMP_MISS

	def touch(self, data):
		pass

	def getLineByHighestId(self, set = None):
		h_line = None
		h_set = None
		higher = -1

		if set == None:
			for _set in self._cells.keys():
				for associativity_lines in self._cells[_set]:
					for cell in associativity_lines:
						if cell.getId() > higher:
							h_line = associativity_lines
							h_set = _set
							higher = cell.getId()

		else:
			h_set = set
			for associativity_lines in self._cells[h_set]:
				for cell in associativity_lines:
					if cell.getId() > higher:
						h_line = associativity_lines
						higher = cell.getId()

		return (h_set, h_line)

	def getLineByLowestId(self, set = None):
		l_line = None
		l_set = None
		lower = 1

		if set == None:
			for _set in self._cells.keys():
				for associativity_lines in self._cells[_set]:
					for cell in associativity_lines:
						if cell.getId() == 0:
							l_line = associativity_lines
							l_set = _set
							lower = 0
							break

						elif 1/float(cell.getId()) < lower:
							l_line = associativity_lines
							l_set = _set
							lower = 1/float(cell.getId())

					if lower == 0:
						break
				if lower == 0:
					break

		else:
			l_set = set
			for associativity_lines in self._cells[l_set]:
				for cell in associativity_lines:
					if cell.getId() == 0:
						l_line = associativity_lines
						lower = 0
						break

					elif 1/float(cell.getId()) < lower:
						l_line = associativity_lines
						lower = 1/float(cell.getId())

				if lower == 0:
					break

		return (l_set, l_line)

	def increment_cells(self, set):
		for associativity_lines in self._cells[set]:
			for data in associativity_lines:
				data.increment()

	def decrement_cells(self, set):
		for associativity_lines in self._cells[set]:
			for data in associativity_lines:
				data.decrement()

	def reset_cells_id(self, set):
		for associativity_lines in self._cells[set]:
			for data in associativity_lines:
				data.resetId()

	def loadFromData(data):
		new_line = []
		for i in range(self.line_size):
			if (i == 0):
				#load data
				new_line.append(data)
			else:
				#load next data
				new_line.append(data.next(i))

		return new_line

	def __repr__(self):
		return "<{0} {1}>".format(self.__class__.__name__, self._cells)

	def __len__(self):
		"""List length"""
		return len(self._cells)

	def __getitem__(self, i):
		"""Get a list item"""
		return self._cells[i]

	def __delitem__(self, i):
		"""Delete an item"""
		del self._cells[i]

	def __setitem__(self, i, val):
		self._cells[i] = val

	def __str__(self):
		string = "\r{\n"
		for set in self._cells.keys():
			string += f"{set}:\t[\n"
			for associativity_lines in self._cells[set]:
				string += "\t\t["
				for cell in associativity_lines:
					string += f" {Converter.convert(cell.getValue(), 2, 16)} |"
				string = string[0:-1]
				string += "]\n"
			string += "\t]\n"
		string += "}"
		return string
		#return str(self._cells)

	def __contains__(self, item):
		return bool(item in self._cells)

class DirectMappedCache(AbstractCache):
	def __init__(self, archi, mem_size, n_lines, line_size, dump_strat):
		super().__init__(archi, mem_size, n_lines, line_size, 1, dump_strat)

	def touch(self, data):
		word = Converter.complete(Converter.convert_from_deci(Converter.convert_to_deci(data)), self.archi)

		#print(self.tag_size)
		tag = word[0:self.tag_size]
		set = word[self.tag_size:self.tag_size+self.set_size]
		offset = word[-self.offset_size::]

		val = Cell(tag, set, offset)

		status = self.checkForValue(val)

		#creating the new line to store needed in case of miss
		new_line = val.getLine()

		if status == CONF_MISS:
			#managing dump strategy
			if self.dump_strat == LRU or self.dump_strat == FIFO:
				#actions for LRU or FIFO strategies
				#LRU: increment each data id in each lines of cache to mark we didn't use them
				#FIFO: increment each data id in each lines of cache to keep counting in order of arrival
				for set_to_increment in self._cells.keys():
					if set_to_increment != set:
						self.increment_cells(set_to_increment)

			elif self.dump_strat == LFU or self.dump_strat == RAND:
				#actions for LFU adn RANDOM strategies
				#do nothing
				pass

			#replace line which has the same set
			self._cells[set] = [new_line]

		elif status == COMP_MISS:
			if len(self._cells.keys()) < self.n_lines:
				#enough place in cache to add data and its following
				#managing dump strategy
				if self.dump_strat == LRU or self.dump_strat == FIFO:
					#actions for LRU or FIFO strategies
					#LRU: increment each data id in each lines of cache to mark we didn't use them
					#FIFO: increment each data id in each lines of cache to keep counting in order of arrival
					for set_to_increment in self._cells.keys():
						if set_to_increment != set:
							self.increment_cells(set_to_increment)

				elif self.dump_strat == LFU or self.dump_strat == RAND:
					#actions for LFU or RANDOM strategies
					#do nothing
					pass

				#add line
				self._cells[set] = [new_line]

			else:
				#Actually is a capacity miss
				status = CAPA_MISS
				#not enough so dumping a set line
				#managing dump strategy
				set_to_remove = None
				if self.dump_strat == LRU or self.dump_strat == FIFO:
					#actions for LRU or FIFO strategies
					#dumping the line which contains the cell with the highest id
					set_to_remove, line_to_remove = self.getLineByHighestId()

				elif self.dump_strat == RAND:
					#actions for RANDOM strategy
					set_to_remove = random.choice(self._cells.keys())

				elif self.dump_strat == LFU:
					#actions for LFU strategy
					set_to_remove, line_to_remove = self.getLineByLowestId()

				self._cells.pop(set_to_remove)
				self._cells[set] = [new_line]

		elif status == HIT:
			#update id depending on dump strat
			#managing dump strategy
			if self.dump_strat == LRU:
				#actions for LRU strategy
				#reinit id
				quit = False
				for associativity_lines in self._cells[set]:
					for cell in associativity_lines:
						if cell == val:
							self.reset_cells_id(cell.getSet())
							quit = True
							break
					if quit:
						break

			elif self.dump_strat == FIFO or self.RAND:
				#actions for FIFO or RANDOM strategies
				#do nothing
				pass

			elif self.dump_strat == LFU:
				#actions for LFU strategy
				#increment data cell id
				quit = False
				for associativity_lines in self._cells[set]:
					for cell in associativity_lines:
						if cell == val:
							cell.increment()
							quit = True
							break
					if quit:
						break

		return status

class SetAssociativeCache(AbstractCache):
	def touch(self, data):
		word = Converter.complete(Converter.convert_from_deci(Converter.convert_to_deci(data)), self.archi)

		tag = word[0:self.tag_size]
		set = word[self.tag_size:self.tag_size+self.set_size]
		offset = word[-self.offset_size::]

		val = Cell(tag, set, offset)

		status = self.checkForValue(val)

		#creating the new line to store needed in case of miss
		new_line = val.getLine()

		if status == CONF_MISS:
			#managing associativity
			if len(self._cells[set]) < self.associativity:
				#enough place so actually a COMP_MISS
				status = COMP_MISS

			else:
				#not enough place
				#managing dump strategy
				line_to_remove = None
				if self.dump_strat == LRU or self.dump_strat == FIFO:
					#actions for LRU or FIFO strategies
					#dumping line of set containing the cell with the highest id
					set_to_remove, line_to_remove = self.getLineByHighestId(set = set)

				elif self.dump_strat == RAND:
					#actions for RANDOM strategy
					line_to_remove = random.choice(self._cells[set])

				elif self.dump_strat == LFU:
					#actions for LFU strategy
					set_to_remove, line_to_remove = self.getLineByLowestId(set = set)

				self._cells[set].remove(line_to_remove)

			#enough place to store duplicated set
			#managing dump strategy
			if self.dump_strat == LRU or self.dump_strat == FIFO:
				#actions for LRU or FIFO strategies
				#LRU: increment each data id in each lines of cache to mark we didn't use them
				#FIFO: increment each data id in each lines of cache to keep counting in order of arrival
				for set_to_increment in self._cells.keys():
					if set_to_increment != set:
						self.increment_cells(set_to_increment)

			elif self.dump_strat == LFU or self.dump_strat == RAND:
				#actions for LFU adn RANDOM strategies
				#do nothing
				pass

			#append new data line
			self._cells[set].append(new_line)

		elif status == COMP_MISS:
			if len(self._cells.keys()) < self.n_lines:
				#enough place in cache to add data and its following
				#managing dump strategy
				if self.dump_strat == LRU or self.dump_strat == FIFO:
					#actions for LRU or FIFO strategies
					#LRU: increment each data id in each lines of cache to mark we didn't use them
					#FIFO: increment each data id in each lines of cache to keep counting in order of arrival
					for set_to_increment in self._cells.keys():
						if set_to_increment != set:
							self.increment_cells(set_to_increment)

				elif self.dump_strat == LFU or self.dump_strat == RAND:
					#actions for LFU or RANDOM strategies
					#do nothing
					pass

				#add line
				self._cells[set] = [new_line]

			else:
				#Actually is a capacity miss
				status = CAPA_MISS
				#not enough so dumping a set line
				#managing dump strategy
				set_to_remove = None
				if self.dump_strat == LRU or self.dump_strat == FIFO:
					#actions for LRU or FIFO strategies
					#dumping the line which contains the cell with the highest id
					set_to_remove, line_to_remove = self.getLineByHighestId()

				elif self.dump_strat == RAND:
					#actions for RANDOM strategy
					set_to_remove = random.choice(self._cells.keys())

				elif self.dump_strat == LFU:
					#actions for LFU strategy
					set_to_remove, line_to_remove = self.getLineByLowestId()

				self._cells.pop(set_to_remove)
				self._cells[set] = [new_line]

		elif status == HIT:
			#update id depending on dump strat
			#managing dump strategy
			if self.dump_strat == LRU:
				#actions for LRU strategy
				#reinit id
				quit = False
				for associativity_lines in self._cells[set]:
					for cell in associativity_lines:
						if cell == val:
							self.reset_cells_id(cell.getSet())
							quit = True
							break
					if quit:
						break

			elif self.dump_strat == FIFO or self.RAND:
				#actions for FIFO or RANDOM strategies
				#do nothing
				pass

			elif self.dump_strat == LFU:
				#actions for LFU strategy
				#increment data cell id
				quit = False
				for associativity_lines in self._cells[set]:
					for cell in associativity_lines:
						if cell == val:
							cell.increment()
							quit = True
							break
					if quit:
						break

		return status

class FullyAssociativeCache(AbstractCache):
	def __init__(self, archi, mem_size, n_lines, line_size, dump_strat):
		super().__init__(archi, mem_size, n_lines, line_size, FULLY, dump_strat)
		self.set_size = 0
		self.tag_size = archi - self.offset_size

	def touch(self, data):
		word = Converter.complete(Converter.convert_from_deci(Converter.convert_to_deci(data)), self.archi)

		tag = word[0:self.tag_size]
		set = ""
		offset = word[-self.offset_size::]

		val = Cell(tag, set, offset)

		status = self.checkForValue(val)

		#creating the new line to store needed in case of miss
		new_line = val.getLine()

		if status == CONF_MISS:
			#IMPOSSIBLE
			raise Exception("Conflict Miss in Fully Associative cache. Impossible.")

		elif status == COMP_MISS:
			if len(self._cells.keys()) < self.n_lines:
				#enough place in cache to add data and its following
				#managing dump strategy
				if self.dump_strat == LRU or self.dump_strat == FIFO:
					#actions for LRU or FIFO strategies
					#LRU: increment each data id in each lines of cache to mark we didn't use them
					#FIFO: increment each data id in each lines of cache to keep counting in order of arrival
					for set_to_increment in self._cells.keys():
						if set_to_increment != set:
							self.increment_cells(set_to_increment)

				elif self.dump_strat == LFU or self.dump_strat == RAND:
					#actions for LFU or RANDOM strategies
					#do nothing
					pass

				#add line
				self._cells[set].append(new_line)

			else:
				#Actually is a capacity miss
				status = CAPA_MISS
				#not enough so dumping a set line
				#managing dump strategy
				line_to_remove = None
				if self.dump_strat == LRU or self.dump_strat == FIFO:
					#actions for LRU or FIFO strategies
					#dumping the line which contains the cell with the highest id
					set_to_remove, line_to_remove = self.getLineByHighestId(set = set)

				elif self.dump_strat == RAND:
					#actions for RANDOM strategy
					line_to_remove = random.choice(self._cells[set])

				elif self.dump_strat == LFU:
					#actions for LFU strategy
					set_to_remove, line_to_remove = self.getLineByLowestId(set = set)

				self._cells[set].remove(line_to_remove)
				self._cells[set].append(new_line)

		elif status == HIT:
			#update id depending on dump strat
			#managing dump strategy
			if self.dump_strat == LRU:
				#actions for LRU strategy
				#reinit id
				quit = False
				for associativity_lines in self._cells[set]:
					for cell in associativity_lines:
						if cell == val:
							cell.resetId()
							quit = True
							break
					if quit:
						break

			elif self.dump_strat == FIFO or self.RAND:
				#actions for FIFO or RANDOM strategies
				#do nothing
				pass

			elif self.dump_strat == LFU:
				#actions for LFU strategy
				#increment data cell id
				quit = False
				for associativity_lines in self._cells[set]:
					for cell in associativity_lines:
						if cell == val:
							cell.increment()
							quit = True
							break
					if quit:
						break

		return status