import yfinance as yf
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

# --- AYARLAR ---
GMAIL_ADRESI = os.getenv("GMAIL_ADRESI")
GMAIL_SIFRESI = os.getenv("GMAIL_SIFRESI")
ALICI_MAILLER = os.getenv("ALICI_MAILLER").split(",")

# --- MATEMATİK MOTORU ---
def calculate_sma(series, length): return series.rolling(window=length).mean()
def calculate_ema(series, length): return series.ewm(span=length, adjust=False).mean()
def calculate_rsi(series, length=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0))
    loss = (-delta.where(delta < 0, 0))
    avg_gain = gain.ewm(alpha=1/length, min_periods=length, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/length, min_periods=length, adjust=False).mean()
    return 100 - (100 / (1 + (avg_gain / avg_loss)))

def analiz_yap(symbol, mode="NDX"):
    print(f"{symbol} analiz ediliyor...")
    df = yf.download(symbol, period="5y", interval="1d", multi_level_index=False)
    if df.empty or len(df) < 500: # 500 günlük veri yoksa
        raise ValueError(f"{symbol} için yeterli veri çekilemedi!")
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
    close = df['Close']
    
    s200_s = calculate_sma(close, 200)
    s500_s = calculate_sma(close, 500)
    e610_s = calculate_ema(close, 610)
    rsi_s = calculate_rsi(close, 14)
    
    dClose = float(close.values[-1])
    s200, s500, e610, rsiV = float(s200_s.values[-1]), float(s500_s.values[-1]), float(e610_s.values[-1]), float(rsi_s.values[-1])
    ratio200, ratio500 = dClose / s200, dClose / s500

    if mode == "NDX":
        proximity = s200 * 1.038
        prev_s200 = float(s200_s.values[-9])
        if dClose < e610 or (dClose < s500 and rsiV < 30):
            res = ("KRİZ FIRSATI!", "BOSS HÜCRE (5.000₺)", "1-2 GÜNDE BİR", "#8e44ad")
        elif dClose < s500 or (dClose < s200 and rsiV < 30):
            res = ("BÜYÜK İNDİRİM", "BÜYÜK HÜCRE (1.500₺-2.000₺)", "1-3 GÜNDE BİR", "#c0392b")
        elif dClose < s200 or (dClose < proximity and rsiV < 30) or (dClose < proximity and s200 < prev_s200):
            res = ("İNDİRİM", "ORTA HÜCRE (500₺-750₺-1.000₺)", "2-4 GÜNDE BİR", "#d35400")
        elif ratio200 >= 1.24 or (ratio200 >= 1.21 and ratio500 >= 1.40):
            res = ("AŞIRI ŞİŞİK", "ALIMI DURDUR", "DUR!", "#7b241c")
        elif ratio200 >= 1.18 and (rsiV >= 76.5 or ratio500 >= 1.38):
            res = ("PAHALI", "MİNİMUM (50₺)", "14 GÜNDE BİR", "#e74c3c")
        elif ratio200 >= 1.14 or ratio500 >= 1.32 or rsiV >= 70.8:
            res = ("ISINMIŞ", "KÜÇÜK (50₺-100₺)", "7-14 GÜNDE BİR", "#f39c12")
        elif dClose < proximity:
            res = ("DESTEK YAKIN (PUSU)", "ORTA (200₺-500₺)", "4-7 GÜNDE BİR", "#16a085")
        else:
            res = ("RUTİN", "KÜÇÜK HÜCRE (50₺-100₺-200₺)", "HAFTADA BİR", "#27ae60")
    else: # GOLD MODE
        proximity = s200 * 1.04
        prev_s200 = float(s200_s.values[-16])
        if ratio200 < 0.94 or (dClose < e610 and rsiV < 27.4):
            res = ("KRİZ FIRSATI!", "BOSS HÜCRE (5.000₺)", "1-2 GÜNDE BİR", "#8e44ad")
        elif (ratio200 < 0.97 and ratio500 < 1.00) or (dClose < s500 and rsiV < 34):
            res = ("BÜYÜK İNDİRİM", "BÜYÜK HÜCRE (1.500₺-2.000₺)", "1-3 GÜNDE BİR", "#c0392b")
        elif dClose < s200 or (dClose < proximity and rsiV < 34) or (dClose < proximity and s200 < prev_s200):
            res = ("İNDİRİM", "ORTA HÜCRE (500₺-750₺-1.000₺)", "2-4 GÜNDE BİR", "#d35400")
        elif ratio200 >= 1.30 or (ratio200 >= 1.21 and rsiV >= 83.3) or (ratio500 >= 1.47):
            res = ("AŞIRI ŞİŞİK", "ALIMI DURDUR", "DUR!", "#7b241c")
        elif ratio200 >= 1.17 and (rsiV >= 77.7 or ratio500 >= 1.37):
            res = ("PAHALI", "MİNİMUM (50₺)", "14 GÜNDE BİR", "#e74c3c")
        elif ratio200 >= 1.13 or rsiV >= 69.5:
            res = ("ISINMIŞ", "KÜÇÜK (50₺-100₺)", "7-14 GÜNDE BİR", "#f39c12")
        elif dClose < proximity:
            res = ("DESTEK YAKIN (PUSU)", "ORTA (200₺-500₺)", "4-7 GÜNDE BİR", "#16a085")
        else:
            res = ("RUTİN", "KÜÇÜK HÜCRE (50₺-100₺-200₺)", "HAFTADA BİR", "#27ae60")
            
    return {"status": res[0], "action": res[1], "freq": res[2], "color": res[3], "price": dClose}

