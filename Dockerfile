FROM python:alpine
MAINTAINER John Peel "john@dgby.org"
COPY . /app
WORKDIR /app
RUN apk add --no-cache build-base \
  & pip install --upgrade pip setuptools \
  & pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
