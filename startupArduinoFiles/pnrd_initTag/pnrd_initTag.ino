
#include <MQTT.h>
#include <Ethernet.h>
#include <SPI.h>
#include "SdFat.h"
#include <Pn532NfcReader.h>
#include <PN532_HSU.h>



byte mac[] = {0xE4, 0x83, 0x26, 0xC4, 0x9a, 0xED};
byte ip[] = {10, 0, 208, 12};
byte gate[] = {10 , 0, 208, 1};
byte masc[] = {255, 255, 252, 0};
byte dns[] = {200, 19, 146, 201};


#define SD_CS_PIN 4
File myFile;
SdFat SD;

unsigned long lastMillis = 0;
String total_msg;

uint8_t int_places;
uint8_t int_transitions;

String places;
String transitions;
String matriz;
String vetor;

int n;
int j;
char temp;
String vetor_temp;
String matriz_temp;

int k;
int cont;
int l;

String msg;
String valores;
int contador;


EthernetClient net;
MQTTClient client_cloud;

//Rotines related with the configuration of the RFID reader PN532      
PN532_HSU pn532hsu(Serial1);
NfcAdapter nfc = NfcAdapter(pn532hsu);

//Creation of the reader and PNRD objects
Pn532NfcReader* reader = new Pn532NfcReader(&nfc);
Pnrd pnrd = Pnrd(reader,int_places,int_transitions);//leitor, no estados e no transicoes


void setup() {

    Serial.begin(115200);
    
  // Open serial communications and wait for port to open:
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }


  Serial.print("Initializing SD card...");

  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("initialization done.");


// Configurações para o uso do MQTT
    Ethernet.begin(mac, ip, dns, gate, masc);
    client_cloud.begin("mqtteste.cloud.shiftr.io", net);
    client_cloud.onMessage(messageReceived);
    connect();



//////LENDO CARTÃO SD///////
    
    Serial.println("Lendo o cartão SD");
    contador = 0;
    myFile = SD.open("PNRDINFO.pnrd");
    if (myFile) {
      while (myFile.available()) {
        String list = myFile.readStringUntil('\n');
        contador++; 
        if (contador == 1){
          places = list;   
          Serial.println("Places = " + places);     
       }
       if (contador == 2){
          transitions = list;
          Serial.println("Transitions = " + transitions);
       }
       if (contador == 3){
          vetor = list;
          Serial.println("Vetor = " + vetor);
       }
       if (contador == 4){
          matriz = list;
          Serial.println("Matriz = " + matriz);
       }
       }
      // close the file:
      myFile.close();
    } else {
      // if the file didn't open, print an error:
      Serial.println("error opening test.txt");
    }  


    
/////DESCOBRINDO VALORES DE PLACE E TRANSITIONS///////
    
   int_places = places.toInt();
   int_transitions = transitions.toInt();
   Serial.print("Places = " ); 
   Serial.println(int_places); 
   Serial.print("Transitions = " ); 
   Serial.println(int_transitions); 

//////DESCOBRINDO VALOR DO VETOR DE ESTADOS/////////

   n = vetor.length();
   j = 0;
   for (int  i = 1; i < (n-1) ; i = i+2){
     vetor_temp += vetor.charAt(i);
   }
   j = vetor_temp.length();

   uint16_t StartingTokenVector[j];
   
   for (int  i = 0; i < j ; i++){
    temp = vetor_temp.charAt(i);
    StartingTokenVector[i] =(temp-48);
   }
   Serial.print ("Vetor de estados = {");
   for (int  i = 0; i < j ; i++){
    Serial.print(StartingTokenVector[i]);
    Serial.print(",");
   }
   Serial.println("}");



//////DESCOBRINDO VALOR DA MATRIZ DE INCIDENCIA/////////

   n = matriz.length();
   j = 0;
   for (int  i = 1; i < (n-1) ; i++){
    temp = matriz.charAt(i);
    if (temp == 44){
      i++;
    }
    if(temp == 45){
       matriz_temp += matriz.charAt(i);
       i++;
       matriz_temp += matriz.charAt(i);
      }
    else {
       matriz_temp += matriz.charAt(i);
      }
   }
   j = matriz_temp.length();


   int8_t tempIncidenceMatrix[j];

   k = 0;
   cont = 0;


   for (int  i = 0; i < j ; i++){
    temp = matriz_temp.charAt(i);
    if (temp == 45 ){
      tempIncidenceMatrix[k] = (temp);
      temp = matriz_temp.charAt(i+1);
      i++;
      tempIncidenceMatrix[k] += (temp-48);
      k++;
      cont++;
    }
    else {
      tempIncidenceMatrix[k] = (temp-48);
      k++;
    }
   }

   l = j- cont;

   int8_t IncidenceMatrix[l];

  
   for (int  i = 0; i < l ; i++){
    if (tempIncidenceMatrix[i] == 46){
      IncidenceMatrix[i] = (tempIncidenceMatrix[i]-47);
    }
    else {
      IncidenceMatrix[i] = (tempIncidenceMatrix[i]);
    }
   }
   Serial.print("Matriz de incidência = {");
   for (int  i = 0; i < l ; i++){
    Serial.print(IncidenceMatrix[i]);
    Serial.print(",");
   }
   Serial.println("}");



//Creation of the reader and PNRD objects
    Pn532NfcReader* reader = new Pn532NfcReader(&nfc);
    Pnrd pnrd = Pnrd(reader,int_places,int_transitions);//leitor, no estados e no transicoes
    
//Initialization of the communication with the reader and with the computer Serial bus     
    reader->initialize(); 

    pnrd.setIncidenceMatrix(IncidenceMatrix);
    pnrd.setTokenVector(StartingTokenVector);

//Setting of the classic PNRD approach  
    pnrd.setAsTagInformation(PetriNetInformation::TOKEN_VECTOR);
    pnrd.setAsTagInformation(PetriNetInformation::ADJACENCY_LIST);
    Serial.print("\nMachine 1: Initial tag recording.");

 
}

void loop() {
  client_cloud.loop();
  delay(10);

  // check if connected
  if (!client_cloud.connected()) {
    connect();
  }

  // publish a message roughly every second.
  if (millis() - lastMillis > 300000) {
    lastMillis = millis();
    client_cloud.publish("PALMS-MQTT", "Arduino conectado");
  }


   Serial.print("Places = " ); 
   Serial.println(int_places); 
   Serial.print("Transitions = " ); 
   Serial.println(int_transitions); 


///Saving PNRD values in Tag////
  Serial.println("Place an tag to be configurated.");

 
  if(pnrd.saveData() == WriteError::NO_ERROR){
        Serial.println("Tag configurated successfully.");
  };

  Serial.print('\n');
  delay(1000);

}


void connect() {
    Serial.print("Conectando...");
    while (!client_cloud.connect("Arduino", "mqtteste", "testes")){
        Serial.print(".");
        delay("1000");
    }
    Serial.println("\nConectado!");

    client_cloud.subscribe("PALMS-MQTT");
}


void messageReceived(String &topic, String &payload){
  Serial.println(topic + ": " + payload);
  if (payload != "Fim"){
    total_msg += payload;
    total_msg += '\n';
  }  
  if (payload == "Iniciar") {
     total_msg = "";
  }
  if (payload == "Fim") {
     Serial.println("Salvando no cartão SD");
     SD.remove("PNRDINFO.pnrd");
     myFile = SD.open("PNRDINFO.pnrd", FILE_WRITE);
     myFile.println(total_msg);
     myFile.close();
  }

  if (payload == "Info") {

  }
 }