def mail_gonder(ndx, xau, usd_rate, eur_rate, btc_price, report_date):
    print(f"3. Adım: Stratejik rapor oluşturuluyor...")
    
    if ndx['status'] in ["KRİZ FIRSATI!", "BÜYÜK İNDİRİM", "İNDİRİM", "DESTEK YAKIN (PUSU)", "RUTİN"]:
        ozet = f"""<b>Servet Odaklı Hamle:</b> Nasdaq şu an toplama bölgesinde. 
        Genç yaşlarda başlanan servet yaratma planı için volatilitenin riskini değil, getiri potansiyelini kucaklama zamanı. 
        AFT fonu için raporun yönlendirdiği gibi kademeli alımlara öncelik verilmelidir; bugünkü derin görünen düşüşler, uzun vadeli servet yolculuğunda sadece 'plajda bir kum tanesi' hükmündedir."""
        ozet_renk = "#27ae60"
    else: 
        if xau['status'] in ["KRİZ FIRSATI!", "BÜYÜK İNDİRİM", "İNDİRİM", "DESTEK YAKIN (PUSU)", "RUTİN"]:
            ozet = f"""<b>Stratejik Korunma:</b> Nasdaq '{ndx['status']}' bölgesine ulaşarak ısınmıştır. 
            Bu aşamada serveti korumak ve fırsat kollamak adına rota, altına (KZL Fonu) çevrilmelidir. 
            Altın şu an '{xau['status']}' durumunda olduğu için nakit akışını buraya yönlendirmek istatistiksel olarak daha güvenli bir limandır."""
            ozet_renk = "#d35400"
        else:
            ozet = f"""<b>Tam Pusu Modu:</b> Hem Nasdaq hem de Altın riskli (görece pahalı) bölgelerdedir. 
            Servet yaratmak kadar, yaratılanı korumak da sanattır. Her iki varlık da soğuyana kadar 
            yeni mermileri harcamayıp nakit/para piyasası fonlarında beklemek en akılcı hamle olacaktır."""
            ozet_renk = "#c0392b"

    msg = MIMEMultipart()
    msg['From'] = GMAIL_ADRESI
    msg['To'] = ", ".join(ALICI_MAILLER)
    msg['Subject'] = f"📊 Servet Raporu: NDX ({ndx['status']}) | XAU ({xau['status']})"
    
    body = f"""
    <html>
        <body style="font-family: 'Segoe UI', Tahoma, sans-serif; color: #333; line-height: 1.6; background-color: #f4f7f6; padding: 20px;">
            <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 25px; border-radius: 12px; background-color: #ffffff;">
            
                <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin-bottom: 20px;">
                    <tr>
                        <td align="left" style="padding-bottom: 5px;">
                            <div style="background-color: #f8f9fa; border: 1px solid #eee; padding: 5px 10px; border-radius: 20px; font-size: 0.65em; color: #666; font-weight: bold; display: inline-block; white-space: nowrap;">
                                🇺🇸 USD: {usd_rate:.2f}₺ | 🇪🇺 EUR: {eur_rate:.2f}₺ | <span style="color: #f1c40f;">₿</span> BTC: {btc_price:,.0f}$
                            </div>
                        </td>
                        <td align="right" style="padding-bottom: 5px; vertical-align: top;">
                            <div style="background-color: #f8f9fa; border: 1px solid #eee; padding: 5px 10px; border-radius: 20px; font-size: 0.65em; color: #666; font-weight: bold; display: inline-block; white-space: nowrap;">
                                📅 {report_date}
                            </div>
                        </td>
                    </tr>
                </table>

                <h2 style="text-align: center; color: #2c3e50; margin-bottom: 5px;">Varlık Yönetimi ve Günlük Strateji Raporu</h2>
                <p style="text-align: center; font-size: 0.85em; color: #7f8c8d; margin-top: 0;">Uzun Vadeli Karar Destek Mekanizması</p>
                <hr style="border: 0; border-top: 2px solid #3498db; width: 60px; margin-bottom: 25px;">
                
                <div style="background-color: {ndx['color']}; color: white; padding: 12px; border-radius: 6px 6px 0 0; font-weight: bold; font-size: 1.1em;">
                    主 NASDAQ (AFT FON): {ndx['status']}
                </div>
                <div style="padding: 15px; border: 1px solid #eee; border-top: 0; margin-bottom: 20px; background-color: #fafafa;">
                    Fiyat: <b>{ndx['price']:,.0f}$</b><br>
                    Matris Hamlesi: <b>{ndx['action']}</b><br>
                    Alım Frekansı: <b>{ndx['freq']}</b>
                </div>

                <div style="background-color: {xau['color']}; color: white; padding: 10px; border-radius: 6px 6px 0 0; font-weight: bold; opacity: 0.9;">
                    ⚖️ ALTIN (KZL FON): {xau['status']}
                </div>
                <div style="padding: 12px; border: 1px solid #eee; border-top: 0; margin-bottom: 25px; background-color: #fafafa; font-size: 0.9em;">
                    Fiyat: {xau['price']:,.0f}$ | Hamle: {xau['action']} | Frekans: {xau['freq']}
                </div>

                <div style="background-color: {ozet_renk}15; border-left: 5px solid {ozet_renk}; padding: 18px; border-radius: 4px;">
                    <strong style="color: {ozet_renk}; font-size: 1.1em;">Stratejik Analiz:</strong><br>
                    <p style="margin-top: 8px; color: #34495e;">{ozet}</p>
                </div>

                <div style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">
                    <p style="margin: 0; font-weight: bold; color: #2c3e50; font-size: 1.1em;">Yusuf Emre ÖZDEN</p>
                    <a href="https://yusufemreozden.com" style="color: #3498db; text-decoration: none; font-size: 0.95em;">yusufemreozden.com</a>
                </div>

                    <p style="font-size: 0.8em; color: #888; text-align: center; margin-top: 40px; line-height: 1.6; border-top: 1px solid #eaeaea; padding-top: 18px;">
                    <i>Bu rapor, Yusuf Emre ÖZDEN tarafından geliştirilmiş algoritmik analiz sistemleri ile otomatik olarak üretilmiştir.</i><br>
                    <span style="color: #999;">© 2026 Y.E.Ö. — Tüm hakları saklıdır.</span>
                </p>
            </div>
        </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(GMAIL_ADRESI, GMAIL_SIFRESI)
        server.sendmail(GMAIL_ADRESI, ALICI_MAILLER, msg.as_string())

if __name__ == "__main__":
    try:
        ndx = analiz_yap("^NDX", "NDX")
        xau = analiz_yap("GC=F", "GOLD")
        usd_data = yf.download("USDTRY=X", period="5d", multi_level_index=False)
        eur_data = yf.download("EURTRY=X", period="5d", multi_level_index=False)
        ## oil_data = yf.download("BZ=F", period="5d", multi_level_index=False)
        btc_data = yf.download("BTC-USD", period="5d", multi_level_index=False)
        usd_rate = float(usd_data['Close'].iloc[-1])
        eur_rate = float(eur_data['Close'].iloc[-1])
        ## oil_price = float(oil_data['Close'].iloc[-1])
        btc_price = float(btc_data['Close'].iloc[-1])
        report_date = datetime.now().strftime("%d.%m.%Y")
        mail_gonder(ndx, xau, usd_rate, eur_rate, btc_price, report_date)
        print(f"✅ Rapor başarıyla iletildi!")
    except Exception as e:
        print(f"❌ HATA: {e}")
