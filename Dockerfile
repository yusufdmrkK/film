# Temel imaj olarak resmi Python 3.10 slim sürümünü kullan
FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Bağımlılıklar dosyasını kopyala
COPY requirements.txt .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Tüm uygulama kodunu çalışma dizinine kopyala
COPY . .

# Flask'ın varsayılan olarak dinleyeceği portu açığa çıkar
EXPOSE 5000

# Uygulamayı başlatma komutunu tanımla
# Flask uygulamalarını çalıştırmak için gunicorn gibi bir WSGI sunucusu kullanmak daha iyidir
# Ancak bu basit örnek için doğrudan python komutunu kullanalım
CMD ["python", "app.py"]
