FROM python:3.8.2-alpine
COPY . /code
WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code"
CMD python -m currency_converter
