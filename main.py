import cv2
import numpy as np
import pandas as pd
import datetime
from playsound import playsound

# EXCEL LOG
log = []

# Sesin sadece BİR kez çalması için bayrak
alert_played = False

# VIDEO AÇ
cap = cv2.VideoCapture("trafik.mp4")

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
current_frame = 0

while True:
    ret, frame = cap.read()
    current_frame += 1

    if not ret or frame is None or current_frame >= frame_count:
        break

    # ---------------------------
    #   GÖRÜNTÜYÜ KÜÇÜLT (Zoom sorunu çözülür)
    # ---------------------------
    frame = cv2.resize(frame, (960, 540))

    # HSV'ye dönüştür
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # ----------------------------------------------------------
#   TRAFİK LAMBASI TESPİTİ (KIRMIZI - SARI - YEŞİL)
# ----------------------------------------------------------

    # Kırmızı ışık
    lower_red1 = np.array([0, 120, 120])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 120, 120])
    upper_red2 = np.array([179, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)
    
    # Sarı ışık
    lower_yellow = np.array([15, 120, 120])
    upper_yellow = np.array([35, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Yeşil ışık
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([85, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    
    # TRAFİK LAMBASI KONUMU İÇİN ÜÇ MASKENİN BİRLEŞTİRİLMESİ
    traffic_light_mask = cv2.bitwise_or(mask_red, mask_yellow)
    traffic_light_mask = cv2.bitwise_or(traffic_light_mask, mask_green)
    
    # Gürültü temizleme
    kernel = np.ones((5,5), np.uint8)
    traffic_light_mask = cv2.morphologyEx(traffic_light_mask, cv2.MORPH_CLOSE, kernel)
    
    # Trafik lambasının konumunu bul
    contours, _ = cv2.findContours(traffic_light_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    trafik_durumu = None
    
    if contours:
        # En büyük konturu al (bu genelde trafik lambasıdır)
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)
    
        if area > 300:  # trafik lambasının kendi küçük olabilir
            x, y, w, h = cv2.boundingRect(c)
    
    # Işık renk tespiti
    red_area = cv2.countNonZero(mask_red)
    yellow_area = cv2.countNonZero(mask_yellow)
    green_area = cv2.countNonZero(mask_green)
    
    if red_area > 500:
        trafik_durumu = "DUR"
    elif yellow_area > 500:
        trafik_durumu = "BEKLE"
    elif green_area > 500:
        trafik_durumu = "GEC"
    
    # EKRANA YAZ
    if trafik_durumu:
        cv2.putText(frame, f"ISIK: {trafik_durumu}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 3)
    
        # Kırmızıda 1 kere ses
        if trafik_durumu == "DUR" and not alert_played:
            playsound("alert.mp3", block=False)
            alert_played = True

    # ----------------------------------------------------------
    #   TRAFİK İŞARETLERİ (STOP – Üçgen – Daire)
    # ----------------------------------------------------------

    # KIRMIZI MASKE (İŞARETLER İÇİN)
    lower_redA = np.array([0, 90, 90])
    upper_redA = np.array([10, 255, 255])
    lower_redB = np.array([160, 90, 90])
    upper_redB = np.array([179, 255, 255])

    red_maskA = cv2.inRange(hsv, lower_redA, upper_redA)
    red_maskB = cv2.inRange(hsv, lower_redB, upper_redB)
    red_mask = cv2.bitwise_or(red_maskA, red_maskB)

    # Morfolojik temizlik
    kernel = np.ones((5,5), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

    # Contour bul
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)

        # küçük kırmızı bölgeleri alma
        if area < 3000:
            continue

        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        kose = len(approx)

        x, y, w, h = cv2.boundingRect(approx)
        ratio = w / float(h)

        isaret = None

        # STOP işareti (sekizgen)
        if 6 <= kose <= 10 and 0.8 < ratio < 1.2:
            isaret = "DUR ISARETI"

        # dairesel yasaklama / hız sınırı
        elif kose > 7 and 0.8 < ratio < 1.2:
            isaret = "DAIRESEL ISARET"

        if isaret is None:
            continue

        # Çiz
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(frame, isaret, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        # Excel kaydı
        zaman = datetime.datetime.now().strftime("%H:%M:%S")
        log.append({
            "Isaret": isaret,
            "Zaman": zaman,
            "X": x,
            "Y": y,
            "Genislik": w,
            "Yukseklik": h
        })

    # ---------------------------------------------
    #   GÖSTER
    # ---------------------------------------------
    cv2.imshow("Trafik Tespit Sistemi", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# EXCEL ÇIKTISI
df = pd.DataFrame(log)
df.to_excel("kayit.xlsx", index=False)
print("Excel kaydı oluşturuldu: kayit.xlsx")

cap.release()
cv2.destroyAllWindows()