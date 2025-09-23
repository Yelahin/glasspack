FROM python:3.13-slim

#and new user and usergroup
RUN apt-get update && apt-get install -y libpq-dev gcc passwd \
    && groupadd -r illia && useradd -r -g illia illia

#manage workdir
WORKDIR /var/www/glasspack

#copy requriments.txt
COPY requriments.txt .
RUN pip install --upgrade pip && pip install -r requriments.txt

#copy project files
COPY . .

#manage user
USER illia

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["gunicorn", "glasspack.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]