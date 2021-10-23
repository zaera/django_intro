FROM python:3.9

WORKDIR /home/build

COPY requirements.txt .

# RUN apt update -y && apt install -y curl

RUN pip install -r requirements.txt

# ENV PYTHONPATH "/home/build/app"

COPY . .

# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--chdir", "/home/build/app", "settings.wsgi", "--timeout 30", "--log-level error", "--max-requests 10000"]
# CMD ["python", "app/manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# docker exec -it e9b91a252ea99cd707f32a2099b642e96d8c758868c90767330751fa0a3c1968 python manage.py createsuperuser