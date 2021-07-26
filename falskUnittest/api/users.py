from config.settings import BASE_URL
import requests
class Users():
    def __init__(self):
        self.baseUrl = BASE_URL
        self.headers = {'User-Agent': 'PostmanRuntime/7.26.8','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','Content-Type':'application/json','Connection': 'keep-alive'}

    def getUsers(self):
        userUrl = self.baseUrl + "/users"
        res = requests.get(url = userUrl,headers = self.headers)
        return res.json()
if __name__ =='__main__':
    user = Users()
    res = user.getUsers()
    print(res)


