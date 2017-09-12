import others
import re

def show_dict(d, key):
	while True:
		for i, value in enumerate(d):
			print('{}. {}'.format(i+1, others.scrape(value[key])))

		answer = input('>> ')
		if answer == '-1':
			return

		if answer == '0':
			return [i for i in range(1, len(d)+1)]

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