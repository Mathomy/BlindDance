"""
Test de vibrations alternées entre deux ESP32 (S3 et C6).
Vérifie la connexion des 2 ESP32 et du fonctionnement des LRA.

"""

import time
import requests
import wifi_esp32

# URL des ESP32 (à changer selon le réseau hotspot)
ESP32_CONFIG = [
    wifi_esp32.IP_S3,  # ESP32 S3
    wifi_esp32.IP_C6   # ESP32 C6
]

# Intervalle entre vibrations en secondes
INTERVAL = 0.8  

# Nombre total de vibrations à envoyer
TOTAL_VIBRATIONS = 20  

# Fonction pour envoyer une commande de vibration à l'ESP32
def envoyer_vibration(index):
    esp_ip = ESP32_CONFIG[index % len(ESP32_CONFIG)]
    try:
        requests.post(f"{esp_ip}/vibrate", timeout=1.2)
        print(f"Vibration envoyée → {esp_ip}") # Verification console
    except Exception as e:
        print(f"ESP32 non joignable : {esp_ip} | {e}") # Verification console

# Boucle principale pour envoyer des vibrations alternées
def main():
    print("Début des vibrations alternées...")
    for i in range(TOTAL_VIBRATIONS):
        envoyer_vibration(i)
        time.sleep(INTERVAL)

    print("Fin des vibrations.")

if __name__ == "__main__":
    main()
