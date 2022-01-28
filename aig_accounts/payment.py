# -*- coding: utf-8 -*-

import urllib.request as request
import json


class Stripe:

	def __init__(self, protocol, host, key):
		self.protocol = protocol
		self.host = host
		self.key = key

#  1 subscribed.
#  0 unsubscribed.
# -1 invalid stripe account.
# -2 no stripe account.
# -3 error.
	def is_subscribe(self, username):
		try:
			with request.urlopen(f"{self.protocol}://{self.host}/public/subscribe/{username}?key={self.key}") as response:
				packet = json.loads(response.read())
				if packet['code'] == 0:
					result = packet['value']
				else :
					result = -1

		except Exception as e:
			result = -3
		return result

if __name__ == "__main__":
	p = Stripe("http", "localhost:3000", "")
	#print(p.is_subscribe("user2221@aigia.jp"))
