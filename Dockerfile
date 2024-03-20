# FROM - Image to start building on.
FROM python:3.8-slim

EXPOSE 8700

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# set the working directory
WORKDIR /app

COPY ./requirements.txt /requirements.txt
RUN apt-get update && apt-get install -y
RUN apt-get install -y gcc libc-dev
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /requirements.txt
RUN apt-get clean
RUN rm -f /var/lib/apt/list/*

# copy all files and directories from <src> to <dest>
COPY ./src .

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser