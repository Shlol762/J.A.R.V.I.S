url = 'https://discordpy.readthedocs.io/en/stable/'
url_api = url + 'api.html#'

discord = {
    'href': url,
    'api':
        {
            'href': url_api,
            '__doc__': ''
        }
    }

print(discord.get('api').get('__doc__'))
