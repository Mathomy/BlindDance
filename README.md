# BlindDance
A rythm game for visually impaired people.

# Table of Contents
1. [Introduction](#Introduction)
2. [How to play](#How-to-play)
3. [Game interface](#Game-interface)
4. [mitain/CAO](#mitain/CAO)
5. [Electronic Circuits](#Electronic-Circuits)
6. [Game Interface](#Game-Interface)
7. [Issue and futur improvement](#Issue-and-futur-improvement)
8. [Contact us](#Contact-us)


## Introduction

BlindRevolution is a video game designed to allow people with visual impairments to play a rhythm and dance game inspired by titles such as Just Dance or Dance Dance Revolution.

To play, users wear two mittens: one on the right arm and one on the left arm. Through these mittens, players receive vibrations on one of their arms, indicating which arm they should raise. The device is equipped with an accelerometer that detects whether the performed movement is correct or not.

Game navigation is based on a fully vocal interface. A voice guides the player through the menus and the different stages of the game, while interactions are carried out using the keyboard to respond to the vocal instructions.

Note: The game has been implemented using royalty-free music. You can modify or add new music tracks (in .mp3 format) in the following folders:

- Musique > Niveau1
- Musique > Niveau2
- Musique > Niveau3

## How to play
Here is a step by step guide on how to play :
- create a hotspot on your computer --> go on your parameter and search hotspot, then you need to adapt the esp32 code with the name of your hotspot and your password. You will see the devices connected on your hotspot and their ip adress (see [Electronic Circuits](#Electronic-Circuits) )
- wear the mitain, box upside, then power on the device, push the switch toward the back of the box.
- enter the ip adress on the game file wifi_esp32.py, jeu.py and test_vibration.py (see [Game interface](#Game-Interface))
- launch the game (main.py) it will start to link with the two devices, you should feel a vibration.
- use the number on your keyboard to navigate on the menu to start a game.

## Game interface

The game interface is based on the Python library pyttsx3, which is used for text-to-speech synthesis. The entire project is structured into several files that communicate with each other.

Here the file organization:

- [**menu.py**](/main.py): Manages the main game menu and presents the first choices to the player (start a game, quit, etc.).

- [**menu_musique.py**](/menu_musique.py): Allows the player to choose the difficulty level and the music track. For each track, a 5-second audio preview is played to help the player make a choice.

- [**jeu.py**](/jeu.py) : Contains the main game logic: music analysis, vibration management, movement detection, score calculation, and vocal feedback to the player. The librosa library is used to analyze the music and extract beats. These beats are used as time references to trigger vibrations (1 vibration every 4 beats in this implementation).
The ANTICIPATION variable defines the anticipation time (in seconds) before the beat.
The vibration is sent randomly to one of the two mittens, slightly before the musical beat to give the player time to react.
After a vibration is sent, the game opens a time validation window (2 beats after the vibration, see the function verifier_mouvement) during which it checks whether a correct movement is detected by the ESP32 accelerometer.
At the end of the music, the player’s score is calculated, and they earn between 1 and 3 stars depending on their performance.

- [**tts.py**](/tts.py) : Contains the parler() function, which makes the text spoken by the voice synthesis.
The voice speed can be adjusted by modifying the following value: _engine.setProperty('rate', 200)

- [**outils.py**](/outils.py): Groups utility functions used in the game:
stop(): quit the game
repete(): repeat the instructions
retour(): return to the previous menu

- [**audio.py**](audio.py): Manages music playback and sound effects (success, error, star reward, etc.).


## Mitain/CAO

To secure the circuit, we designed a case in Fusion 360 and then 3D-printed it. Openings were made for the USB-C port and for the wires of the LRA actuators and the battery. Finally, an on/off button was added on the top of the case.

characteristic of the case :
- Interior: H: **30 mm, W: 65 mm, L: 50 mm**
- Exterior: **35 mm × 70 mm × 55 mm**
- The screw are m2 or m3 depending on the precision of the 3d printer.
- one hole for the wires, one for the usb c plug and one for the switch

Finally, we sewed the mittens, which (we think) ideally allow:

- Easy wearing of the mittens.

- LRA motors to be placed directly on the areas where vibrations are best felt (upper wrist + forearm muscle).

- Wireless use of the device (the mittens are long enough to fit the case with all the electronic components inside).

## Electronics

### Used Components

#### XIAO ESP32S3 + and XIAO ESP32C6

**Datasheets:**
- [Getting Started with Seeed Studio XIAO ESP32S3 Series](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/)
- [Getting Started with Seeed Studio XIAO ESP32C6](https://wiki.seeedstudio.com/xiao_esp32c6_getting_started/)

**Role:**
- Management of WiFi communication with the PC  
- Reception of vibration commands  
- Reading of motion data (accelerometer)  
- Coordination between all I2C components (haptic driver, accelerometer)  
- Each ESP32 is connected to the PC WiFi hotspot  

---

#### TCA9548A Multiplexer

**Datasheet:**
- [Low Voltage 8-Channel I2C Switch With Reset](https://cdn-shop.adafruit.com/datasheets/tca9548a.pdf)

Two haptic drivers use the same I2C address.  
A multiplexer is therefore required to differentiate them and avoid I2C bus conflicts.

---

#### Haptic Driver – DA7280

**Datasheet:**
- [Haptic Driver DA7280](https://cdn.sparkfun.com/assets/a/e/d/1/9/da7280_datasheet_3v0.pdf)

**Library used:**
- [GitHub – PatternAgents / Haptic_DA7280](https://github.com/PatternAgents/Haptic_DA7280/tree/master)

**Role:**
- Generates and precisely controls vibrations  
- Drives LRA motors  
- Allows definition of waveforms, durations, and intensities  
- Better haptic control than PWM  

---

#### LRA

**Datasheet:**
- [LRA HD-VA3222](https://api.puiaudio.com/filename/HD-VA3222.pdf)

**Role:**
- Produces vibration  
- Non-polarized motor  
- Requires current peaks managed by the DA7280 driver  

---

#### Accelerometer

**Datasheet:**
- [Gravity: I2C LIS2DW12 Accelerometer](https://wiki.dfrobot.com/Gravity_I2C_LIS2DW12_Triple_Axis_Accelerometer_SKU_SEN0409)

**Library used (recommended by the datasheet):**
- [GitHub DFRobot / DFRobot_LIS](https://github.com/DFRobot/DFRobot_LIS)

**Role:**
- Motion detection  
- Sends an event when the bracelet moves
- Parameters configured on the ESP32

### Battery 
 Because the LRA can use a lot of current, We choose "big" battery with 1000 and 800 mha. We believe that charging can be tedious for visually impaired people. so high autonomy -> no need to charge often. be careful, the accelerometer can fried if supplied directly by the battery ( current too high) for the LRA driver it is the opposite, the esp32 can't deliver enought current with the 3v3 output. 

### Global Electronic Architecture
![Global electronic architecture](archi_projet_design.JPG)
*Figure 1 – Global electronic architecture of one bracelet*

### Embedded Code Overview

The ESP32s connect to the PC using a WiFi hotspot.  
Each ESP32 is assigned an IP address and communicates directly with the game running on the computer.

Communication between the PC and the ESP32s is based on HTTP.  
HTTP is a simple request–response protocol: the PC sends a request to the ESP32, the ESP32 executes the action and returns a response, then the connection is closed.

Two main functionalities are handled by the embedded code:

- **Vibration control**  
  When an HTTP request is received, the ESP32 triggers a vibration by selecting the correct I2C channel and sending a waveform command to the haptic driver.

- **Motion detection**  
  The accelerometer continuously monitors movement.  
  When a movement is detected, the ESP32 stores this information and sends it to the PC upon request.



## Issue and futur improvement

Several improvements can be made to the game. Here are the ones we identified during our project:

**Interface improvements**:

- Allow interrupting the voice to respond immediately.

- Allow navigating between music tracks while previews are playing (useful when there are many tracks).

- Add game settings for a complete experience (volume, enable/disable success or failure sounds).

**Mittens and case:**

- Strengthen the external soldering of the LRA motors.

- Improve access to the USB-C port (currently difficult for visually impaired users). Maybe create the 3 holes in the CAO file.

- Add Braille information on the case (on/off button, USB-C port, right/left hand).

**Circuit:**

- Add a battery level indicator
- change the esp32 s3+ for a c6 for a more stable connexion. ( No informations found in datasheet about this issue. It is just an empirical observation, maybe the wifi antenna is dammaged)

**Code:**

- Switch from HTTP requests to sockets to reduce latency and allow faster vibration updates.
- detect vertical and horizontal movement instead of just a movement.

**Gameplay:**

- Add more movement

- Add a “calibration” phase: before playing, ask the player to lift their arms in each direction to register a personalized movement validation window --> Visually impaired people tend to make movement with less amplitude than sighted people.

## Contact us :

- camelia.alitouche0@gmail.com
- margot.porteneuve@gmail.com
- tlamy80@gmail.com



