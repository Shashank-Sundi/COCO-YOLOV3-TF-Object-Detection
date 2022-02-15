#FROM python:3.7-slim
#ENV PYTHONUNBUFFERED 1
#MAINTAINER shashank sundi <sundi.sn@gmail.com>
#WORKDIR  /app
#COPY ./requirements.txt /app/requirements.txt
#RUN apt update 
#RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
#RUN pip install -r requirements.txt
#ADD . /app
#EXPOSE 5000
#CMD ["python","app.py"]

FROM python:3.7-slim AS builder
ENV PYTHONUNBUFFERED 1
MAINTAINER shashank sundi <sundi.sn@gmail.com>
WORKDIR  /app
COPY ./requirements.txt  /app/requirements.txt
RUN apt update 
RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
RUN pip install -r requirements.txt


FROM python:3.7-slim
WORKDIR .
COPY --from=builder usr/local/lib  usr/local/lib
ADD . /app
EXPOSE 5000
CMD ["python","app.py"]