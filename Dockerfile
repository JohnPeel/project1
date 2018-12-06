FROM johnpeel/cx_oracle:latest
MAINTAINER John Peel "john@dgby.org"
WORKDIR /app

ENV FLASK_APP app.py
COPY . /app
RUN python -m venv /app/venv \
 && /app/venv/bin/pip install -r requirements.txt \
 && /app/venv/bin/pip install gunicorn \
 && chmod +x /app/boot.sh \
 && adduser -D appuser \
 && chown -R appuser:appuser /app
USER appuser

ENTRYPOINT ["/app/boot.sh"]
