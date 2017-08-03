import json

class Data_user:
	
	def _read(self):
		try:
			data = json.load(open('data_user.json'))
		except IOError:
			data = []

		return data

	def _write(self, data):
		with open('data_user.json', 'w') as file:
				json.dump(data, file, indent=2)

	def log_in(self, login, pas):
		person = [{
			'login': login,
			'pas': pas
		}]
		self._write(person)

	def log_out(self):
		self._write([{}])

	def check(self):
		data = self._read()
		try:
			if len(data[0]) > 0:
				return True
			else:
				return False
		except IndexError:
			return False

	def get_data(self):
		data = self._read()
		return data