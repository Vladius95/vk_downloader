import vk
import sys
import os
import downloads
import others
import time
import menu
from vk.exceptions import VkAuthError, VkAPIError
from abc import ABCMeta, abstractmethod
from data import DataUser

APP_ID = 6109861

class DeletedError(Exception):
	pass

class NoUserError(Exception):
	pass

class NoCommunityError(Exception):
	pass

def singleton(cls):
	instances = {}
	def getinstance():
		if cls not in instances:
			instances[cls] = cls()
		return instances[cls]
	return getinstance

@singleton
class Auth:

	def __init__(self):
		user = DataUser()
		entered = False
		while True:
			if user.isHasData():
				data = user.getData()
				login = data[0]['login']
				if not entered:
					tempPas = 'grekpridurok1488' #input('Password (0 - log out): ')
					if tempPas == '0':
						self.log_out()
						continue
					elif user.checkPas(tempPas):
						pas = tempPas
						entered = True
					else:
						print('Invalid password. Try again')
						continue
				else:
					pas = tempPas
			else:
				print('Autorization')
				print('Enter your mail and password')
				login = input('Mail: ')
				pas = input('Password: ')
			try:
				session = vk.AuthSession(app_id=APP_ID, user_login=login, user_password=pas, scope='friends,photos,video')
				self._vk = vk.API(session)
				user.logIn(login, pas)
				break
			except VkAuthError:
				print('Invalid login or password, try again')

	def get_session(self):
		return self._vk

	def log_out(self):
		DataUser().logOut()

class ObjectVK(metaclass=ABCMeta):

	@abstractmethod
	def get_name(self):
		pass

	@abstractmethod
	def get_id(self):
		pass

	@abstractmethod
	def show_info(self):
		pass

	@abstractmethod
	def download_photos(self):
		pass

	@abstractmethod
	def download_videos(self):
		pass

class Media(metaclass=ABCMeta):

	@abstractmethod
	def get_albums(self):
		pass

class Photos(Media):
	def __init__(self, ID, relations):
		self._id = ID
		self._vk = relations
		try:
			self._albums = self._vk.photos.getAlbums(owner_id=self._id, need_system=1, photo_sizes=1)
		except VkAPIError:
			self._albums = None

	def get_albums(self):
		return self._albums

	def download_albums(self, numbers_albums, path):
		dl = downloads.Downloader(path)
		
		albums = [self._albums[i-1] for i in numbers_albums]
		path.append(None)
		for item, album in enumerate(albums):
			photos = self._vk.photos.get(owner_id=self._id, album_id=album['aid'])
			title_album = others.scrape(album['title'])
			path[-1] = title_album
			dl.set_path(path)

			if dl.create_dir():
				print('The album {} already exist'.format(title_album))
				time.sleep(1)
			elif album['size'] == 0:
				print('The album {} is empty'.format(title_album))
				time.sleep(1)
			else:
				for photo in others.ProgressBar('({}/{}). {} is downloading'.format(item, len(albums), title_album), photos):
					dl.download_photo(photo, str(photo['pid']))

				print('The album {} is downloaded'.format(title_album))

