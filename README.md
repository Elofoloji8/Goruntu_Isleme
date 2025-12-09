# 🚦 Trafik Lambası ve Trafik İşareti Tespit Sistemi (OpenCV)

Bu proje, video üzerinden **trafik lambalarını** (kırmızı–sarı–yeşil ışık) ve **trafik işaretlerini** (STOP, dairesel yasaklama, üçgen uyarı) tespit eden bir görüntü işleme uygulamasıdır.

Proje tamamen **YOLO olmadan**, yalnızca **OpenCV + HSV analiz + contour detection** ile geliştirilmiştir.

## ✨ Özellikler

### 🔥 Trafik Lambası Tespiti
- Kırmızı ışık → **DUR** (tek sefer sesli uyarı)
- Sarı ışık → **BEKLE**
- Yeşil ışık → **GEÇ**

### 🛑 Trafik İşareti Tespiti
- STOP işareti (sekizgen)
- Dairesel hız sınırı / yasaklama işaretleri
- Üçgen uyarı işaretleri
- Her işaret çerçeve içine alınır ve Excel’e kaydedilir

### 📊 Excel Çıktısı
Her tespit için şu bilgiler kaydedilir:
- İşaret türü
- Tespit zamanı
- X/Y konumu
- Genişlik / Yükseklik

Oluşturulan dosya:
kayit.xlsx

### 🔔 Sesli Uyarı
- Kırmızı ışık algılandığında **alert.mp3** bir kez çalınır.

---

## 🛠 Kullanılan Teknolojiler

|   Teknoloji   |    Açıklama |
|-------------|---------------|
| Python      | Ana programlama dili |
| OpenCV      | Görüntü işleme, HSV dönüşümü, contour analizi |
| NumPy       | Matris işlemleri |
| Pandas      | Excel çıktısı üretimi |
| Playsound   | Ses çalma |
| Spyder      | Geliştirme ortamı |

## 🚀 Kurulum

### 1) Gerekli paketleri yükle
pip install opencv-python
pip install numpy
pip install pandas
pip install playsound==1.2.2

### 2) Proje dosyalarını aynı klasöre koy
main.py
video.mp4
alert.mp3
### 3) Programı çalıştır
python main.py
