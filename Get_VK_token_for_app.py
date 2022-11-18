import webbrowser


def open_url(app_id):
	base_url = 'https://oauth.vk.com/authorize?'
	params = {
		'client_id': app_id,
		'display': 'page',
		'scope': 'friends,photos,stories,offline,messages',
		'redirect_uri': 'https://oauth.vk.com/blank.html',
		'response_type': 'token',
		'v': '5.131',
		'state': 'Well done'
	}
	url_params = "&".join([f'{k}={v}' for k, v in params.items()])
	url = base_url + url_params
	print(url)
	webbrowser.open(url, new=2)


if __name__ == '__main__':
	your_app_id = 3456
	open_url(your_app_id)
