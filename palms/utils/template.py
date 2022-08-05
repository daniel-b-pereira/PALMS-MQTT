

def pnrd_init_template(n_places,n_transitions,IncidenceMatrix,StartingTokenVector):
    return f'\
{n_places}\n\
{n_transitions}\n\
{{{StartingTokenVector}}}\n\
{{{IncidenceMatrix}}}\n\
'

#def pnrd_init_template(n_places,n_transitions,IncidenceMatrix,StartingTokenVector):
#    return f'\n\
#        #include <Pn532NfcReader.h>                                     \n\
#        #include <SPI.h>                                                \n\
#        #include <PN532_SPI.h>                                          \n\
#        #include <PN532.h>                                              \n\
#        #include <NfcAdapter.h>                                         \n\
#                                                                        \n\
#        int8_t mIncidenceMatrix[] = {{{IncidenceMatrix}}};              \n\
#        uint16_t mStartingTokenVector[] = {{{StartingTokenVector}}};    \n\
#                                                                        \n\
#        int incomingByte = 0;                                           \n\
#                                                                        \n\
#        PN532_SPI pn532spi(SPI, 10);                                    \n\
#        NfcAdapter nfc = NfcAdapter(pn532spi);                          \n\
#                                                                        \n\
#        Pn532NfcReader* reader = new Pn532NfcReader(&nfc);              \n\
#        Pnrd pnrd = Pnrd(reader,{n_places},{n_transitions}, false, false, false);            \n\
#                                                                        \n\
#                                                                        \n\
#        void setup() {{                                                 \n\
#//Initialization of the communication with the reader and with the computer Serial bus\n\
#        Serial.begin(9600);                                             \n\
#        reader->initialize();                                           \n\
#                                                                        \n\
#        // pnrd.setGoalToken(tokenDesejado);                            \n\
#        pnrd.setIncidenceMatrix(mIncidenceMatrix);                      \n\
#        pnrd.setTokenVector(mStartingTokenVector);                      \n\
#                                                                        \n\
#        // pnrd.setAsTagInformation(PetriNetInformation::GOAL_TOKEN);   \n\
#        pnrd.setAsTagInformation(PetriNetInformation::TOKEN_VECTOR);    \n\
#        pnrd.setAsTagInformation(PetriNetInformation::ADJACENCY_LIST);  \n\
#                                                                        \n\
#        Serial.print("\\n\\nInitial recording of PNRD tags.");          \n\
#                                                                        \n\
#        }}                                                              \n\
#                                                                        \n\
#        void loop() {{                                                  \n\
#        if (Serial.available() > 0) {{                                  \n\
#            incomingByte = Serial.read();                               \n\
#                                                                        \n\
#            Serial.print("I received: ");                               \n\
#            Serial.println(incomingByte, DEC);                          \n\
#    }}                                                                  \n\
#        delay(1000);                                                    \n\
#        Serial.println("Place a tag near the reader.");                 \n\
#                                                                        \n\
#        if(pnrd.saveData() == WriteError::NO_ERROR){{                   \n\
#                Serial.println("Tag configurated successfully.");       \n\
#                                                                        \n\
#        }};                                                             \n\
#                                                                        \n\
#        Serial.print("\\n\\n");                                         \n\
#        delay(1000);                                                    \n\
#                                                                        \n\
#        }}                                                              \n\
#        '


def pnrd_arduino_uno_template(n_places,n_transitions,readerId,antenaId,positon_fire=0):
    return f'\
{n_places}\n\
{n_transitions}\n\
{readerId}\n\
{antenaId}\n\
{positon_fire}\n\
'

