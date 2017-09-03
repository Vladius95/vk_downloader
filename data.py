import json
import hashlib

class DataUser:
	
	def _read(self):
		try:
			data = json.load(open('data_user.json'))
		except IOError:
			data = []
		return data

	def _write(self, data):
		with open('data_user.json', 'w') as file:
			json.dump(data, file, indent=2)

	def logIn(self, login, pas):
		person = [{
			'login': login,
			'pas': hashlib.md5(pas.encode()).hexdigest()
		}]
		self._write(person)

	def logOut(self):
		self._write([{}])

	def isHasData(self):
		data = self._read()
		try:
			if len(data[0]) > 0:
				return True
			else:
				return False
		except IndexError:
			return False

	def checkPas(self, pas):
		data = self._read()
		return True if data[0]['pas'] == hashlib.md5(pas.encode()).hexdigest() else False

	def getData(self):
		data = self._read()
		return data