class Videos(Media):
	def __init__(self, ID, relations):
		self._vk = relations
		self._id = ID
		self._albums = self._vk.video.getAlbums(owner_id=self._id, need_system=1)[1:]

	def get_albums(self):
		return self._albums

	def get_videos(self):
		available_videos = []
		videos = []
		print('Please, wait. Videos are checked for download availability')

		for album in self._albums:
			try:
				temp_videos = self._vk.video.get(owner_id=self._id, album_id=album['album_id'])
			except VkAPIError:
				return []
			count = temp_videos[0]

			if count > 100:
				count -= 100
				count_offset = 100
				while True:
					if count <= 100:
						temp_videos = self._vk.video.get(owner_id=self._id, album_id=album['album_id'],
							count=count, offset=count_offset)
						videos.extend(temp_videos[1:])
						break
					else:
						temp_videos = self._vk.video.get(owner_id=self._id, album_id=album['album_id'],
							count=100, offset=count_offset)
						videos.extend(temp_videos[1:])
						count -= 100
						count_offset += 100
			else:
				videos.extend(temp_videos[1:])
			
		dl = downloads.Downloader()
		for video in videos:
			if dl.check_download(video['player']):
				if video['title'] not in [video['title'] for video in available_videos]:
					available_videos.append(video)

		return available_videos

	def download_videos(self, videos, path):
		dl = downloads.Downloader(path)
		dl.create_dir()
		number = len(videos)

		for item, video in enumerate(videos):
			title = others.scrape(video['title'])
			print('({}/{}) {} is downloading...'.format(item+1, number, title))
			dl.download_video(video['player'], title)

			print('{} is downloaded'.format(title))

class User(ObjectVK):
	def __init__(self, ID):
		try:
			self._vk = Auth().get_session()
			self._user = self._vk.users.get(user_ids=ID, fields='sex,city,country,bdate,about,activities, \
				books,education,games,contacts,country,interests,counters,tv,followers_count,movies,music')[0]
			self._id = self._user['uid']
			self._name = others.scrape(self._user['first_name'] + ' ' + self._user['last_name'])
		except VkAPIError:
			raise NoUserError
			
	def get(self, field):
		return self._user[field]

	@classmethod
	def get_id(cls, ID):
		return cls(ID).get('uid')

	@classmethod
	def get_name(cls, ID):
		return others.scrape(cls(ID).get('first_name') + ' ' + cls(ID).get('last_name'))

	def show_info(self):
		country_id = self._user['country']
		if country_id != 0:
			self._user['country'] = self._vk.database.getCountriesById(country_ids=country_id)[0]['name']

		city_id = self._user['city']
		if city_id != 0:
			self._user['city'] = self._vk.database.getCitiesById(city_ids=city_id)[0]['name']

		sex_id = self._user['sex']
		self._user['sex'] = 'women' if sex_id == 1 else 'men' if sex_id == 2 else 0

		try:
			if 'university' in self._user.keys():
				un_id = self._user['university']
				faculty_id = self._user['faculty']
				faculties = self._vk.database.getFaculties(university_id=un_id)

				for faculty in faculties[1:]:
					if faculty['id'] == faculty_id:
						self._user['faculty_name'] = faculty['title']
						break
		except VkAPIError:
			pass


		for field, info in self._user.items():
			try:
				if len(info) != 0:
					if field == 'counters':
						for i, j in info.items():
							print(i.capitalize(), str(j), sep=': ', end='\n\n')
					else:
						print(field.capitalize(), info, sep=': ', end='\n\n')
			except TypeError:
				continue

	def download_photos(self):
		vk_photos = self.PhotosUser(self._id, self._vk)
					
		print(self._name)
		print('Select the numbers of the albums you want to download.\n0 - to download all. -1 - back')
		echo_user_photo = menu.show_dict(vk_photos.get_albums(), 'title')
		if echo_user_photo is not None:
			vk_photos.download_albums(echo_user_photo, [User.get_name(self._id), 'Photos'])

	def download_videos(self):
		vk_videos = self.VideosUser(self._id, self._vk)
		videos = vk_videos.get_videos()
		if videos is None:
			print('No videos available')
			return

		print(self._name)
		print('Select the numbers of the available videos you want to download.\n0 - to download all. -1 - back')
		echo_com_videos = menu.show_dict(videos, 'title')
		if echo_com_videos is not None:
			vk_videos.download_videos([videos[i-1] for i in echo_com_videos], [User.get_name(self._id), 'Videos'])

	class PhotosUser(Photos):
		def __init__(self, ID, relations):
			self._id = User.get_id(ID)
			super().__init__(self._id, relations)
	

	class VideosUser(Videos):
		def __init__(self, ID, relations):
			self._id = User.get_id(ID)
			super().__init__(ID, relations)


