FROM python:3.8.5-buster
LABEL Alessio Caradossi <alkcxy@gmail.com>
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./net_trackr.py" ]