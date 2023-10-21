FROM python:3.11.5
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requierements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]