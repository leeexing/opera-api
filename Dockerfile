FROM python-app

LABEL version='1.0'
LABEL author='leeing'

RUN pip3 install pika -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 80 5000 6281 8080

ENTRYPOINT []