#def pnrd_arduino_uno_template(n_places,n_transitions,readerId,antenaId,positon_fire=0):
#    return f'\
#        #include <Pn532NfcReader.h>         \n\
#        #include <PN532_HSU.h>              \n\
#        #include <PN532.h>              \n\
#        #include <SPI.h>                \n\
#        #include <PN532_SPI.h>              \n\
#        #include <NfcAdapter.h>             \n\
#                        \n\
#                        \n\
#        uint32_t tagId = 0xFF;             \n\
#        String readerId = "{readerId}";               \n\
#        uint16_t * tokenVector;             \n\
#        uint8_t n_places = {n_places};      \n\
#        uint8_t n_transitions = {n_transitions};               \n\
#        uint8_t position_fire = {positon_fire};              \n\
#        int antenna = {antenaId};                                                   \n\
#        bool tagReadyToContinue = false;                \n\
#        String stringToken;             \n\
#                        \n\
#        //Rotines related with the configuration of the RFID reader PN532               \n\
#        PN532_SPI pn532spi(SPI, 10);                \n\
#        NfcAdapter nfc = NfcAdapter(pn532spi);                     \n\
#        //Creation of the reader and PNRD objects               \n\
#        Pn532NfcReader* reader = new Pn532NfcReader(&nfc);                \n\
#        Pnrd pnrd = Pnrd(reader,n_places,n_transitions,false,false,false);                \n\
#        // -----------------------------------------------------------------------              \n\
#                        \n\
#        void setup() {{                 \n\
#        //Initialization of the communication with the reader and with the computer Serial bus                \n\
#        Serial.begin(9600);                   \n\
#        reader->initialize();                    \n\
#        pnrd.setAsTagInformation(PetriNetInformation::TOKEN_VECTOR);             \n\
#        pnrd.setAsTagInformation(PetriNetInformation::ADJACENCY_LIST);               \n\
#        // pnrd.setAsTagInformation(PetriNetInformation::GOAL_TOKEN);                \n\
#                        \n\
#        }}               \n\
#        void serial_com(                \n\
#            uint32_t tagId,               \n\
#            String readerId,                \n\
#            int antenna,              \n\
#            char ErrorType[100],              \n\
#            String tokenVector,               \n\
#            int fireVector=position_fire              \n\
#            ){{             \n\
#        Serial.println(String("I") + String(tagId,HEX) + String("-A") + String(antenna) + String("-R") + String(readerId) + String("-P")+ String(ErrorType)+ String("-T[") + String(tokenVector)+ String("]")+ String("-F")+ String(fireVector)+String("-EE"));               \n\
#        }}               \n\
#                        \n\
#        void loop() {{              \n\
#        delay(50);               \n\
#                        \n\
#        ReadError readError = pnrd.getData();               \n\
#        delay(50);               \n\
#        if(readError == ReadError::NO_ERROR){{               \n\
#            FireError fireError;               \n\
#            // pnrd.printTokenVector();                \n\
#                        \n\
#            //verifica se é uma nova tag                \n\
#            if(tagId != pnrd.getTagId()){{              \n\
#                tagId = pnrd.getTagId();                \n\
#                FireError fireError = pnrd.fire(position_fire);             \n\
#                        \n\
#                //get token Vector                \n\
#                pnrd.getTokenVector(tokenVector);                \n\
#                stringToken = " ";                \n\
#                for (int32_t place = 0; place < n_places; place++) {{             \n\
#                    if ((n_places -1) == place){{             \n\
#                        stringToken += String(tokenVector[place]);              \n\
#                    }}             \n\
#                    else{{            \n\
#                        stringToken += String(tokenVector[place]);              \n\
#                        stringToken += ",";             \n\
#                    }}             \n\
#                }}             \n\
#                //------------------------------------                \n\
#                        \n\
#                switch (fireError){{             \n\
#                    case FireError::NO_ERROR :                \n\
#                        //Atualizando a tag             \n\
#                        if(pnrd.saveData() == WriteError::NO_ERROR){{              \n\
#                            // pnrd.printGoalToken();                \n\
#                            serial_com(tagId,readerId,antenna,"NO_ERROR",stringToken);             \n\
#                            return;               \n\
#                        }}else{{             \n\
#                            serial_com(tagId,readerId,antenna,"ERROR_TAG_UPDATE",stringToken);             \n\
#                            return;               \n\
#                        }}               \n\
#                        \n\
#                    case FireError::PRODUCE_EXCEPTION :               \n\
#                        serial_com(tagId,readerId,antenna,"PRODUCE_EXCEPTION",stringToken);                \n\
#                    return;               \n\
#                        \n\
#                    case FireError::CONDITIONS_ARE_NOT_APPLIED :              \n\
#                        serial_com(tagId,readerId,antenna,"CONDITIONS_ARE_NOT_APPLIED",stringToken);               \n\
#                    break;                \n\
#                        \n\
#                    case FireError::NOT_KNOWN:                \n\
#                        serial_com(tagId,readerId,antenna,"NOT_KNOWN",stringToken);              \n\
#                    break;                \n\
#                }}                 \n\
#            }}             \n\
#        }}             \n\
#        Serial.flush();\n\
#        }}'


def pnrd_arduino_mega_template(n_places,n_transitions,readerId,antenaId_list):
    return f'\
{n_places}\n\
{n_transitions}\n\
{readerId}\n\
{antenaId_list}\n\
'

