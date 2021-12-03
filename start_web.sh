#!/bin/bash

export FLASK_APP=flaskr
export FLASK_ENV=development
export MYSQL_HOST=mysql_app
export MYSQL_USER=root
export MYSQL_PWD=yuekang333
export MYSQL_DB=app_data

#docker run --name mysql_app -v ${PWD}/data/mysql_data:/var/lib/mysql --restart=always \
#        -e MYSQL_ROOT_PASSWORD=yuekang333 -e MYSQL_DATABASE=app_data -e TZ=Asia/Shanghai \
#        -p 3306:3306 -d mysql --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
flask run  --host=0.0.0.0

#gunicorn flaskr, -c "./gunicorn.conf.py"