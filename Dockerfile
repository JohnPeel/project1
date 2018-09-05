FROM python:alpine
MAINTAINER John Peel "john@dgby.org"
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
