FROM python:3

RUN pip install pipenv

WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install

ENV FLASK_APP main.py
EXPOSE 5000

CMD ["pipenv", "run", "flask", "run", "--host", "0.0.0.0"]