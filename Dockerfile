FROM ubuntu

COPY . /app

WORKDIR /app

RUN apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y \
	python3 \
	python3-pip \
	python3-opencv

RUN pip3 install -r requirements.txt


EXPOSE 5000

RUN ["expose", "FLASK_APP=app.py"]
ENTRYPOINT ["flask", "run"]
