FROM python:3.6-slim    

RUN mkdir /backend

WORKDIR /backend

ADD . /backend
# Install any needed packages specified in requirements.txt

EXPOSE 8080

RUN pip install -r requirements.txt

CMD python manage.py runserver 0:8000
# CMD ["%%CMD%%"]