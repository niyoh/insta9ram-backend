# insta9ram-backend

Demo URL: [http://ec2-54-235-51-216.compute-1.amazonaws.com/](http://ec2-54-235-51-216.compute-1.amazonaws.com/)
(unfortunately, I forgot to select ap-southeast and deployed it in us-east. I'm trying to clone an instance back to ap-southeast)

#Installation
```
yum install redis   # superuser
npm install -g pm2   # superuser

git clone https://github.com/niyoh/insta9ram-backend/
cd insta9ram-backend
redis-server &    # it automatically loads dump.rdb
npm install
DEBUG=9gagGalleryBackend:* pm2 start bin/www -x -- --port 3003 --env=sdbx   # port 3003

cd ..
git clone https://github.com/niyoh/insta9ram-frontend/
cd insta9ram-frontend
npm install
pm2 start npm -- start    # port 3000, (browser-sync @ port 3001)
```

##nginx
dependencies
```
yum install nginx   # superuser
vi /etc/nginx/nginx.conf
```
add new virtual host (server) entry
```
server {
  listen 80;
  server_name ec2-54-235-51-216.compute-1.amazonaws.com insta9ram.appicpaas.com 9gag.niyoh.tech;

  location / {
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;  
    proxy_pass         "http://127.0.0.1:3000/";
  }
  
  location /backend/ {
    proxy_set_header   X-Forwarded-For $remote_addr;
    proxy_set_header   Host $http_host;
    proxy_pass         "http://127.0.0.1:3003/";
  }
```
frontend runs at /, backend runs at /backend/

or I got the AMI image in my account. I can add you thru IAM.

#Web Crawling
all posts are crawled with this HTTP request.
the tokens / cookies are copied from the browser inspector.
```
GET http://www.instagram.com/query

content-type: application/x-www-form-urlencoded
cookie: sessionid=IGSCb457b01e03e1c98ef58d3f92e04a784ac65e7beacc9a16eb7dc922e2d1f6ca81%3AUhal4tLEwC9t4VXbFVUOKOmFp7NWbCAN%3A%7B%22asns%22%3A%7B%22219.76.15.129%22%3A4760%2C%22time%22%3A1475832727%7D%7D; mid=V_drlwAEAAFrog6Z3drPBSNztXgB; fbm_124024574287414=base_domain=.instagram.com; fbsr_124024574287414=q8EMA71f8SoTA3nkP4KR9d3ZxB2CoKQv3KONed44vwY.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUI2VjZ4VXo3d3hBVGVMMW0wVVhONmltQWt6LThzWk95Y1ZnUzBlSkpPQVFrWEE2ZTZwem1hRGxCTWxEajZMY0xMaG4zRGVuQWtqLXd0RXVkelh1MU9PdmlyTGtNc2JpOS1pN2ROM1VuQVV6NGtZTUgxNXdyZENBdkdVSnF0ZFJyLW4zMFk4RzNDdnBxeGhJdkRRRVpwSEJLMHdyd3RDQ0c4VkdIME5PTlVCMG42c0dITGxlNnF3N0FLNkRNemJuTWx6QW5wMVZhT3NLc0FxS2YweERONmdvTEx3eTBlZzdOdlNvUXppSmpoRGVBZ1loOVNnMS1rVUZOMmVqcHVTOUtjZ1pRZG84WUwxa19FQnVQdldocVpta2Y0dDFaWEdKelVuM3BTT29VZ2xYLWtTdE1ZVGJVNzQ4NTdveEtLS3NESkl5eFQza0tmTmRsN1pnNm9uLXQxZCIsImlzc3VlZF9hdCI6MTQ3NTgzNDA5OSwidXNlcl9pZCI6IjcwMDEzMjcyNiJ9; csrftoken=wLBZf0vs2E7iD7N5FIwmpavvKDFORnna; s_network=; ig_pr=2; ig_vw=1280
referer: https://www.instagram.com/9gag/
x-csrftoken: wLBZf0vs2E7iD7N5FIwmpavvKDFORnna

payload:
q=ig_user(259220806)+%7B+media.after(1353397180899329160%2C+200)+%7B%0A++count%2C%0A++nodes+%7B%0A++++caption%2C%0A++++code%2C%0A++++comments+%7B%0A++++++count%0A++++%7D%2C%0A++++comments_disabled%2C%0A++++date%2C%0A++++dimensions+%7B%0A++++++height%2C%0A++++++width%0A++++%7D%2C%0A++++display_src%2C%0A++++id%2C%0A++++is_video%2C%0A++++likes+%7B%0A++++++count%0A++++%7D%2C%0A++++owner+%7B%0A++++++id%0A++++%7D%2C%0A++++thumbnail_src%2C%0A++++video_views%0A++%7D%2C%0A++page_info%0A%7D%0A+%7D&ref=users%3A%3Ashow&query_id=17842962958175392
```
(for the sake of avoiding the work to setup instagram APIs)
video URLs are obtained manually from DOM inspection due to limited time.
future improvements: register for auth_token @ instagram API / use scrapy framework to crawl stuff

#Database Architecture
ZSET (as indexes): chrono (score:UNIX timestamp), likes (score:like count), comments (score:comment count)
so for sorting with time (chronological order), likes, comments, the sorted result is readily available with: 
```
SORT chrono BY nosort DESC GET ...
```

HASH (post details): 
```
# structure of post
      {
        "code": "BKYM8zJhhl0",
        "date": 1473945907,
        "dimensions": {
          "width": 640,
          "height": 506
        },
        "comments_disabled": false,
        "comments": {
          "count": 28238
        },
        "caption": "Just one more episode #9gag @9gagmobile",
        "likes": {
          "count": 702405
        },
        "owner": {
          "id": "259220806"
        },
        "thumbnail_src": "https:\/\/scontent-nrt1-1.cdninstagram.com\/t51.2885-15\/e35\/c67.0.507.507\/14351007_1939234682970443_1842768309_n.jpg?ig_cache_key=MTMzOTg3Nzg0Mzc5MDA3NjI3Ng%3D%3D.2.c",
        "is_video": false,
        "id": "1339877843790076276",
        "display_src": "https:\/\/scontent-nrt1-1.cdninstagram.com\/t51.2885-15\/s640x640\/sh0.08\/e35\/14351007_1939234682970443_1842768309_n.jpg?ig_cache_key=MTMzOTg3Nzg0Mzc5MDA3NjI3Ng%3D%3D.2"
      }
```

The sorting can also be customized with a GET param in url encoded JSON with following structure:
{ "field":"date", "order":"DESC", "isAlpha":true }
But I have no time to prevent it from injection attacks.

