import others
import re

def show_dict(d, key):
	while True:
		for i, value in enumerate(d):
			print('{}. {}'.format(i+1, others.scrape(value[key])))

		answer = input('>> ')
		if answer == '-1':
			return

		numbers =  re.findall(r'\d+', answer)
		if len(numbers) == 0:
			print('There are no digits, try again')
			continue

		for i in range(len(numbers)):
			numbers[i] = int(numbers[i])
			if numbers[i] < 1 or numbers[i] > len(d):
				print('There are digits out of range, try again')
				break
		else:
			return list(set(numbers))
		"""digit = ''
		list_numbers = []
		for i in answer:
			if i.isdigit():
				digit += i
			elif len(digit) == 0:
				continue
			else:
				list_numbers.append(int(digit))
				digit = ''
		if len(digit) != 0:
			list_numbers.append(int(digit))

		if len(list_numbers) == 0:
			print('There are no digits, try again')
			continue
		if list_numbers == [0] and len(list_numbers) == 1:
			return [i for i in range(1, len(d)+1)]

		for i in list_numbers:
			if i not in range(1, len(d)+1):
				print('There is no number {}, try again'.format(i))
				break
		else:
			break"""
	#return list(set(numbers))