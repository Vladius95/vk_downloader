import json

class Data_user:
	
	def __read(self):
		try:
			data = json.load(open('data_user.json'))
		except IOError:
			data = []

		return data

	def __write(self, data):
		with open('data_user.json', 'w') as file:
				json.dump(data, file, indent=2)

	def log_in(self, login, pas):
		person = [{
			'login': login,
			'pas': pas
		}]
		self.__write(person)

	def log_out(self, name_login):
		self.__write([{}])

	def check(self):
		data = self.__read()

		if len(data) > 0:
			return True
		else:
			return False

	def get_data(self):
		data = self.__read()
		return data