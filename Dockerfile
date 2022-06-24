FROM python:3.9-slim

ENV CLOWDER_URL=http://clowder:9000 \
    CLOWDER_KEY=secret \
    RECURSIVE=False \
    DATA=/data \
    DATASET_ID="" \
    DATASET_NAME=""

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY uploader.py ./

CMD python ./uploader.py
