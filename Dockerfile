FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app
RUN apt-get update && pip3 install -r requirements.txt
ENV ANSIBLE_HOST_KEY_CHECKING=False
ENV ANSIBLE_JINJA2_EXTENSIONS=jinja2.ext.loopcontrols,jinja2.ext.do,jinja2.ext.i18n