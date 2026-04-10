FROM gcr.io/google.com/cloudsdktool/cloud-sdk:slim AS downloader
RUN gsutil cp gs://findmy-test/ani_libs.bin /tmp/ani_libs.bin

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY --from=downloader /tmp/ani_libs.bin /app/ani_libs.bin

EXPOSE 6970

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "6970"]
