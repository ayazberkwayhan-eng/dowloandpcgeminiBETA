import speech_recognition as sr
import webbrowser
import google.generativeai as genai
import os
import time
from datetime import datetime
import random
from AppOpener import open as uygulama_ac
import pyautogui  # Klavyeyi senin yerine kullanacak sihirbaz

# Pygame'in açılış yazısını gizlemek için
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame 

API_KEY = "YOUR_GEMİNİ_API_KEY"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=(
        "Sen bu bilgisayarın ta kendisisin ve kullanıcının en yakın yapay zeka dostu Gemini'sin. "
        "Kişiliğin son derece zeki, cana yakın, samimi ve hafif esprili. "
        "Cevapların HER ZAMAN kısa, net ve en fazla 1-2 cümle olmalıdır. Asla sembol kullanma."
    )
)

pygame.mixer.init()

def konus(metin):
    try:
        from gtts import gTTS
        ses_dosyasi = "asistan_ses.mp3"
        
        pygame.mixer.music.unload()
        if os.path.exists(ses_dosyasi):
            try: os.remove(ses_dosyasi)
            except: pass
            
        tts = gTTS(text=metin, lang='tr')
        tts.save(ses_dosyasi)
        
        pygame.mixer.music.load(ses_dosyasi)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
    except Exception as e:
        print(f"\n[Ses Hatası]: {e}")

r = sr.Recognizer()
r.dynamic_energy_threshold = False  
r.energy_threshold = 300            

print("\n🚀 SİSTEM BAŞLATILIYOR...")
konus("Sistem hazır dostum, seni dinliyorum.")

while True:
    ses = ""
    with sr.Microphone() as kaynak:
        print("\n[Dinleniyor...] Konuşabilirsiniz...")
        try:
            audio = r.listen(kaynak, timeout=3, phrase_time_limit=5)
            komut = r.recognize_google(audio, language='tr-TR')
            print(f"Sen: {komut}")
            ses = komut.lower()
        except sr.WaitTimeoutError:
            continue
        except Exception as e:
            continue

    if ses:
        if "dur" in ses or "susuver" in ses or "kes" in ses or "sessiz ol" in ses:
            print("Asistan: Sustum.")
            konus("Sustum.")
            continue
            
        # 🎬 SHORTS/REELS KAYDIRMA KOMUTU (YENİ)
        elif "kaydır" in ses or "geç" in ses or "sonraki" in ses:
            print("[Sistem] Video aşağı kaydırılıyor...")
            # Aşağı yön tuşuna basarak bir sonraki videoya geçer (Sesli onay vermez ki videonun sesiyle karışmasın)
            pyautogui.press('down')
            continue
            
        elif "aç" in ses and not ("youtube" in ses or "google" in ses):
            uygulama_adi = ses.replace("aç", "").strip()
            print(f"[Sistem] Bilgisayarda '{uygulama_adi}' aranıyor...")
            konus(f"Hemen {uygulama_adi} uygulamasını açıyorum.")
            try:
                uygulama_ac(uygulama_adi, match_closest=True) 
            except:
                konus("Uygulamayı bulamadım.")
            continue
            
        elif "youtube" in ses and "aç" in ses:
            konus("YouTube açılıyor.")
            webbrowser.open("https://www.youtube.com")
            continue
            
        elif "google" in ses and "aç" in ses:
            konus("Google açılıyor.")
            webbrowser.open("https://www.google.com")
            continue
            
        elif "saat" in ses and "kaç" in ses:
            su_an = datetime.now().strftime("%H:%M")
            konus(f"Saat şu an {su_an}.")
            continue
            
        elif "yazı tura" in ses or "para at" in ses:
            sonuc = random.choice(["Yazı", "Tura"])
            konus(f"Sonuç {sonuc} geldi.")
            continue
            
        elif "kapat" in ses or "kendini kapat" in ses or "asistanı kapat" in ses:
            konus("Görüşmek üzere dostum!")
            break
            
        else:
            try:
                print("[Sistem] Gemini düşünüyor...")
                response = model.generate_content(ses)
                cevap = response.text
                print(f"Asistan: {cevap}")
                konus(cevap)
            except Exception as e:
                print(f"Hata: {e}")
                konus("Tekrar söyler misin?")