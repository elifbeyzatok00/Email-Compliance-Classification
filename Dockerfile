# Python 3.11 slim image kullan (daha küçük boyut için)
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Docker için optimize edilmiş requirements dosyasını kopyala ve bağımlılıkları yükle
COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

# Models ve data klasörlerini kopyala (app.py'nin üst dizininde olacak şekilde)
RUN mkdir -p ./models ./data/processed
COPY models/ ./models/
COPY data/processed/ ./data/processed/

# Uygulama dosyasını ana dizine kopyala
COPY app.py ./

# Streamlit için gerekli portları aç
EXPOSE 8501

# Streamlit uygulamasını başlat
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