class Community(ObjectVK):
	def __init__(self, ID):
		try:
			self._vk = Auth().get_session()
			self._group = self._vk.groups.getById(group_id=ID, 
				fields='description,members_count,deactivated,counters')[0]
			self._name = self._group['name']
			self._id = self._group['gid']
			if self._name == 'DELETED':
				raise DeletedError
		except VkAPIError:
			print('There is no such community')
			raise NoCommunityError

	def get(self, field):
		return self._group[field]

	@classmethod
	def get_id(cls, ID):
		return cls(ID).get('gid')

	@classmethod
	def get_name(cls, ID):
		return others.scrape(cls(ID).get('name'))

	def show_info(self):
		fields = {}
		fields['Name'] = others.scrape(self._name)
		fields['Count members'] = str(self._group['members_count'])
		fields['Type'] = self._group['type']
		fields['Description'] = self._group['description'] if len(self._group['description']) != 0 else 'No description'
		if self._group['counters'] is not None:
			for key, value in self._group['counters'].items():
				fields[key.capitalize()] = str(value)

		for key, value in fields.items():
			print(key + ': ' + value)

	def download_photos(self):
		vk_photos = self.PhotosCommunity(self._id, self._vk)
		albums = vk_photos.get_albums()
		if albums is None:
			print('No albums')
			return

		print(self._name)
		print('Select the numbers of the available videos you want to download.\n0 - to download all. -1 - back')
		echo_com_photo = menu.show_dict(albums, 'title')
			
		vk_photos.download_albums(echo_com_photo, [Community.get_name(self._id[1:]), 'Images'])

	def download_photo_posts(self, count):
		vk_post_photos = self.PhotosCommunity(self._id, self._vk)
		vk_post_photos.download_posts(count)

	def download_videos(self):
		vk_videos = self.VideosCommunity(self._id, self._vk)
		videos = vk_videos.get_videos()
		if len(videos) == 0:
			print('No videos available')
			return 

		print(others.scrape(self._name))
		print('Select the numbers of the available videos you want to download.\n0 - to download all. -1 - back')
		echo_com_videos = menu.show_dict(videos, 'title')

		vk_videos.download_videos([videos[i-1] for i in echo_com_videos], [Community.get_name(self._id[1:]), 'Videos'])

	class PhotosCommunity(Photos):
		def __init__(self, ID, relations):
			self._id = '-'+str(ID)
			super().__init__(self._id, relations)
			
		def _get_posts(self, count):
			posts = []
			count_offset = 0
			while True:
				if count <= 100:
					temp_posts = self._vk.wall.get(owner_id=self._id, count=count, offset=count_offset)[1:]
					
					for post in temp_posts:
						try:
							posts.extend(post['attachments'])
						except KeyError:
							continue
					return posts
				else:
					temp_posts = self._vk.wall.get(owner_id=self._id, count=100, offset=count_offset)[1:]
					for post in temp_posts:
						try:
							posts.extend(post['attachments'])
						except KeyError:
							continue
					count_offset += 100
					count -= 100
			return posts

		def download_posts(self, count):
			photos_wall = self._get_posts(count)
			
			path = [Community.get_name(self._id[1:]), 'Images', 'Posts' + str(count)]
			dl = downloads.Downloader(path)
			dl.create_dir()
			count_images = 0
			for photo in others.ProgressBar('Images from the posts are downloading', photos_wall):
				try:
					dl.download_photo(photo['photo'], str(photo['photo']['pid']))
					count_images += 1
				except KeyError:
					continue	
				
			print('{} images from {} posts is downloaded'.format(count_images, count))

	class VideosCommunity(Videos):
		def __init__(self, ID, relations):
			self._id = '-' + str(ID)
			super().__init__(self._id, relations)