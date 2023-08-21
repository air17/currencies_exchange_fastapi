FROM python:3.10
RUN mkdir /src
COPY src /src/
COPY requirements.txt /src/
WORKDIR /src
ENV PYTHONPATH=/src
RUN pip install --no-cache-dir -r requirements.txt
