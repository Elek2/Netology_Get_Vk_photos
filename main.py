from datetime import datetime
import requests
from pprint import pprint
import json


class GetPhotos:
	def __init__(self, vk_token, ya_token):
		self.vk_token = vk_token
		self.base_VK_url = 'https://api.vk.com/method/'
		self.base_VK_params = {
			'access_token': self.vk_token,
			'v': '5.131',
		}
		self.ya_token = ya_token
		self.base_Ya_url = 'https://cloud-api.yandex.net/v1/disk/'
		self.Ya_headers = {
			'Content-Type': 'application/json',
			'Authorization': f'OAuth {self.ya_token}'
		}

	def get_user_name(self, user_id):
		end_url = 'users.get'
		VK_params = {
			'user_ids': user_id,
		}
		url = self.base_VK_url + end_url
		response = requests.get(url, params={**self.base_VK_params, **VK_params}).json()['response']
		return response[0]['first_name'] + '_' + response[0]['last_name']


	def get_photos(self, user_id):
		end_url = 'photos.get'
		VK_params = {
			'owner_id': user_id,
			'album_id': 'profile',
			'extended': 1,
			'count': 1,
			'photo_sizes': 1
		}
		url = self.base_VK_url + end_url
		response = requests.get(url, params={**self.base_VK_params, **VK_params}).json()['response']
		photos = self._reformat_photos_list(response['items'])

		# for photo in photos:
		# self._upload(photos[0]['name'], photos[0]['photo_url'])

		# photo_json = [{"file_name": photo['name'], "size": photo['size_type']} for photo in photos]
		pprint(response)

	# return photos

	def _reformat_photos_list(self, photos_list):
		colums = ['name', 'size_type', 'photo_url']
		likes_list = [photo['likes']['count'] for photo in photos_list]
		reformat_photos_list = []
		for photo in photos_list:
			max_photo_size = max(photo['sizes'], key=lambda x: x['type'])
			max_photo = list(filter(lambda x: x['type'] == max_photo_size['type'], photo['sizes']))
			photo['photo_url'] = max_photo[0]['url']
			photo['size_type'] = max_photo[0]['type']

			if likes_list.count(photo["likes"]['count']) > 1:
				date = str(datetime.utcfromtimestamp(photo["date"]).strftime('%Y-%m-%d'))
				name = f'{str(photo["likes"]["count"])}_{date}.jpg'
			else:
				name = f'{str(photo["likes"]["count"])}.jpg'
			photo['name'] = name
			photo['likes'] = photo['likes']['count']
			photo = {key: value for key, value in photo.items() if key in colums}
			reformat_photos_list.append(photo)
		return reformat_photos_list

	def _create_folder_disk(self, file_name, url):
		upload_url = 'https://cloud-api.yandex.net/v1/disk/resources'
		headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.Ya_token}'}
		folder_name = "VK_fhotos"
		params = {"path": f"{folder_name}/{file_name}", "url": url}
		response = requests.post(upload_url, headers=headers, params=params)
		print(response)

	def _upload_to_disk(self, file_name, url):
		upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
		headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.Ya_token}'}
		folder_name = "VK_fhotos"
		params = {"path": f"{folder_name}/{file_name}", "url": url}
		response = requests.post(upload_url, headers=headers, params=params)
		print(response)
# return


if __name__ == '__main__':

	VK_token = open('VK_token.txt', 'r').read()
	Ya_token = open('Ya_token.txt', 'r').read()

	photo_bot = GetPhotos(VK_token, Ya_token)
	photos_list = photo_bot.get_user_name(36140)


