import streamlit as st
import torch
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Sayfa yapılandırması
st.set_page_config(
    page_title="E-posta Uyumluluk Sınıflandırması",
    page_icon="📧"
)

@st.cache_resource
def load_model_and_tokenizer():
    """Model ve tokenizer'ı yükle (cache ile performans optimizasyonu)"""
    try:
        model_path = "models/trained_model2/checkpoint-3111"
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        # GPU varsa kullan
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        
        return model, tokenizer, device
    except Exception as e:
        st.error(f"Model yüklenirken hata oluştu: {e}")
        return None, None, None

@st.cache_resource
def load_label_mapping():
    """Label mapping'ini yükle"""
    try:
        # Eğitim datasından label mapping'ini oluştur
        train_file = "data/processed/combined_data.jsonl"
        
        train_data = []
        with open(train_file, "r", encoding="utf-8") as f:
            for line in f:
                train_data.append(json.loads(line))
        
        labels = sorted(list(set([item['label'] for item in train_data])))
        label2id = {label: i for i, label in enumerate(labels)}
        id2label = {i: label for label, i in label2id.items()}
        
        return id2label
    except Exception as e:
        st.error(f"Label mapping yüklenirken hata oluştu: {e}")
        # Model eğitimindeki gerçek label mapping (sorted)
        return {
            0: "abuse_of_dominance",
            1: "anti_competitive_merger", 
            2: "bid_rigging",
            3: "clean",
            4: "customer_sharing",
            5: "exclusive_contracts",
            6: "market_allocation",
            7: "other_competition_violation",
            8: "price_fixing"
        }

def predict_email(subject, body, model, tokenizer, id2label):
    """
    E-posta subject ve body'sini sınıflandırır
    
    Args:
        subject (str): E-posta konusu
        body (str): E-posta içeriği
        model: Fine tune edilmiş model
        tokenizer: Model ile uyumlu tokenizer
        id2label: Label mapping
    
    Returns:
        dict: label ve confidence içeren sözlük
    """
    text = subject + " " + body
    
    # Tokenize et ve modelin bulunduğu device'a gönder
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    model.eval()  # Evaluation moduna al
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)
        label_id = torch.argmax(probs, dim=-1).item()
        confidence = probs[0, label_id].item()
    
    return {"label": id2label[label_id], "confidence": confidence}

def main():
    st.title("📧 E-posta Uyumluluk Sınıflandırması")
    st.markdown("Bu uygulama, e-posta içeriklerini uyumluluk açısından sınıflandırır.")
    
    # Model ve tokenizer'ı yükle
    model, tokenizer, device = load_model_and_tokenizer()
    id2label = load_label_mapping()
    
    if model is None or tokenizer is None:
        st.stop()
    
    # Başarılı yükleme mesajı
    st.success(f"✅ Model başarıyla yüklendi ({device})")
    
    # Kullanıcı girdileri
    st.header("E-posta Bilgilerini Girin")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        subject = st.text_input(
            "📝 E-posta Konusu (Subject)",
            placeholder="Örn: Fiyatlandırma Üzerine Görüşme Talebi",
            help="E-postanın konu satırını girin"
        )
    
    with col2:
        body = st.text_area(
            "📄 E-posta İçeriği (Body)",
            placeholder="Örn: Merhaba, yarın toplantı yapmayı öneriyorum...",
            help="E-postanın içeriğini girin",
            height=100
        )
    
    # Tahmin butonu
    if st.button("🔍 Sınıflandır", use_container_width=True):
        if subject.strip() == "" and body.strip() == "":
            st.warning("⚠️ Lütfen en az konu veya içerik alanlarından birini doldurun.")
        else:
            try:
                # Tahmin yap
                result = predict_email(subject, body, model, tokenizer, id2label)
                
                # Sonuçları göster
                st.write(f"**Sınıflandırma:** {result['label']}")
                st.write(f"**Güven Skoru:** {result['confidence']:.4f}")
            
            except Exception as e:
                st.error(f"Tahmin yapılırken hata oluştu: {e}")
    

if __name__ == "__main__":
    main()
