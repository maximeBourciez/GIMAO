FROM python:3.9-slim


RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    iputils-ping

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
