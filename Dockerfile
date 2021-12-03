# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD ["bash", "start_web.sh"]
#CMD ["gunicorn", "flaskr:app", "-c", "./gunicorn.conf.py"]
