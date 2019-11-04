FROM leeing0712/flaskapp

LABEL version='1.0'
LABEL author='leeing'

# USER root

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 5280

ENV NAME leeing

CMD ["python", "manage.py", "runserver"]
