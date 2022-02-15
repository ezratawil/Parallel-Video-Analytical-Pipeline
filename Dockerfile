FROM  python:3.8.3

WORKDIR /app

COPY requirements.txt .

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 libqt5x11extras5 -y
RUN pip install -r requirements.txt

COPY  solution/ /app/


CMD ["python", "MAIN.py"]