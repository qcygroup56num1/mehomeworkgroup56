import requests

url='https://en.bitcoin.it/wiki/Testnet'
tx={"1233672365448"}
print("发送的tx为：",tx)
post_html=requests.post(url,data=tx)
print("响应信息：")
print(post_html.text)
