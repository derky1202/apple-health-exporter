FROM python:3.11
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN pip install poetry &&\
  poetry config virtualenvs.create false &&\
  poetry install --no-dev
COPY . /app
ENV PORT=38001
EXPOSE 38001
ENV HOST="::"
CMD bash -c "python -m uvicorn server:app --host $HOST --port $PORT"
