import json
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=1)
with open('instagram-200pics.json') as data_file:
	post_json = json.load(data_file)

for post in post_json:
	post['likes'] = post['likes']['count']
	post['comments'] = post['comments']['count']
	r.hmset('post:' + post['id'], post)
	r.zadd('likes', +post['likes'], 'post:' + post['id'])
	r.zadd('comments', +post['comments'], 'post:' + post['id'])
	r.zadd('chrono', +post['date'], 'post:' + post['id'])
	if post['is_video'] == True:
		r.zadd('videos', +post['date'], 'post:' + post['id'])
