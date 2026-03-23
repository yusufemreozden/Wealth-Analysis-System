# 📊 Wealth Analysis & Decision Support System (WADSS)

![Python Version](https://img.shields.io/badge/python-3.12-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/status-active-success?style=flat-square)
![Platform](https://img.shields.io/badge/automation-GitHub%20Actions-blueviolet?style=flat-square&logo=github-actions)

## 🎯 Proje Hakkında
Bu proje; finansal piyasalardaki gürültüyü filtrelemek ve veri odaklı uzun vadeli yatırım kararları almak amacıyla geliştirilmiş bir **Algorithmic Decision Support System** (Algoritmik Karar Destek Sistemi)'dir. 

Sistem; **NASDAQ (TEFAS: AFT)** ve **Altın (TEFAS: KZL)** varlıklarını teknik indikatörler aracılığıyla analiz eder ve belirlenen **"Matris Stratejisi"**ne göre günlük aksiyon raporları üretir. Yatırımcının duygusal kararlar yerine, önceden tanımlanmış matematiksel eşiklere göre hareket etmesini sağlar.

---

## 🚀 Temel Özellikler
* **Otonom Veri Analizi:** Yahoo Finance API üzerinden 5 yıllık tarihsel verilerin anlık işlenmesi.
* **Gelişmiş Teknik Göstergeler:** Trend analizi için SMA (200, 500) & EMA (610) ve Momentum kontrolü için RSI (14) kullanımı.
* **Dinamik Karar Motoru:** Fiyatın hareketli ortalamalara uzaklığını hesaplayarak "Kriz Fırsatı", "İndirim", "Pusuda Bekle" gibi spesifik aksiyonlar üretilmesi.
* **Kurumsal Raporlama:** GitHub Actions ile her gün (TSİ 15:00) otomatik tetiklenen, özelleştirilmiş HTML/CSS e-posta bültenleri.
* **Anlık Makro Takip:** USD/TRY, EUR/TRY ve Bitcoin (BTC) fiyatlarının rapor başlığında konsolide edilmesi.

---

## 🛠️ Teknik Mimari
Proje, modüler ve güvenli bir altyapı üzerine inşa edilmiştir:

| Teknoloji | Fonksiyon |
| :--- | :--- |
| **Python 3.12** | Algoritma ve Veri Yönetimi |
| **Pandas** | Zaman Serisi Analizi |
| **yfinance** | Finansal Veri Kaynağı |
| **GitHub Actions** | CI/CD Tabanlı Otomasyon (Cron Job) |
| **SMTP / MIME** | E-Posta İletim Protokolü |
| **GitHub Secrets** | Güvenli Kimlik Bilgisi (Secret Management) |

---

## 📈 Algoritmik Strateji (The Matrix Logic)
Sistemin karar mekanizması, fiyatın uzun vadeli ortalamalardan sapmasını (Mean Reversion) ve momentum doygunluğunu temel alır:

1.  **Kriz Fırsatı:** Fiyatın EMA 610 altında veya RSI'ın 30'un altında olduğu, maksimum biriktirme bölgesi.
2.  **İndirim Bölgesi:** Fiyatın SMA 200/500 seviyelerine yaklaştığı "Güvenli Alım" alanı.
3.  **Pahalı / Alımı Durdur:** Fiyatın tarihsel ortalamalardan %20+ koptuğu, kar realizasyonu veya bekleme aşaması.

---

## ⚙️ Kurulum ve Yapılandırma
Sistemi kendi ortamınızda çalıştırmak için aşağıdaki adımları izleyin:

1.  **Repoyu Clone'layın:**
    ```bash
    git clone [https://github.com/yusufemreozden/WADSS.git](https://github.com/yusufemreozden/WADSS.git)
    ```
2.  **Gereksinimleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **GitHub Secrets Tanımlayın:**
    GitHub Settings > Secrets > Actions kısmına şu değişkenleri ekleyin:
    * `GMAIL_ADRESI`: Gönderici mail adresi.
    * `GMAIL_SIFRESI`: Google Uygulama Şifresi (16 Haneli).
    * `ALICI_MAILLER`: Raporun gideceği adresler (virgülle ayrılmış).

---

## 📜 Lisans & İletişim
Bu proje **MIT Lisansı** altında lisanslanmıştır. 

**Geliştiren:** Yusuf Emre ÖZDEN  
**Web:** [yusufemreozden.com](https://yusufemreozden.com)  
**LinkedIn:** [linkedin.com/in/yusufemreozden](https://linkedin.com/in/yusufemreozden)

---
*Bu sistem yatırım tavsiyesi vermez; sadece teknik verilere dayalı bir analiz simülasyonudur.*
