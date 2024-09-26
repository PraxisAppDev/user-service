import redis

class UserEventListener:
    def __init__(self, host='redis-11734.c11.us-east-1-3.ec2.redns.redis-cloud.com', port=11734, db=0, password='zMJq8dQ7IQhh4ooxREeEDinaqCK8NS9q', stream_key='auth_to_user_stream'):
        # Initialize Redis client with connection details (host, port, db, password, decode_responses)
        self.client = redis.Redis(host=host, port=port, db=db, password=password, decode_responses=True)
        self.stream_key = stream_key

    def listen_for_events(self):
        last_id = '0'
        while True:
            messages = self.client.xread({self.stream_key: last_id}, block=0)
            for stream, message_data in messages:
                last_id = message_data[0][0]
                event_data = message_data[0][1]
                if event_data['type'] == 'user_authenticated':
                    user_id = event_data['user_id']
                    print(f"User authenticated with ID: {user_id}")
                    self.handle_user_authentication(user_id)

    def handle_user_authentication(self, user_id):
        print(f"Handling user authentication for user_id: {user_id}")