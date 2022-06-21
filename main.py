from lib.my_requests import MyRequests
import config

#response = MyRequests.get(f'/tm-widgets/api/nsi/SearchOrganization?code={config.idLpu}')
#print(response.json())

response1 = MyRequests.get('/tm-core/api/Queries/GetProcess/69fac0a9-7791-4083-a89a-82cad36efd14', headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'})
print(response1.content)