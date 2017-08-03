import os
import requests
from bs4 import BeautifulSoup

class Downloader:
	def __init__(self):
		self._path = os.path.abspath('Downloads')+os.sep

	def create_dir(self, args):
		if not os.path.exists(self._path+os.path.join(*args)):
			os.makedirs(self._path+os.path.join(*args))
			return False
		return True

	def _get_content(self, content):
		sizes = ['src_xxxbig', 'src_xxbig', 'src_xbig', 'src_big', 'src', 'src_small']
		for size in sizes:
			try:
				return requests.get(content[size]).content
			except KeyError:
				continue		

	def download_photo(self, photo, args):
		with open(self._path+os.sep.join(args)+'.jpg', 'wb') as file_jpg:
			file_jpg.write(self._get_content(photo))

	def check_download(self, link):
		html = requests.get(link).text
		soup = BeautifulSoup(html, 'html.parser')
		try:
			video_URL = soup.find('div', id='page_wrap').find('source').get('src').split('?')[0]
			return True
		except AttributeError:
			return False

	def download_video(self, link, args):
		html = requests.get(link).text
		soup = BeautifulSoup(html, 'html.parser')
		
		video_URL = soup.find('div', id='page_wrap').find('source').get('src').split('?')[0]
		response = requests.get(video_URL, stream=True)

		with open(self._path+'{path}.mp4'.format(path=os.sep.join(args)), 'wb') as video_file:
			for chunk in response.iter_content(1024000*4):
				video_file.write(chunk)