import requests

token = "coloque_aqui_o_token_de_refresh_gerado_no_login"

headers = {"Authorization": "Bearer " + token}

response = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)

if response.status_code == 200:
    print("Novo token de acesso:", response.json()["access_token"])
else:
    print("Falha ao obter novo token de acesso. Status code:", response.status_code)

print(response.json())
