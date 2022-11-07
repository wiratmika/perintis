FROM python:3.9
WORKDIR /app

COPY app/Pipfile ./Pipfile
COPY app/Pipfile.lock ./Pipfile.lock
RUN pip install pipenv
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "perintis.py"]
