import redis
import json

r = redis.Redis(host='redis-12893.c8.us-east-1-4.ec2.redns.redis-cloud.com', port=12893, db=0, password='hAlZdUs2811tjwgZhohkG9E1XSMNBkSu')

user_data = r.get('username:testuser')
if user_data:
    print(json.loads(user_data))
else:
    print("User not found")