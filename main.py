import time
import requests
from pprint import pprint
import pandas as pd


class VkSearch:
	def __init__(self, token):
		self.token = token
		self.base_url = 'https://api.vk.com/method/'
		self.base_params = {
			'access_token': self.token,
			'v': '5.131',
		}

	def get_users(self, user_ids):
		end_url = 'users.get'
		params = {
			'user_ids': user_ids,
			'fields': 'education, sex'
		}
		url = self.base_url + end_url
		response = requests.get(url, params={**self.base_params, **params})
		return response.json()

	def search_groups(self, q,  sorting=0):
		end_url = 'groups.search'
		params = {
			'q': q,
			'sort': sorting,
			'count': 300
		}
		url = self.base_url + end_url
		response = requests.get(url, params={**self.base_params, **params}).json()
		return response['response']['items']

	def search_groups_deep(self, q, sorting=0):
		end_url = 'groups.getById'
		groups_ids = ','.join([str(group['id']) for group in self.search_groups(q, sorting)])
		params = {
			'group_ids': groups_ids,
			'fields': 'description, members_count',
		}
		url = self.base_url + end_url
		response = requests.get(url, params={**self.base_params, **params}).json()
		filtered_resp = [
			{k: v for k, v in i.items() if k in ('description', 'members_count', 'id')}
			for i in response['response']
		]
		# return response['response']
		return filtered_resp

	def get_followers(self, user_id=None):
		end_url = 'users.getFollowers'
		params = {
			'user_id': user_id,
			# 'sort': sorting,
			'count': 1000
		}
		url = self.base_url + end_url
		response = requests.get(url, params={**self.base_params, **params}).json()
		return response['response']

	def get_news(self, q, user_id=None):
		end_url = 'newsfeed.search'
		params = {
			'q': q,
			# 'start_from': 0,
			'count': 200
		}
		url = self.base_url + end_url
		news = []
		while True:
			response = requests.get(url, params={**self.base_params, **params}).json()['response']
			time.sleep(0.4)
			news.extend(response['items'])
			if 'next_from' in response:
				params['start_from'] = response['next_from']
			else:
				break
		return news


yur = VkSearch(vk_token.TOKEN)

# pprint(yur.get_users('323546,4456789'))
# pprint(yur.search_groups_deep('звери'))
# print(pd.DataFrame(yur.search_groups_deep('звери')))
# pprint(yur.get_followers())
a = yur.get_news('питер')
# with open('text.txt', 'w', encoding='utf-8') as text:
# 	text.write(str(a))
pprint(len(a))
# print(pd.DataFrame(a))

