FROM leeing0712/flaskapp

LABEL version='1.0'
LABEL author='leeing'

# USER root

WORKDIR /code

ADD . /code

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 6281

ENV NAME opera

CMD ["python", "manage.py", "runserver"]