#def pnrd_arduino_mega_template(n_places,n_transitions,readerId,antenaId_list):
#    count =0
#    reader_config =''
#    setup_config = ''
#    tag_config = ''
#    loop_config = ''
#    for antenna in antenaId_list:
#        if count<2:
#            reader_config +="\
#        PN532_HSU pn532hsu{0}(Serial{0});\n\
#        NfcAdapter nfc{0}= NfcAdapter(pn532hsu{0});\n\
#        Pn532NfcReader* reader{0} = new Pn532NfcReader(&nfc{0}); \n\
#        Pnrd pnrd{0} = Pnrd(reader{0},n_places,n_transitions,false,false,false);\n\n".format(count)
#        else:
#            reader_config +="\
#        PN532_SPI pn532spi{0}(SPI, 10);\n\
#        NfcAdapter nfc{0} = NfcAdapter(ppn532spi{0});\n\
#        Pn532NfcReader* reader{0} = new Pn532NfcReader(&nfc{0}); \n\
#        Pnrd pnrd{0} = Pnrd(reader{0},n_places,n_transitions,false,false,false);\n\n".format(count) 
#
#        setup_config+="\
#            reader{0}->initialize();\n\
#            pnrd{0}.setAsTagInformation(PetriNetInformation::TOKEN_VECTOR);\n\
#            pnrd{0}.setAsTagInformation(PetriNetInformation::ADJACENCY_LIST);\n\n".format(count)
#
#        tag_config +=f"\
#        uint32_t tagId{count} = 0xFF;\n"
#
#        loop_config += '\n\
#            ReadError readError{0} = pnrd{0}.getData();\n\
#            delay(50);                                      \n\
#            if(readError{0} == ReadError::NO_ERROR){{   \n\
#                FireError fireError{0};                            \n\
#                if(tagId{0} != pnrd{0}.getTagId()){{             \n\
#                    tagId{0} = pnrd{0}.getTagId();                \n\
#                    FireError fireError{0} = pnrd{0}.fire({1});                          \n\
#                    pnrd{0}.getTokenVector(tokenVector);                \n\
#                    stringToken = " ";                \n\
#                    for (int32_t place = 0; place < n_places; place++) {{             \n\
#                        if ((n_places -1) == place){{            \n\
#                            stringToken += String(tokenVector[place]);              \n\
#                        }}             \n\
#                        else{{          \n\
#                            stringToken += String(tokenVector[place]);              \n\
#                            stringToken += ",";             \n\
#                        }}\n\
#                    }}\n\
#                    //------------------------------------                \n\
#                    switch (fireError{0}){{\n\
#                        case FireError::NO_ERROR :                     \n\
#                            if(pnrd{0}.saveData() == WriteError::NO_ERROR){{              \n\
#                                serial_com(tagId{0},readerId,{1},"NO_ERROR",stringToken,{1});             \n\
#                                return;               \n\
#                            }}else{{             \n\
#                                serial_com(tagId{0},readerId,{1},"ERROR_TAG_UPDATE",stringToken,{1});             \n\
#                                return;               \n\
#                            }}               \n\
#                            \n\
#                        case FireError::PRODUCE_EXCEPTION :               \n\
#                            serial_com(tagId{0},readerId,{1},"PRODUCE_EXCEPTION",stringToken,{1});                \n\
#                        return;               \n\
#                            \n\
#                        case FireError::CONDITIONS_ARE_NOT_APPLIED :              \n\
#                            serial_com(tagId{0},readerId,{1},"CONDITIONS_ARE_NOT_APPLIED",stringToken,{1});               \n\
#                        break;                \n\
#                            \n\
#                        case FireError::NOT_KNOWN:                \n\
#                            serial_com(tagId{0},readerId,{1},"NOT_KNOWN",stringToken,{1});              \n\
#                        break;                \n\
#                    }}                 \n\
#                }}             \n\
#            }}'.format(count, antenna)
#        count +=1
#
#    a =f'\n\
#        #include <Pn532NfcReader.h>\n\
#        #include <PN532_HSU.h>\n\
#        #include <PN532.h>\n\
#        #include <SPI.h>\n\
#        #include <PN532_SPI.h>\n\
#        #include <NfcAdapter.h>\n\
#                                \n\
#{tag_config}\n\
#        uint16_t * tokenVector;             \n\
#        uint8_t n_places = {n_places};      \n\
#        uint8_t n_transitions = {n_transitions};               \n\
#        bool tagReadyToContinue = false;                \n\
#        String stringToken;             \n\
#                        \n\
#        String readerId = "{readerId}";\n\
#{reader_config}\n\
#        void setup() {{            \n\
#            //Initialization of the communication with the reader and with the computer Serial bus                \n\
#            Serial.begin(9600);    \n\
#{setup_config}\n\
#        }}\n\
#        void serial_com(                \n\
#            uint32_t tagId,               \n\
#            String readerId,                \n\
#            int antena,              \n\
#            char ErrorType[100],     \n\
#            String tokenVector,         \n\
#            int fireVector            \n\
#            ){{             \n\
#        Serial.println(String("I") + String(tagId,HEX) + String("-A") + String({1}) + String("-R") + String(readerId) + String("-P")+ String(ErrorType)+ String("-T[") + String(tokenVector)+ String("]")+ String("-F")+ String(fireVector)+String("-EE"));               \n\
#        }}               \n\
#                        \n\
#        void loop() {{              \n\
#            delay(50);  \n\
#{loop_config}\n\
#            Serial.flush();  \n\
#        }}'
#    return a


