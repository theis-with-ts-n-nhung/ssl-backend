FROM python:3.9
COPY . /app/
RUN pip install poetry
RUN poetry config virtualenvs.create false
WORKDIR /app
RUN poetry install
CMD [ "ssl-backend" ]