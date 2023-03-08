#
import requests
#d02342df046dd4270f5bd06d54b4debe7c1f1ec9a32606608bfea574fc419658efc2cc43116c0a1646575
url = "https://api.vk.com/method/groups.get?user_ids=5689449&access_token=d02342df046dd4270f5bd06d54b4debe7c1f1ec9a32606608bfea574fc419658efc2cc43116c0a1646575&v=5.131"
response = requests.get(url)
j_data = response.json()
print(j_data)