def ipnrd_init_template(n_places,n_transitions,fire_vector):
    return f'\n\
{n_places}\n\
{n_transitions}\n\
{{{fire_vector}}}\n\
'    

#def ipnrd_init_template(n_places,n_transitions,fire_vector):
#    return f'\n\
#        #include <Pn532NfcReader.h>         \n\
#        #include <PN532_HSU.h>              \n\
#        #include <PN532.h>              \n\
#        #include <SPI.h>                \n\
#        #include <PN532_SPI.h>              \n\
#        #include <NfcAdapter.h>    \n\
#            \n\
#        uint16_t mFireVector[] = {{{fire_vector}}};\n\
#        uint8_t n_places = {n_places};\n\
#        uint8_t n_transitions = {n_transitions};\n\
#        //Rotines related with the configuration of the RFID reader PN532      \n\
#        PN532_SPI pn532spi(SPI, 10);                \n\
#        NfcAdapter nfc = NfcAdapter(pn532spi); \n\
#        \n\
#        //Creation of the reader and PNRD objects\n\
#        Pn532NfcReader* reader = new Pn532NfcReader(&nfc);\n\
#        Pnrd pnrd = Pnrd(reader,n_places,n_transitions, false, false,false);\n\
#        \n\
#        void setup() {{  \n\
#        //Initialization of the communication with the reader and with the computer Serial bus\n\
#        Serial.begin(9600); \n\
#        reader->initialize();      \n\
#        \n\
#        //Defining the fire vector to be recorded\n\
#        pnrd.setFireVector(mFireVector);\n\
#        \n\
#        //Setting of the classic iPNRD approach \n\
#        pnrd.setAsTagInformation(PetriNetInformation::FIRE_VECTOR);\n\
#        Serial.print("\\nInitial recording of iPNRD tags.");\n\
#        }}\n\
#        \n\
#        void loop() {{\n\
#        \n\
#        Serial.println("Place a tag near the reader.");\n\
#        \n\
#        if(pnrd.saveData() == WriteError::NO_ERROR){{\n\
#                Serial.println("Tag configurated successfully.");\n\
#        }};\n\
#        \n\
#        Serial.print("\n"); \n\
#        delay(1000); \n\
#        \n\
#        }}\n'


def ipnrd_arduino_uno_template(n_places,n_transitions,readerId,IncidenceMatrix,StartingTokenVector):
    return f'\
{n_places}\n\
{n_transitions}\n\
{readerId}\n\
{{{StartingTokenVector}}}\n\
{{{IncidenceMatrix}}}\n\
'

