# 📊 Wealth Analysis & Decision Support System (WADSS)

![Python Version](https://img.shields.io/badge/python-3.12-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/status-active-success?style=flat-square)
![Platform](https://img.shields.io/badge/automation-GitHub%20Actions-blueviolet?style=flat-square&logo=github-actions)

## 🎯 Proje Hakkında
Bu proje; finansal piyasalardaki gürültüyü filtrelemek ve veri odaklı uzun vadeli yatırım kararları almak amacıyla geliştirilmiş bir **Algorithmic Decision Support System** (Algoritmik Karar Destek Sistemi)'dir. 

Sistem; **NASDAQ (TEFAS: AFT)** ve **Altın (TEFAS: KZL)** varlıklarını teknik indikatörler aracılığıyla analiz eder ve belirlenen **"Matris Stratejisi"**ne göre günlük aksiyon raporları üretir. Yatırımcının duygusal kararlar yerine, önceden tanımlanmış matematiksel eşiklere göre hareket etmesini sağlar.

---

## 🔬 Kantitatif Metodoloji (Quantitative Methodology)
Sistemin karar mekanizması, basit indikatör takibi yerine tarihsel veri setleri üzerinde yapılan **İstatistiksel Yüzdelik (Percentile Analysis)** çalışmalarına dayanır:

* **Veri Madenciliği:** Nasdaq ve XAUUSD varlıklarının son 10 yıllık günlük verileri analiz edilerek "Normal Dağılım" dışındaki sapmalar tespit edilmiştir.
* **İstatistiksel Eşikler:** Kodda kullanılan alım/satım katsayıları (örn. `ratio200 >= 1.24`), fiyatın tarihsel olarak sadece %5'lik zaman dilimlerinde ulaştığı "Ekstrem Noktalar" (Tail Risks) baz alınarak optimize edilmiştir.
* **Gürültü Filtreleme:** Standart sapma analizleri sayesinde piyasadaki önemsiz dalgalanmalar elenmiş, strateji sadece olasılık değeri yüksek "Pusu" ve "Kriz" bölgelerine odaklanmıştır.

---

## 🚀 Temel Özellikler
* **Otonom Veri Analizi:** Yahoo Finance API üzerinden tarihsel verilerin anlık işlenmesi.
* **Gelişmiş Teknik Göstergeler:** SMA (200, 500) & EMA (610) trend takibi ve RSI (14) momentum kontrolü.
* **Matris Karar Motoru:** Fiyatın hareketli ortalamalara uzaklığını hesaplayarak "Kriz Fırsatı", "İndirim", "Pusu" gibi spesifik aksiyonlar üretilmesi.
* **Kurumsal Raporlama:** GitHub Actions ile her gün (TSİ 15:00) otomatik tetiklenen, profesyonel HTML/CSS e-posta bültenleri.
* **Makro Gösterge Paneli:** USD/TRY, EUR/TRY ve Bitcoin (BTC) fiyatlarının rapor başlığında konsolide edilmesi.

---

## 🛠️ Teknik Mimari
| Teknoloji | Fonksiyon |
| :--- | :--- |
| **Python 3.12** | Algoritma ve Veri Yönetimi |
| **Pandas** | Zaman Serisi ve İstatistiksel Analiz |
| **yfinance** | Finansal Veri API Entegrasyonu |
| **GitHub Actions** | CI/CD Tabanlı Otomasyon (Cron Job) |
| **SMTP / MIME** | Kurumsal Rapor İletim Protokolü |
| **GitHub Secrets** | Güvenli Kimlik Bilgisi Yönetimi |

---

## ⚙️ Kurulum ve Yapılandırma
Sistemi kendi ortamınızda çalıştırmak için:

1.  **GitHub Secrets Tanımlayın:**
    GitHub Settings > Secrets > Actions kısmına şu değişkenleri ekleyin:
    * `GMAIL_ADRESI`: Gönderici mail adresi.
    * `GMAIL_SIFRESI`: Google Uygulama Şifresi (16 Haneli).
    * `ALICI_MAILLER`: Raporun gideceği adresler (virgülle ayrılmış).

2.  **Gereksinimleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 📜 Lisans & İletişim
Bu proje **MIT Lisansı** altında lisanslanmıştır. 

**Geliştiren:** Yusuf Emre ÖZDEN  
**Web:** [yusufemreozden.com](https://yusufemreozden.com)  
**LinkedIn:** [linkedin.com/in/yusufemreozden](https://linkedin.com/in/yusufemreozden)

---
*Bu sistem yatırım tavsiyesi vermez; sadece teknik ve istatistiksel verilere dayalı bir analiz simülasyonudur.*
