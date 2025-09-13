# E-posta Uyumluluk Sınıflandırması (Email Compliance Classification)

Bu proje, e-posta içeriklerini uyumluluk açısından sınıflandırmak için geliştirilmiş bir makine öğrenmesi uygulamasıdır. Özellikle rekabet hukuku ihlalleri ve diğer uyumluluk sorunlarını tespit etmek amacıyla tasarlanmıştır.

![Uygulama Arayüzü](assets/streamlit%20ui.png)


## 📋 İçindekiler

- [Proje Hakkında](#proje-hakkında)
- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Veri Yapısı](#veri-yapısı)
- [Model Detayları](#model-detayları)
- [Docker ile Çalıştırma](#docker-ile-çalıştırma)
- [Proje Yapısı](#proje-yapısı)
- [Gereksinimler](#gereksinimler)
- [Katkıda Bulunma](#katkıda-bulunma)

## 🎯 Proje Hakkında

Bu sistem, e-posta içeriklerini aşağıdaki kategorilerde sınıflandırır:

- **abuse_of_dominance**: Pazar gücünün kötüye kullanılması
- **anti_competitive_merger**: Rekabet karşıtı birleşmeler
- **bid_rigging**: İhale manipülasyonu
- **clean**: Temiz/uyumlu içerik
- **customer_sharing**: Müşteri paylaşımı
- **exclusive_contracts**: Münhasır sözleşmeler
- **market_allocation**: Pazar paylaşımı
- **other_competition_violation**: Diğer rekabet ihlalleri
- **price_fixing**: Fiyat sabitleme

## ✨ Özellikler

- 🤖 **Transformer Tabanlı Model**: BERT benzeri model kullanarak yüksek doğruluk
- 🌐 **Web Arayüzü**: Streamlit ile kullanıcı dostu arayüz
- 🚀 **GPU Desteği**: CUDA desteği ile hızlı tahmin
- 📊 **Güven Skoru**: Her tahmin için güvenilirlik skoru
- 🐳 **Docker Desteği**: Kolay deployment için konteyner desteği
- 📄 **PDF İşleme**: PDF dosyalarından metin çıkarma desteği

## 🚀 Kurulum

### Yerel Kurulum

1. **Projeyi klonlayın:**
```bash
git clone <repository-url>
cd "Email Compliance Classification"
```

2. **Sanal ortam oluşturun:**
```bash
python -m venv new_env
```

3. **Sanal ortamı etkinleştirin:**
```bash
# Windows
new_env\Scripts\activate

# Linux/Mac
source new_env/bin/activate
```

4. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements.txt
```

5. **Uygulamayı çalıştırın:**
```bash
streamlit run app.py
```

## 🐳 Docker ile Çalıştırma

1. **Docker image'ını oluşturun:**
```bash
docker build -t email-compliance-classifier .
```

2. **Konteyner'ı çalıştırın:**
```bash
docker run -p 8501:8501 email-compliance-app
```

3. **Tarayıcıda açın:**
```
http://localhost:8501
```

## 💻 Kullanım

### Web Arayüzü ile Kullanım

1. Uygulamayı başlattıktan sonra web arayüzüne erişin
2. E-posta konusu (Subject) alanını doldurun
3. E-posta içeriği (Body) alanını doldurun
4. "Sınıflandır" butonuna tıklayın
5. Sonuçları görüntüleyin:
   - **Sınıflandırma**: Tahmin edilen kategori
   - **Güven Skoru**: Tahminin güvenilirlik derecesi (0-1 arası)

### Programatik Kullanım

```python
from src.app import predict_email, load_model_and_tokenizer, load_label_mapping

# Model ve tokenizer'ı yükle
model, tokenizer, device = load_model_and_tokenizer()
id2label = load_label_mapping()

# Tahmin yap
subject = "Fiyatlandırma Üzerine Görüşme Talebi"
body = "Yarın toplantı yapmayı öneriyorum..."

result = predict_email(subject, body, model, tokenizer, id2label)
print(f"Sınıflandırma: {result['label']}")
print(f"Güven Skoru: {result['confidence']:.4f}")
```

## 📊 Veri Yapısı

### Eğitim Verisi
Proje aşağıdaki veri formatlarını destekler:

**JSONL formatı:**
```json
{
  "text": "E-posta içeriği burada...",
  "label": "clean"
}
```

### Veri Dosyaları

- `data/raw/dataset.jsonl`: Ham Etiketlenmiş veri seti
- 'data/raw/PDFS': Ham pdf verileri
- `data/processed/dataset_formatted.jsonl`: İşlenmiş eğitim verisi (~11,750 örnek)
- `data/processed/pdf_dataset.jsonl`: PDF'lerden çıkarılan veriler (~101 örnek)
- `data/processed/pdf_dataset_cleaned.jsonl`: PDF'lerden çıkarılan verilerin temizlenmiş hali
- `data/processed/pdf_dataset_labeled.jsonl`: PDF'lerden çıkarılan temizlenmiş verilerin etiketlenmiş hali
- `data/processed/combined_data.jsonl`: Birleştirilmiş eğitim verisi

## 🤖 Model Detayları

### Model Mimarisi
- **Base Model**: Transformer tabanlı sequence classification modeli
- **Tokenizer**: BERT-compatible tokenizer
- **Max Length**: 512 token
- **Classes**: 9 farklı uyumluluk kategorisi

### Eğitilmiş Modeller
Projede iki farklı eğitilmiş model bulunur:

1. **trained_model1**: 
   - `checkpoint-2350`
   - `checkpoint-3525`

2. **trained_model2**: 
   - `checkpoint-3000`
   - `checkpoint-3111` (varsayılan olarak kullanılan)

### Model Performansı
- GPU desteği ile hızlı tahmin
- Güven skoru ile tahmin güvenilirliği
- Real-time sınıflandırma

## 📁 Proje Yapısı

```
Email Compliance Classification/
├── data/
│   ├── raw/
│   │   ├── dataset.jsonl              # Ham veri seti
│   │   └── PDFs/                      # PDF dosyaları (100 adet)
│   └── processed/
│       ├── dataset_formatted.jsonl    # İşlenmiş veri
│       ├── pdf_dataset.jsonl         # PDF'lerden çıkarılan veri
│       ├── pdf_dataset_cleaned.jsonl         
│       ├── pdf_dataset_labeled.jsonl         
│       └── combined_data.jsonl       # Birleştirilmiş veri
├── models/
│   ├── trained_model1/               # İlk eğitilmiş model
│   └── trained_model2/               # İkinci eğitilmiş model (aktif)
├── notebooks/
│   └── main.ipynb                    # Veri işleme ve model eğitimi
├── new_env/                          # Python sanal ortamı
├── app.py                            # Streamlit uygulaması (ana dizin)
├── Dockerfile                        # Docker konfigürasyonu
├── requirements.txt                  # Tüm proje bağımlılıkları
├── requirements-docker.txt           # Docker için optimize edilmiş bağımlılıklar
├── assets                            # README'de kullanılan resim ve video
│   ├── streamlit ui.png              # Uygulamanın Streamlit UI Görseli
│   └── proje nasıl çalışır.mp4       # Proje nasıl çalışır videosu
└── README.md                         # Bu dosya
```

## 📦 Gereksinimler

### Ana Bağımlılıklar
- **Python**: 3.11+
- **PyTorch**: 2.8.0+ (CUDA desteği ile)
- **Transformers**: 4.56.1
- **Streamlit**: 1.49.1
- **NumPy**: 2.2.6
- **Pandas**: 2.3.2

### Tam Bağımlılık Listesi
Detaylı bağımlılık listesi için `requirements.txt` dosyasına bakınız.

## 🔧 Yapılandırma

### Model Yolu
Varsayılan model yolu: `models/trained_model2/checkpoint-3111`

Farklı bir model kullanmak için `app.py` dosyasında `model_path` değişkenini güncelleyin:

```python
model_path = "models/trained_model1/checkpoint-3525"  # Örnek
```

### GPU Kullanımı
Uygulama otomatik olarak GPU'yu algılar ve kullanır. GPU mevcut değilse CPU'da çalışır.

## 🚨 Önemli Notlar

1. **Model Dosyaları**: Model dosyaları büyük olduğu için Git LFS kullanılması önerilir
2. **Bellek Kullanımı**: Modeller yaklaşık 500MB RAM kullanır
3. **GPU Gereksinimleri**: CUDA uyumlu GPU önerilir (opsiyonel)
4. **Veri Gizliliği**: Hassas verilerle çalışırken güvenlik önlemlerini alın

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun


