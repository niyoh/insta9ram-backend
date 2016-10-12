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
yum install nginx   &#35; superuser
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


