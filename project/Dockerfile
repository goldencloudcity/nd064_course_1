FROM python:3.8

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python init_db.py
# command to run on container start
EXPOSE 3111

CMD [ "python", "app.py" ]
