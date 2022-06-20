FROM python:3.10.2

COPY . /GoogleSheetsSQL

WORKDIR /GoogleSheetsSQL

RUN pip install -r requirements.txt

CMD ['python', 'main.py']



