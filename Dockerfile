FROM centos
RUN dnf -y update
RUN dnf -y install python3
RUN pip3 install --upgrade pip
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD gunicorn  --bind 0.0.0.0:5000 wsgi
EXPOSE 5000
