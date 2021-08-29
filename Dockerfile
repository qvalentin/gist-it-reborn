FROM python:3.9

WORKDIR /app

COPY src/requirements.txt ./
RUN pip install -r requirements.txt

COPY src /app

EXPOSE 4876
CMD [ "python", "server.py" ]
