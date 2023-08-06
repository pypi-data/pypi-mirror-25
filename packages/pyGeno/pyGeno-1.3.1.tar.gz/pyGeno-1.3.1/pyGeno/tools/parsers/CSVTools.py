import os, types, collections

class EmptyLine(Exception) :
	"""Raised when an empty or comment line is found (dealt with internally)"""

	def __init__(self, lineNumber) :
		message = "Empty line: #%d" % lineNumber 
		Exception.__init__(self, message)
		self.message = message

	def __str__(self) :
		return self.message

def removeDuplicates(inFileName, outFileName) :
	"""removes duplicated lines from a 'inFileName' CSV file, the results are witten in 'outFileName'"""
	f = open(inFileName)
	legend = f.readline()
	
	data = ''
	h = {}
	h[legend] = 0
	
	lines = f.readlines()
	for l in lines :
		if not h.has_key(l) :
			h[l] = 0
			data += l
			
	f.flush()
	f.close()
	f = open(outFileName, 'w')
	f.write(legend+data)
	f.flush()
	f.close()

def catCSVs(folder, ouputFileName, removeDups = False) :
	"""Concatenates all csv in 'folder' and wites the results in 'ouputFileName'. My not work on non Unix systems"""
	strCmd = r"""cat %s/*.csv > %s""" %(folder, ouputFileName)
	os.system(strCmd)

	if removeDups :
		removeDuplicates(ouputFileName, ouputFileName)

def joinCSVs(csvFilePaths, column, ouputFileName, separator = ',') :
	"""csvFilePaths should be an iterable. Joins all CSVs according to the values in the column 'column'. Write the results in a new file 'ouputFileName' """
	
	res = ''
	legend = []
	csvs = []
	
	for f in csvFilePaths :
		c = CSVFile()
		c.parse(f)
		csvs.append(c)
		legend.append(separator.join(c.legend.keys()))
	legend = separator.join(legend)
	
	lines = []
	for i in range(len(csvs[0])) :
		val = csvs[0].get(i, column)
		line = separator.join(csvs[0][i])
		for c in csvs[1:] :
			for j in range(len(c)) :
				if val == c.get(j, column) :
					line += separator + separator.join(c[j])
					
		lines.append( line )
	
	res = legend + '\n' + '\n'.join(lines)
	
	f = open(ouputFileName, 'w')
	f.write(res)
	f.flush()
	f.close()
	
	return res

class CSVEntry(object) :
	"""A single entry in a CSV file"""
	
	def __init__(self, csvFile, lineNumber = None) :
		
		self.csvFile = csvFile
		self.data = []
		if lineNumber != None :
			self.lineNumber = lineNumber
			
			tmpL = csvFile.lines[lineNumber].replace('\r', '\n').replace('\n', '')
			if len(tmpL) == 0 or tmpL[0] in ["#", "\r", "\n", csvFile.lineSeparator] :
				raise EmptyLine(lineNumber)

			tmpData = tmpL.split(csvFile.separator)

			tmpDatum = []
			for d in tmpData :
				sd = d.strip()
				if len(tmpDatum) > 0 or (len(sd) > 0 and sd[0] == csvFile.stringSeparator) :
					tmpDatum.append(sd)
				
					if len(sd) > 0 and sd[-1] == csvFile.stringSeparator :
						self.data.append(csvFile.separator.join(tmpDatum))
						tmpDatum = []
				else :
					self.data.append(sd)
		else :
			self.lineNumber = len(csvFile)
			for i in range(len(self.csvFile.legend)) :
				self.data.append('')

	def commit(self) :
		"""commits the line so it is added to a file stream"""
		self.csvFile.commitLine(self)

	def __iter__(self) :
		self.currentField = -1
		return self
	
	def next(self) :
		self.currentField += 1
		if self.currentField >= len(self.csvFile.legend) :
			raise StopIteration
			
		k = self.csvFile.legend.keys()[self.currentField]
		v = self.data[self.currentField]
		return k, v

	def __getitem__(self, key) :
		"""Returns the value of field 'key'"""
		try :
			indice = self.csvFile.legend[key.lower()]
		except KeyError :
			raise KeyError("CSV File has no column: '%s'" % key)
		
		return self.data[indice]

	def __setitem__(self, key, value) :
		"""Sets the value of field 'key' to 'value' """
		try :
			field = self.csvFile.legend[key.lower()]
		except KeyError :
			self.csvFile.addField(key)
			field = self.csvFile.legend[key.lower()]
			self.data.append(str(value))
		else :
			try:
				self.data[field] = str(value)
			except Exception as e:
				for i in xrange(field-len(self.data)+1) :
					self.data.append("")
				self.data[field] = str(value)

	def __repr__(self) :
		return "<line %d: %s>" %(self.lineNumber, str(self.data))
		
	def __str__(self) :
		return self.csvFile.separator.join(self.data)
	
