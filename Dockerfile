FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY currency_converter/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./currency_converter .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "currency_converter.wsgi:application" ]