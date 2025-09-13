FROM python:3.13.3

#and new user and usergroup
RUN groupadd -r illia && useradd -r -g illia illia

#upgrade pip
RUN pip install --upgrade pip

#manage workdir
WORKDIR /var/www/glasspack

#copy requriments.txt
COPY requriments.txt .
RUN pip install -r requriments.txt

#copy project files
COPY . .

#manage user
USER illia

CMD ["gunicorn", "glasspack.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]