FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /backend

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

RUN pip install -r requirements.txt

COPY . /backend

# CMD python manage.py runserver 0:8000
# CMD ["%%CMD%%"]