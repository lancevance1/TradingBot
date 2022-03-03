import time
import hmac
import config
from requests import Request

ts = int(time.time() * 1000)
url = 'https://ftx.com/api'
request = Request('GET', url)
prepared = request.prepare()
signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
signature = hmac.new(config.FTXSecretKey.encode(), signature_payload, 'sha256').hexdigest()

prepared.headers['FTX-KEY'] = config.FTXAPIKey
prepared.headers['FTX-SIGN'] = signature
prepared.headers['FTX-TS'] = str(ts)

response = request("GET", url, headers=prepared.headers, data=signature)

print(response.text)