#def ipnrd_arduino_uno_template(n_places,n_transitions,readerId,IncidenceMatrix,StartingTokenVector):
#    return f'\
#        #include <Pn532NfcReader.h>         \n\
#        #include <PN532_HSU.h>              \n\
#        #include <PN532.h>              \n\
#        #include <SPI.h>                \n\
#        #include <PN532_SPI.h>              \n\
#        #include <NfcAdapter.h>             \n\
#                        \n\
#        int8_t mIncidenceMatrix[] = {{{IncidenceMatrix}}};              \n\
#        uint16_t mStartingTokenVector[] = {{{StartingTokenVector}}};    \n\
#                        \n\
#        uint32_t tagId = 0xFF;             \n\
#        String readerId = "{readerId}";               \n\
#        uint16_t * tokenVector;             \n\
#        uint16_t * fireVector;             \n\
#        uint8_t n_places = {n_places};      \n\
#        uint8_t n_transitions = {n_transitions};               \n\
#        uint8_t position_fire;             \n\
#        int antenna = 1;                                                   \n\
#        bool tagReadyToContinue = false;                \n\
#        String stringToken;             \n\
#                        \n\
#        //Rotines related with the configuration of the RFID reader PN532               \n\
#        PN532_SPI pn532spi(SPI, 10);                \n\
#        NfcAdapter nfc = NfcAdapter(pn532spi);                     \n\
#        //Creation of the reader and PNRD objects               \n\
#        Pn532NfcReader* reader = new Pn532NfcReader(&nfc);                \n\
#        Pnrd pnrd = Pnrd(reader,n_places,n_transitions,false,false,false);                \n\
#        // -----------------------------------------------------------------------              \n\
#                        \n\
#        void setup() {{                 \n\
#        //Initialization of the communication with the reader and with the computer Serial bus                \n\
#        Serial.begin(9600);                   \n\
#        reader->initialize();                    \n\
#        pnrd.setTokenVector(mStartingTokenVector);\n\
#        pnrd.setIncidenceMatrix(mIncidenceMatrix);\n\
#\n\
#        //Setting of the classic iPNRD approach \n\
#        pnrd.setAsTagInformation(PetriNetInformation::FIRE_VECTOR);\n\
#\n\
#        pnrd.setDeviceId(1);\n\
#                        \n\
#        }}               \n\
#        void serial_com(                \n\
#            uint32_t tagId,               \n\
#            String readerId,                \n\
#            int antenna,              \n\
#            char ErrorType[100],              \n\
#            String tokenVector,               \n\
#            int fireVector=position_fire              \n\
#            ){{             \n\
#        Serial.println(String("I") + String(tagId,HEX) + String("-A") + String(antenna) + String("-R") + String(readerId) + String("-P")+ String(ErrorType)+ String("-T[") + String(tokenVector)+ String("]")+ String("-F")+ String(fireVector)+String("-EE"));               \n\
#        }}               \n\
#                        \n\
#        void loop() {{              \n\
#        delay(50);               \n\
#                        \n\
#        ReadError readError = pnrd.getData();               \n\
#        delay(50);               \n\
#        if(readError == ReadError::NO_ERROR){{               \n\
#            FireError fireError;               \n\
#            // pnrd.printTokenVector();                \n\
#                        \n\
#            //verifica se é uma nova tag                \n\
#            if(tagId != pnrd.getTagId()){{              \n\
#                tagId = pnrd.getTagId();                \n\
#                FireError fireError = pnrd.fire();             \n\
#                        \n\
#                //get token Vector                \n\
#                pnrd.getTokenVector(tokenVector);                \n\
#                stringToken = " ";                \n\
#                for (int32_t place = 0; place < n_places; place++) {{             \n\
#                    if ((n_places -1) == place){{             \n\
#                        stringToken += String(tokenVector[place]);              \n\
#                    }}             \n\
#                    else{{            \n\
#                        stringToken += String(tokenVector[place]);              \n\
#                        stringToken += ",";             \n\
#                    }}             \n\
#                }}             \n\
#                //------------------------------------                \n\
#                pnrd.getFireVector(fireVector);                     \n\
#                for (uint32_t  transition = 0; transition < n_transitions; transition++) {{\n\
#                    if(fireVector[transition]==1){{\n\
#                        position_fire = transition;\n\
#                        break;\n\
#                    }};	        \n\
#                }}\n\
#                        \n\
#                switch (fireError){{             \n\
#                    case FireError::NO_ERROR :                \n\
#                        //Atualizando a tag             \n\
#                        if(pnrd.saveData() == WriteError::NO_ERROR){{              \n\
#                            // pnrd.printGoalToken();                \n\
#                            serial_com(tagId,readerId,antenna,"NO_ERROR",stringToken);             \n\
#                            return;               \n\
#                        }}else{{             \n\
#                            serial_com(tagId,readerId,antenna,"ERROR_TAG_UPDATE",stringToken);             \n\
#                            return;               \n\
#                        }}               \n\
#                        \n\
#                    case FireError::PRODUCE_EXCEPTION :               \n\
#                        serial_com(tagId,readerId,antenna,"PRODUCE_EXCEPTION",stringToken);                \n\
#                    return;               \n\
#                        \n\
#                    case FireError::CONDITIONS_ARE_NOT_APPLIED :              \n\
#                        serial_com(tagId,readerId,antenna,"CONDITIONS_ARE_NOT_APPLIED",stringToken);               \n\
#                    break;                \n\
#                        \n\
#                    case FireError::NOT_KNOWN:                \n\
#                        serial_com(tagId,readerId,antenna,"NOT_KNOWN",stringToken);              \n\
#                    break;                \n\
#                }}                 \n\
#            }}             \n\
#        }}             \n\
#        Serial.flush();\n\
#        }}'