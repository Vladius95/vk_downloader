import vk_expansion

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#options
#///////////////////////////////////////////////////////////////////////////////
MAIN = ['Search for user by id', 'Communities', 'Log out', 'Exit']			  #|
USER = ['Private info', 'Download photos', 'Download videos', 'Back']		  #|
COMMUNITIES = ['Description', 'Download albums', 'Download images from posts',#|
				'Download videos', 'Back'] 									  #|
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def show(options):
	while True:
		try:
			temp = {i+1: option for i, option in enumerate(options)}
			for i, j in temp.items():
				print('{}. {}'.format(i, j))
			answer = int(input('>> '))

			return temp[answer]
		except KeyError:
			print('There are no such numbers, try again')

def main():
	
	while True:
		try:
			echo_main = show(MAIN)
		except ValueError:
			print('There are no such numbers, try again')
			continue

		if echo_main == 'Search for user by id':
			echo_user_id = input('Enter id\n>> ')
			try:
				vk_user = vk_expansion.User(echo_user_id)
			except vk_expansion.UserError:
				print('There is no such user')
				continue
			name_user = vk_user.get_name(echo_user_id)

			while True:
				print(name_user)
				try:
					echo_user = show(USER)
				except ValueError:
					print('There are no such numbers, try again')
					continue

				if echo_user == 'Private info':
					vk_user.show_info()

				elif echo_user == 'Download photos':
					vk_user.download_photos()

				elif echo_user == 'Download videos':
					vk_user.download_videos()

				elif echo_user == 'Back':
					break

		elif echo_main == 'Communities':
			echo_com_id = input('Enter id of community\n>> ')
			try:
				vk_com = vk_expansion.Community(echo_com_id)
			except vk_expansion.DeletedError:
				print('Community is deactivated')
				continue
			name_com = vk_com.get_name(echo_com_id)

			while True:
				print(name_com)
				echo_com = show(COMMUNITIES)

				if echo_com == 'Description':
					vk_com.show_info()

				elif echo_com == 'Download albums':
					vk_com.download_photos()

				elif echo_com == 'Download images from the posts':
					try:
						count_posts = int(input('Enter count post for download from\n>> '))
					except ValueError:
						print('Digits must be integer')
						continue
					vk_com.download_photo_posts(count_posts)

				elif echo_com == 'Download videos':
					vk_com.download_videos()
					
				elif echo_com == 'Back':
					break

		elif echo_main == 'Log out':
			pass

		elif echo_main == 'Exit':
			break

if __name__ == '__main__':
	main()