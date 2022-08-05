# ![PALMS LOGO](ico.ico) PALMS

PALMS or PNRD/iPNRD Arduino Library Management System is a middleware able to integrate Petri net modeling tools (through the use of pnml exported file) with PNRD/iPNRD (Petri Net Inside RFID Database/ inverted PNRD). In this version of PALMS, it can be connected to as many Arduinos as available through MQTT connection. It is mandatory to use Ethernet Shield and one SD card. Each Ardunino Mega can connect up to three PN532 RFID readers. As internal structure, PALMS has two modes, it means, Setup and Runtime.

## SETUP MODE

The feature of Setup mode is pnml convertion and the generation of a 'setup.palms' file as intermediary of PNML and PNRD/iPNRD relationship. Arduino's standard files are stored in startupArduinoFiles directory. Attention: There are two distincts Arduino's files in startupArduinoFiles directory, one for tag initial marking (pnrd_iniTag.ino) and another for reader setup (pnrd_reader), and both must be installed by Arduino IDE manually in advance. PALMS create automaticaly '.pnrd' files with PNRD data structure and this file allows PALMS update PNRD information in "real-time" using MQTT protocol.

## RUNTIME MODE
In the Runtume mode PALMS transfer the Petri Net information to the connected arduinos via MQTT, and receive the data generated from the readers with next state calculus files . Based on these informations, marking vector is updated as well as a runtime history json. If an exception is identified, PALMS shows it in its visual interface. Pnml is updated in order to visualize the whole process through any Petri net modelling tool which is able to read this format. PALMS follows pnml format. PALMS does not deal with exception treatment.

## USING PALMS

1. Install Python3
2. Install PIP
3. Install pip requirements
    ```python
    pip install -r requirements.txt
    ```
4. Execute script
    ```python
    python main.py
    ```

## COMPILING EXECUTABLE ON WINDOWS
Although the method above is preferable and also applicable for windows OS, a second way to run the software is building the executable .exe:

1. Install Pyinstaller
    ```python
    pip install pyinstaller
    ```
2. Execute script
    ```python
    pyinstaller --onefile -w main.py
    ```
The execuble built is found in the dist directory.

# License information
PALMS is licensed under The MIT License (MIT). Which means that you can use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software. But you always need to state that MAPL-UFU is the original author of this software.

This project was started by Roger Carrijo, MQTT versions was developed by Daniel Barbosa Pereira.
