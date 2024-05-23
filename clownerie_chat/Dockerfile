FROM python:3.9.0-slim

RUN python -m pip install rasa

WORKDIR /app
ENV HOME=/app
COPY . .

RUN rasa train

USER 1001

ENTRYPOINT ["rasa"]

CMD ["run","-m","/app/models","--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints.yml", "--debug"]

EXPOSE 5005