FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install virtualenv

RUN virtualenv .venv

RUN . .venv/bin/activate && pip install -r requirements.txt

COPY . .

CMD ["/bin/bash", "-c", ". .venv/bin/activate && python update-infos.py"]
