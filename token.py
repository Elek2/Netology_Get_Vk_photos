import webbrowser

base_url = 'https://oauth.vk.com/authorize?'
params = {
	'client_id': 51475199,
	'display': 'page',
	'scope': 'friends,photos,stories,offline',
	'redirect_uri': 'https://oauth.vk.com/blank.html',
	'response_type': 'token',
	'v': '5.131',
	'state': 'Well done'
}
url_params = "&".join([f'{k}={v}' for k, v in params.items()])
url = base_url + url_params
print(url)


webbrowser.open(url, new = 2)