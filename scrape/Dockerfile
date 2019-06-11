FROM python:3

RUN pip install pipenv

WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install

CMD ["pipenv", "run", "python", "scrape.py"]