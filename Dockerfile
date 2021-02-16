FROM python:3.8

ENV PYTHONUNBUFFERED 1

# Set working directory
RUN mkdir /peikareh
WORKDIR /peikareh
COPY . /peikareh

# Installing requirements
RUN pip install --upgrade pip
RUN pip install -r requirement.txt

CMD ["gunicorn", "--chdir", "peikareh", "--bind", ":8000", "peikareh.wsgi:application"]