import os
import requests
from flask import Flask, render_template_string

# API anahtarını ortam değişkeninden al
# Docker'da çalıştırırken bu değişkeni ileteceğiz.
API_KEY = os.environ.get('TMDB_API_KEY')
BASE_URL = "https://api.themoviedb.org/3"
POPULAR_MOVIES_ENDPOINT = f"{BASE_URL}/movie/popular"

app = Flask(__name__)

# Basit bir HTML şablonu (Normalde ayrı bir 'templates' klasöründe olur)
HTML_TEMPLATE = """
<!doctype html>
<html lang="tr">
<head>
    <meta charset="utf-8">
    <title>Popüler Filmler</title>
</head>
<body>
    <h1>Popüler Filmler (TMDB API)</h1>
    <ul>
        {% for movie in movies %}
            <li>
                <strong>{{ movie.title }}</strong> 
                (Puan: {{ movie.vote_average }}, Çıkış: {{ movie.release_date }})
            </li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def get_popular_movies():
    if not API_KEY:
        return "Hata: TMDB_API_KEY ortam değişkeni ayarlanmadı.", 500

    params = {
        'api_key': API_KEY,
        'language': 'tr-TR' # İsteğe bağlı, Türkçe içerik gelmesi için
    }
    
    try:
        response = requests.get(POPULAR_MOVIES_ENDPOINT, params=params)
        response.raise_for_status() # HTTP hatalarını yakalamak için
        data = response.json()
        movies = data.get('results', [])
        
        # Sadece ilk 10 filmi göster
        top_movies = movies[:10]
        
        return render_template_string(HTML_TEMPLATE, movies=top_movies)
        
    except requests.exceptions.RequestException as e:
        return f"API isteği hatası: {e}", 500

if __name__ == '__main__':
    # Flask sunucusunu 0.0.0.0 üzerinde çalıştır ki Docker içinde erişilebilir olsun
    app.run(debug=True, host='0.0.0.0', port=5000)
