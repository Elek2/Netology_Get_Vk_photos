from datetime import datetime
import requests
import json
from tqdm import tqdm
import logging


class GetPhotos:
	def __init__(self, vk_id, ya_token):
		self.vk_id = vk_id
		self.vk_token = open('VK_token.txt', 'r').read()
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

		logging.basicConfig(
			filename="logs.log",
			level=logging.INFO,
			format="%(asctime)s %(levelname)s %(message)s"
		)

	def _get_name(self):
		end_url = 'users.get'
		vk_params = {
			'user_ids': self.vk_id,
		}
		url = self.base_VK_url + end_url
		try:
			response = requests.get(url, params={**self.base_VK_params, **vk_params}).json()['response']
			full_name = response[0]['first_name'] + '_' + response[0]['last_name']
			logging.info(f"Имя пользователя: {full_name}")
			if full_name == 'DELETED_':
				logging.error("Пользователь удален")
			if not response[0]['can_access_closed']:
				logging.error("Приватный пользователь. Доступ к фото запрещен")
			return full_name
		except IndexError:
			logging.error("Имя пользователя не получено")

	@property
	def _get_vk_photos(self):
		end_url = 'photos.get'
		vk_params = {
			'owner_id': self.vk_id,
			'album_id': 'profile',
			'extended': 1,
			'count': 1000,
			'photo_sizes': 1
		}
		url = self.base_VK_url + end_url
		try:
			response = requests.get(url, params={**self.base_VK_params, **vk_params}).json()['response']['items']
			logging.info("Получены фотографии пользователя")
			return response
		except TypeError:
			logging.error("Фотографии не получены")

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

	def _create_folder_on_disk(self, folder_name="Фотографии с VK"):
		end_url = 'resources'
		url = self.base_Ya_url + end_url
		try:
			response = requests.put(url, headers=self.Ya_headers, params={"path": folder_name})
			if response.status_code != 409:
				logging.info(f"Папка \"{folder_name}\" на Яндекс.Диске создана")
			return folder_name
		except:
			logging.error("Папка на Яндекс.Диске НЕ создана")

	def _upload_to_disk(self, file_name, photo_url):
		end_url = 'resources/upload'
		url = self.base_Ya_url + end_url
		params = {"path": file_name, "url": photo_url}
		response = requests.post(url, headers=self.Ya_headers, params=params)
		return response

	def get_photos(self):
		full_name = self._get_name()
		all_photos = self._get_vk_photos
		needed_photos = self._reformat_photos_list(all_photos)
		base_folder_name = self._create_folder_on_disk()
		folder_name = self._create_folder_on_disk(f'{base_folder_name}/{full_name}')

		for photo in tqdm(needed_photos, desc='Загружено фотографий'):
			file_name = f'{folder_name}/{photo["name"]}'
			photo_url = photo["photo_url"]
			self._upload_to_disk(file_name, photo_url)
		logging.info(f"Фотографии {len(needed_photos)} шт. загружены на Яндекс.Диск")

		photo_json = [{"file_name": photo['name'], "size": photo['size_type']} for photo in needed_photos]
		with open(f'{full_name}_photo.json', 'w', encoding='utf-8') as f:
			json.dump(photo_json, f)

		return photo_json


if __name__ == '__main__':
	VK_token = open('VK_token.txt', 'r').read()
	Ya_token = open('Ya_token.txt', 'r').read()

	photo_bot = GetPhotos(36140, Ya_token)
	photo_bot.get_photos()

# 5327 - private
# 1243256126 - deleted
# 1234569789578354 - нет
# 36140 = я