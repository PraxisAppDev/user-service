import redis
import json

r = redis.Redis(host='redis-11734.c11.us-east-1-3.ec2.redns.redis-cloud.com', port=11734, db=0, password='zMJq8dQ7IQhh4ooxREeEDinaqCK8NS9q')

user_data = r.get('user:testuser1')
if user_data:
    print(json.loads(user_data))
else:
    print("User not found")