FROM python:latest
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1
CMD ["sleep", "infinity"]