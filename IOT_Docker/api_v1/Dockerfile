FROM python:3.11.2-alpine3.17

WORKDIR /api_v1

COPY requirements.txt requirements.txt
RUN pip3 install flask
RUN pip3 install -r requirements.txt

COPY . .

#CMD ["ls", "-la"]

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]