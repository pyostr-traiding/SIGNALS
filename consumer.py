import json
import os

import redis
import time

from dotenv import load_dotenv

load_dotenv()


connection = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD'),
	db=0,
	decode_responses=True
)

queue = connection.pubsub()
queue.subscribe("signals:BTCUSDT")

while True:
	time.sleep(0.01)
	msg = queue.get_message()
	if msg:
		if not isinstance(msg["data"], int):

			print(json.loads(msg['data']))