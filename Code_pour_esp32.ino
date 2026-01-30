/*
Code à téléverser sur les ESP32 (S3 et C6)
Fonctionnalités :
- Connexion au réseau WiFi
- Serveur HTTP avec endpoints pour vibration et détection de mouvement
- Gestion du moteur haptique DA7280 via I2C
- Gestion de l'accéléromètre LIS2DW12 via TCA9548A (multiplexeur I2C)
*/

#include <WiFi.h> // Bibliothèque pour le WiFi
#include <WebServer.h> // Bibliothèque pour le serveur HTTP
#include <Wire.h>
#include "Haptic_DA7280.h" // Bibliothèque pour le DA7280
#include <DFRobot_LIS2DW12.h> // Bibliothèque pour le LIS2DW12

// Wifi A CHANGER EN FONCTION DU RESEAU
const char* ssid = "nom_reseau"; 
const char* password = "mdp_hotspot";

// HTTP
WebServer server(80);

// Haptic
Haptic_DA7280 haptic1;
int waveform = 3; // Type de vibration

// TCA
#define TCA_ADDR 0x70
#define ACCE_CHANNEL 0  // Canal où est branché le LIS2DW12

// Fonction pour sélectionner le canal du TCA9548A
void tcaSelect(uint8_t channel) {
  if (channel > 7) return;
  Wire.beginTransmission(TCA_ADDR);
  Wire.write(1 << channel);
  Wire.endTransmission();
}

// Fonction pour vérifier les adresses I2C des périphériques connectés
void scanI2C() {
  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.print("I2C trouvé à 0x");
      Serial.println(addr, HEX);
    }
  }
}

// Accéléromètre
DFRobot_LIS2DW12_I2C acce(&Wire, 0x18); // Attention 0x18 pour boitié droit, 0x19 pour boîtier gauche !!!

// Vibration
void vibrate() {
  tcaSelect(1);  // canal 1 uniquement
  haptic1.setWaveform(1, waveform);
  haptic1.goWait();
  haptic1.stop();
}

// Mouvement detection param
bool mouvement_detecte_flag = false;

// Handlers HTTP
void handleVibrate() {
  vibrate();
  server.send(200, "text/plain", "OK");
}

// Endpoint pour vérifier le mouvement
void handleMovement() {
  if (mouvement_detecte_flag) {
    server.send(200, "application/json", "{\"mouvement\":true}");
    mouvement_detecte_flag = false; // reset après lecture
  } else {
    server.send(200, "application/json", "{\"mouvement\":false}");
  }
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  // I2C SCAN
  tcaSelect(0);
  scanI2C();
  tcaSelect(1);
  scanI2C();

  // Wifi Connection
  WiFi.begin(ssid, password);
  Serial.print("Connexion WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnecte !");
  Serial.println(WiFi.localIP());

  // HAPTIC DA7280 INITIALISATION
  tcaSelect(1);
  if (haptic1.begin() != HAPTIC_SUCCESS) {
    Serial.println("ERREUR : DA7280 non detecte");
    while (1);
  }
  haptic1.setActuatorType(LRA);
  haptic1.setMode(REGISTER_MODE);

  // ACCELEROMETRE LIS2DW12 INITIALISATION
  tcaSelect(ACCE_CHANNEL);
  while(!acce.begin()){
    Serial.println("Communication avec accéléro échouée !");
    delay(1000);
  }
  // Configuration de l'accéléromètre
  acce.softReset();
  acce.setRange(DFRobot_LIS2DW12::e2_g);
  acce.setFilterPath(DFRobot_LIS2DW12::eLPF);
  acce.setFilterBandwidth(DFRobot_LIS2DW12::eRateDiv_4);
  acce.setPowerMode(DFRobot_LIS2DW12::eContLowPwrLowNoise1_12bit);
  acce.setDataRate(DFRobot_LIS2DW12::eRate_200hz);
  acce.setWakeUpThreshold(0.3);
  acce.setWakeUpDur(4);
  acce.setActMode(DFRobot_LIS2DW12::eDetectAct);
  acce.setInt1Event(DFRobot_LIS2DW12::eWakeUp);

  // HTTP SERVER SETUP
  server.on("/vibrate", HTTP_POST, handleVibrate);
  server.on("/movement", HTTP_GET, handleMovement);
  server.on("/ping", HTTP_GET, []() {
    server.send(200, "text/plain", "OK");
  });

  server.begin();
  Serial.println("Serveur HTTP pret");
}

void loop() {
  // HTTP SERVER HANDLER
  server.handleClient();

  // MOUVEMENT DETECTION
  tcaSelect(ACCE_CHANNEL);
  if (acce.actDetected()) {
    Serial.println("Mouvement détecté");
    mouvement_detecte_flag = true;
    delay(100); // pour laisser le capteur repasser en sleep
  }
}
