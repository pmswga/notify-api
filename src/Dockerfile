FROM python:3.10-alpine

WORKDIR /app
COPY . .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]