import string

def scrape(text):
	chars = string.digits + string.punctuation + string.whitespace
	return ''.join([i for i in text if i.isalpha() or i in chars])

class ProgressBar:
	def __init__(self, description, subject):
		self._subject = subject
		self._description = description
		if self._description.find(' is downloading') > 40:
			self._description = self._description[:40] + '... is downloading'
		self._length = len(subject)
		self._counter = 0
		self._progress_bar = ['[', ']']
		for i in range(1, 11):
			self._progress_bar.insert(i, '-')

	def __iter__(self):
		return self

	def __next__(self):
		if self._counter == self._length:
			print(' '*(len(self._description) + len(self._progress_bar) + 9), end='\r')
			raise StopIteration

		progress = (self._counter+1)/self._length
		position = int(progress*100)//10
		if position >= 1:
			self._progress_bar.pop(position)
			self._progress_bar.insert(position, '#')

		print(self._description, ''.join(self._progress_bar), '{:.2%}'.format(progress), 
			end='\r')
		self._counter += 1
		return self._subject[self._counter-1]