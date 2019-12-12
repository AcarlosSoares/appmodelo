# pipenv install requests
# fonte: https://www.bogotobogo.com/python/python-REST-API-Http-Requests-for-Humans-with-Flask.php

import requests
# import json

try:
	# response = requests.get("http://www.flask-demo1.com/product/1")
    response = requests.get("http://localhost:8080/sgu/aplicativo")
    print(response.json())
except:
    print("Something went wrong")
# else:
#     print("Nothing went wrong") 
# finally:
#   print("The 'try except' is finished") 


# Outra Forma de Acessa o serviço Rest
# api_token = 'seu_api_token'
# api_url_base = 'http://www.flask-demo1.com'
#
# headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(api_token)}
# api_url = '{0}account'.format(api_url_base)
# response = requests.get(api_url, headers=headers)
#
# print(response.headers)
# print(" ")
# print(response.status_code)
# print(response.json())
#
# if response.status_code == 200:
#     print(json.loads(response.content.decode('utf-8')))
# else:
#     print('Erros')
