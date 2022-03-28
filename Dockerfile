FROM python:3.8

WORKDIR /code

# Install dependencies

# RUN apt update && apt install -y libopenblas-dev libceres-dev libeigen3-dev gfortran cmake build-essential

# RUN apt update && apt install -y libgfortran-7-dev

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY unitaries/ unitaries/
COPY final_unitaries/ final_unitaries/
COPY project_files/ project_files/
COPY *.py/ .

CMD /bin/bash