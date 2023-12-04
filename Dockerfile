FROM python:3.11

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY todolist_project/ /app

WORKDIR /app

CMD ["gunicorn", "todolist_project.wsgi:application", "--bind", "0:8000" ]
