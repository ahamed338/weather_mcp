FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=7860
ENV OWM_API_KEY=your_api_key_here

CMD ["python", "app.py"]
