FROM python:3.8

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY unitaries/ .
COPY final_unitaries/ .
COPY project_files/ .
COPY *.py/ .

CMD /bin/bash