class CSVFile(object) :
	"""
	Represents a whole CSV file::
		
		#reading
		f = CSVFile()
		f.parse('hop.csv')
		for line in f :
			print line['ref']

		#writing, legend can either be a list of a dict {field : column number}
		f = CSVFile(legend = ['name', 'email'])
		l = f.newLine()
		l['name'] = 'toto'
		l['email'] = "hop@gmail.com"
		
		for field, value in l :
			print field, value

		f.save('myCSV.csv')		
	"""
	
	def __init__(self, legend = [], separator = ',', lineSeparator = '\n') :
		
		self.legend = collections.OrderedDict()
		for i in range(len(legend)) :
			if legend[i].lower() in self.legend :
				raise  ValueError("%s is already in the legend" % legend[i].lower())
			self.legend[legend[i].lower()] = i
		self.strLegend = separator.join(legend)

		self.filename = ""
		self.lines = []	
		self.separator = separator
		self.lineSeparator = lineSeparator
		self.currentPos = -1
	
		self.streamFile = None
		self.writeRate = None
		self.streamBuffer = None
		self.keepInMemory = True

	def addField(self, field) :
		"""add a filed to the legend"""
		if field.lower() in self.legend :
			raise  ValueError("%s is already in the legend" % field.lower())
		self.legend[field.lower()] = len(self.legend)
		if len(self.strLegend) > 0 :
			self.strLegend += self.separator + field
		else :
			self.strLegend += field
			
	def parse(self, filePath, skipLines=0, separator = ',', stringSeparator = '"', lineSeparator = '\n') :
		"""Loads a CSV file"""
		
		self.filename = filePath
		f = open(filePath)
		if lineSeparator == '\n' :
			self.lines = f.readlines()
		else :
			self.lines = f.read().split(lineSeparator)
		f.flush()
		f.close()
		
		self.separator = separator
		self.lineSeparator = lineSeparator
		self.stringSeparator = stringSeparator
		self.legend = collections.OrderedDict()
		
		i = 0
		for c in self.lines[0].lower().replace(stringSeparator, '').split(separator) :
			legendElement = c.strip()
			if legendElement not in self.legend :
				self.legend[legendElement] = i
			i+=1
	
		self.strLegend = self.lines[0].replace('\r', '\n').replace('\n', '')
		sk = skipLines+1
		for l in self.lines :
			if l[0] == "#" :
				sk += 1
			else :
				break

		self.header = self.lines[:sk]
		self.lines = self.lines[sk:]
	

	def streamToFile(self, filename, keepInMemory = False, writeRate = 1) :
		"""Starts a stream to a file. Every line must be committed (l.commit()) to be appended in to the file.

		If keepInMemory is set to True, the parser will keep a version of the whole CSV in memory, writeRate is the number
		of lines that must be committed before an automatic save is triggered.
		"""
		if len(self.legend) < 1 :
			raise ValueError("There's no legend defined")

		try :
			os.remove(filename)
		except :
			pass
		
		self.streamFile = open(filename, "a")
		self.writeRate = writeRate
		self.streamBuffer = []
		self.keepInMemory = keepInMemory

		self.streamFile.write(self.strLegend + "\n")

	def commitLine(self, line) :
		"""Commits a line making it ready to be streamed to a file and saves the current buffer if needed. If no stream is active, raises a ValueError"""
		if self.streamBuffer is None :
			raise ValueError("Commit lines is only for when you are streaming to a file")

		self.streamBuffer.append(line)
		if len(self.streamBuffer) % self.writeRate == 0 :
			for i in xrange(len(self.streamBuffer)) :
				self.streamBuffer[i] = str(self.streamBuffer[i])
			self.streamFile.write("%s\n" % ('\n'.join(self.streamBuffer)))
			self.streamFile.flush()
			self.streamBuffer = []

	def closeStreamToFile(self) :
		"""Appends the remaining commited lines and closes the stream. If no stream is active, raises a ValueError"""
		if self.streamBuffer is None :
			raise ValueError("Commit lines is only for when you are streaming to a file")

		for i in xrange(len(self.streamBuffer)) :
			self.streamBuffer[i] = str(self.streamBuffer[i])
		self.streamFile.write('\n'.join(self.streamBuffer))
		self.streamFile.close()

		self.streamFile = None
		self.writeRate = None
		self.streamBuffer = None
		self.keepInMemory = True

	def _developLine(self, line) :
		stop = False
		while not stop :
			try :
				if self.lines[line].__class__ is not CSVEntry :
					devL = CSVEntry(self, line)
					stop = True
				else :
					devL = self.lines[line]
					stop = True
			except EmptyLine as e :
				del(self.lines[line])
					
		self.lines[line] = devL
	
	def get(self, line, key) :
		self._developLine(line)
		return self.lines[line][key]

	def set(self, line, key, val) :
		self._developLine(line)
		self.lines[line][key] = val
	
	def newLine(self) :
		"""Appends an empty line at the end of the CSV and returns it"""
		l = CSVEntry(self)
		if self.keepInMemory :
			self.lines.append(l)
		return l
	
	def insertLine(self, i) :
		"""Inserts an empty line at position i and returns it"""
		self.data.insert(i, CSVEntry(self))
		return self.lines[i]
	
	def save(self, filePath) :
		"""save the CSV to a file"""
		self.filename = filePath
		f = open(filePath, 'w')
		f.write(self.toStr())
		f.flush()
		f.close()

	def toStr(self) :
		"""returns a string version of the CSV"""
		s = [self.strLegend]
		for l in self.lines :
			s.append(str(l))
		return self.lineSeparator.join(s)
	
	def __iter__(self) :
		self.currentPos = -1
		return self
	
	def next(self) :
		self.currentPos += 1
		if self.currentPos >= len(self) :
			raise StopIteration
			
		self._developLine(self.currentPos)
		return self.lines[self.currentPos]
	
	def __getitem__(self, line) :
		try :
			if self.lines[line].__class__ is not CSVEntry :
				self._developLine(line)
		except AttributeError :
			for l in xrange(len(self.lines[line])) :
				self._developLine(l + line.start)

			# start, stop = line.start, line.stop
			# if start is None :
			# 	start = 0
			
			# if stop is None :
			# 	stop = 0

			# for l in xrange(start, stop) :
			# 	self._developLine(l)

		return self.lines[line]

	def __len__(self) :
		return len(self.lines)
