
#include <MQTT.h>
#include <Ethernet.h>
#include <SPI.h>
#include "SdFat.h"
#include <Pn532NfcReader.h>
#include <PN532_HSU.h>
#include <PN532.h>
#include <PN532_SPI.h>
#include <NfcAdapter.h>



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


int contador;

String inf;


EthernetClient net;
MQTTClient client_cloud;

//Rotines related with the configuration of the RFID reader PN532 1     
PN532_HSU pn532hsu1(Serial1);
NfcAdapter nfc1 = NfcAdapter(pn532hsu1);

//Rotines related with the configuration of the RFID reader PN532  2    
PN532_HSU pn532hsu2(Serial2);
NfcAdapter nfc2 = NfcAdapter(pn532hsu2);

//Creation of the reader and PNRD objects 1
Pn532NfcReader* reader1 = new Pn532NfcReader(&nfc1);
Pnrd pnrd1 = Pnrd(reader1,int_places,int_transitions);//leitor, no estados e no transicoes 

//Creation of the reader and PNRD objects  2
Pn532NfcReader* reader2 = new Pn532NfcReader(&nfc2);
Pnrd pnrd2 = Pnrd(reader2,int_places,int_transitions);//leitor, no estados e no transicoes

uint32_t tagId1 = 0xFF;
uint32_t tagId2 = 0xFF;


bool tagReadyToContinue = false;


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


//Creation of the reader and PNRD objects 1
    Pn532NfcReader* reader1 = new Pn532NfcReader(&nfc1);
    Pnrd pnrd1 = Pnrd(reader1,int_places,int_transitions);//leitor, no estados e no transicoes
    
//Initialization of the communication with the reader and with the computer Serial bus     
    reader1->initialize(); 
    

//Setting of the classic PNRD approach  
  pnrd1.setAsTagInformation(PetriNetInformation::TOKEN_VECTOR);
  pnrd1.setAsTagInformation(PetriNetInformation::ADJACENCY_LIST);



//Creation of the reader and PNRD objects
    Pn532NfcReader* reader2 = new Pn532NfcReader(&nfc2);
    Pnrd pnrd2 = Pnrd(reader2,int_places,int_transitions);//leitor, no estados e no transicoes
    
//Initialization of the communication with the reader and with the computer Serial bus     
    reader2->initialize(); 
    

//Setting of the classic PNRD approach  
  pnrd2.setAsTagInformation(PetriNetInformation::TOKEN_VECTOR);
  pnrd2.setAsTagInformation(PetriNetInformation::ADJACENCY_LIST);

  Serial.println("\nMachine 2: Reader."); 
 
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



  delay(1000);
  
  //Tag reading
  ReadError readError = pnrd1.getData();

 //In case of a successful reading  
  if(readError == ReadError::NO_ERROR){
    
    FireError fireError;
    
    //Checks if it's a new tag
    if(tagId1 != pnrd1.getTagId()){
        tagId1 = pnrd1.getTagId();
        Serial.print("\nNew part. ID: ");
        Serial.println(tagId1, HEX);
        
        tagReadyToContinue = false;

         //Fire of transition 0
        FireError fireError = pnrd1.fire(0);
     
    switch(fireError){
        case FireError::NO_ERROR :   
        
          //Save new information in tag          
          if(pnrd1.saveData() == WriteError::NO_ERROR){
               Serial.println("NO ERROR.");
               inf = "NO ERROR.";
               return;
          }else{
               Serial.println("Error in the tag.");
               return;
          };
          return;

        case FireError::PRODUCE_EXCEPTION :
          Serial.println("Error: exception.");
          inf = "PRODUCE EXCEPTION.";
          break;

        case FireError::CONDITIONS_ARE_NOT_APPLIED :   
          Serial.println("Error: CONDITIONS ARE NOT APPLIED");
          inf = "CONDITIONS ARE NOT APPLIED";          
          break;
    } 
    

        
    }
  }



  
  delay(1000);
  
  //Tag reading
  ReadError readError2 = pnrd2.getData();

 //In case of a successful reading  
  if(readError2 == ReadError::NO_ERROR){
    
    FireError fireError;
    
    //Checks if it's a new tag
    if(tagId2 != pnrd2.getTagId()){
        tagId2 = pnrd2.getTagId();
        Serial.print("\nNew part. ID: ");
        Serial.println(tagId2, HEX);
        
        tagReadyToContinue = false;

         //Fire of transition 0
        FireError fireError = pnrd2.fire(0);
     
    switch(fireError){
        case FireError::NO_ERROR :   
        
          //Save new information in tag          
          if(pnrd1.saveData() == WriteError::NO_ERROR){
               Serial.println("NO ERROR.");
               inf = "NO ERROR.";
               return;
          }else{
               Serial.println("Error in the tag.");
               return;
          };
          return;

        case FireError::PRODUCE_EXCEPTION :
          Serial.println("Error: exception.");
          inf = "PRODUCE EXCEPTION.";
          break;

        case FireError::CONDITIONS_ARE_NOT_APPLIED :   
          Serial.println("Error: CONDITIONS ARE NOT APPLIED");
          inf = "CONDITIONS ARE NOT APPLIED";          
          break;
    } 
    

        
    }
  }

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
  if (payload != "End"){
    total_msg += payload;
    total_msg += '\n';
  }  
  if (payload == "Atualizar") {
     total_msg = "";
  }
  if (payload == "End") {
     Serial.println("Salvando no cartão SD");
     SD.remove("PNRDINFO.pnrd");
     myFile = SD.open("PNRDINFO.pnrd", FILE_WRITE);
     myFile.println(total_msg);
     myFile.close();
  }

  if (payload == "Info") {
    client_cloud.publish("PALMS-MQTT", inf);

  }
 }
