FROM python:3.9-alpine3.14
ENV FLASK_PATH /flaskapp
ENV FLASK_USER flaskuser
RUN adduser -h $FLASK_PATH -s /bin/sh -D $FLASK_USER
WORKDIR $FLASK_PATH
COPY . .
RUN chown -R $FLASK_USER:$FLASK_USER $FLASK_PATH
RUN pip install -r requirements.txt
USER $FLASK_USER
CMD ["app.py"]
ENTRYPOINT ["python3"]

