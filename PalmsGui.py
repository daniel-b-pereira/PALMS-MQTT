'''
Created on Jan , 2022
@author: Daniel
git:  
'''
import os
import datetime
import sys
import json
from time import sleep
from PyQt5 import QtCore, QtWidgets, QtSql,QtGui
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from MsgThreadQt import MsgThreadQt
from gui.MainWindow import Ui_MainWindow
from gui.PopupInfo import PopupInfo
from pprint import pprint
from datetime import datetime,date
import pytz

from ftplib import FTP, all_errors

from palms.Pnrd import Pnrd
from palms.FileCreator import FileCreator
from palms.utils.find_serial_port import serial_ports
from palms.utils.template import pnrd_init_template,pnrd_arduino_uno_template,pnrd_arduino_mega_template,ipnrd_init_template,ipnrd_arduino_uno_template
import serial

import time
from paho.mqtt import client as mqtt_client




class PalmsGui():
 
   
    def __init__(self):
        #Variables
        
        self.pnrd = Pnrd()
        self.pnrd_setup_is_ok = False

#        self.serial_port_verify, self.serial_port = serial_ports() 
#        self.pnrd_serial = dict()
        self.pnrd_ftp = dict()

        self.msg_thread = ''
        self.count_antenna = 0   
        self.qtd_antena = 0    
        self.reader_list = []
        self.transition_names = []
        self.array_matrix = []
        self.array_marking= []
        self.starting_token_vector = []
        self.palms_type = ''
        self.text_setup = ''
        app = QtWidgets.QApplication(sys.argv)
        
        
       
        
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow) 
       
#----------------------------------------------------------------------------------------------  
        # self.ui.serialConection_lineEdit.setText(self.serial_port)
        self.ui.actionopen_pnml.triggered.connect(self.open_pnml_file)
        self.ui.actionOpen_Setup_File_palms.triggered.connect(self.open_palms_file)
        self.ui.setupPalms_comboBox.currentIndexChanged.connect(self.setup_palms_type)

#        self.ui.confirmSerialConection_pushButton.clicked.connect(self.verify_palms_loader)
        self.ui.transferPNRDSetup_pushButton.clicked.connect(self.connect_mqtt)
        self.ui.transferPNRDSetup_pushButton.clicked.connect(self.publish_mqtt)
#        self.ui.transferPNRDSetup_pushButton.clicked.connect(self.connect_FTP_IP) ##########################################
        
 #       self.ui.getRuntimeInfo_pushButton.clicked.connect(self.updateRuntimeInfo)  
        self.ui.getRuntimeInfo_pushButton.clicked.connect(self. connect_mqtt)      
        self.ui.getRuntimeInfo_pushButton.clicked.connect(self. receive_mqtt) 
        
        
        self.ui.generateNewPNML_pushButton.clicked.connect(self. connect_mqtt)      
        self.ui.generateNewPNML_pushButton.clicked.connect(self. publish_inicial) 
        
      

#        self.ui.addSerial_pushButton.clicked.connect(self.append_reader)  
        self.ui.addIP_pushButton.clicked.connect(self.append_reader)

        self.ui.createSetup_pushButton.clicked.connect(self.create_palms_file)
        self.ui.nAntennas_spinBox.setMaximum(1)
        self.ui.nAntennas_spinBox.setMinimum(3)
        self.ui.setup_tabWidget.setCurrentIndex(0)

#        self.set_comboBox(self.serial_port,'COM')
        
#---------------------------------------------------------------------------------------------
       
        	
        self.MainWindow.show()
        sys.exit(app.exec_()) 
        

     
        
    def connect_mqtt(self) -> mqtt_client:
    	self.broker = 'mqtteste.cloud.shiftr.io'
    	self.port = 1883
    	self.topic = "PALMS-MQTT"
    	self.client_id = 'PALMS'
    	self.username = 'mqtteste'
    	self.password = 'testes'
    	def on_connect(client, userdata, flags, rc):
        	if rc == 0:
            		print("Conectado ao MQTT Broker!")
        	else:
            		print("Falha na conexão, return code %d\n", rc)

    	self.client = mqtt_client.Client(self.client_id)
    	self.client.username_pw_set(self.username, self.password)
    	self.client.on_connect = on_connect
    	self.client.connect(self.broker, self.port)
    	return self.client


    def setup_palms_type(self):
        self.palms_type = self.ui.setupPalms_comboBox.currentText()
        if self.palms_type=='iPNRD':
            self.ui.nAntennas_spinBox.setMaximum(1)
            self.ui.nAntennas_spinBox.setMinimum(1)
            self.ui.qtdTotalTansitions_label.setText(f'(Left: {1})')
        if self.palms_type=='PNRD':
            self.ui.nAntennas_spinBox.setMaximum(3)
            self.ui.nAntennas_spinBox.setMinimum(1)
            self.ui.qtdTotalTansitions_label.setText(f'(Left: {self.count_antenna})')
        return self.palms_type

    def create_palms_file(self):
        self.palms_type = self.ui.setupPalms_comboBox.currentText()
        self.get_transition_names(self.pnrd.len_transitions,self.pnrd.len_places)

        dict_palms = {
            "pnmlFile": self.pnrd.file,
            "type": self.palms_type,
            "qtdReaders":len(self.reader_list),
            "readerListConfig": self.reader_list,
            "transitionNames": self.transition_names
        }
        palms_file = FileCreator('palmsSetup',self.pnrd.file,'setup','palms')
        palms_file.set_text(json.dumps(dict_palms, indent=4, sort_keys=True))
        str_array_matrix = ','.join(map(str, self.array_matrix))
        str_starting_token_vector= ','.join(map(str, self.starting_token_vector))
        if self.palms_type=='PNRD':
            palms_init_template = FileCreator('palmsSetup',self.pnrd.file,'pnrd_initTag','pnrd')
            #palms_init_template = FileCreator('palmsSetup',self.pnrd.file,'pnrd_initTag','ino')
            palms_init_template.set_text(
                pnrd_init_template(
                    n_places=self.pnrd.len_places,
                    n_transitions = self.pnrd.len_transitions,
                    IncidenceMatrix = str_array_matrix,
                    StartingTokenVector = str_starting_token_vector
                )
            )
            id_antenna = 0
            reader_count = 0
            for e in self.reader_list:
                if e["readerName"]=='':
                    e["readerName"] = 'palms'

                readers_file = FileCreator(f'palmsSetup/{e["IP"]}',self.pnrd.file,'PNRDINFO','pnrd')
#                readers_file = FileCreator('palmsSetup',self.pnrd.file,f'pnrd_reader{reader_count}_{e["readerName"]}','pnrd')
                #readers_file = FileCreator('palmsSetup',self.pnrd.file,f'pnrd_reader{reader_count}_{e["readerName"]}','ino')
                if e["qtdAntenna"]==1:
                    readers_file.set_text(
                        pnrd_arduino_uno_template(
                            n_places=self.pnrd.len_places,
                            n_transitions=self.pnrd.len_transitions,
                            readerId=e["readerName"],
                            antenaId=id_antenna,
                            positon_fire= id_antenna
                        )
                    )
                    id_antenna +=1
                else:
                    antena_count = []
                    for i in range(e["qtdAntenna"]):
                        antena_count.append(id_antenna)
                        id_antenna +=1

                    readers_file.set_text(
                        pnrd_arduino_mega_template(
                            n_places=self.pnrd.len_places,
                            n_transitions=self.pnrd.len_transitions,
                            readerId=e["readerName"],
                            antenaId_list=antena_count,
                        )
                    )
                reader_count+= 1
        elif self.palms_type=='iPNRD':
            fire_vector_init = []
            for i in range(self.pnrd.len_transitions):
                if i==0:
                    fire_vector_init.append(1)
                else:
                    fire_vector_init.append(0)

            palms_init_template = FileCreator('palmsSetup',self.pnrd.file,'ipnrd_initTag','pnrd')
            #palms_init_template = FileCreator('palmsSetup',self.pnrd.file,'ipnrd_initTag','ino')
            palms_init_template.set_text(
                ipnrd_init_template(
                    n_places=self.pnrd.len_places,
                    n_transitions = self.pnrd.len_transitions,
                    fire_vector = ','.join(map(str, fire_vector_init)),
                )
            )
            for e in self.reader_list:
                if e["readerName"]=='':
                    e["readerName"] = 'palms'

                readers_file = FileCreator(f'palmsSetup/{e["IP"]}',self.pnrd.file,f'iPNRDINFO','pnrd')
#                readers_file = FileCreator('palmsSetup',self.pnrd.file,f'ipnrd_reader_{e["readerName"]}','pnrd')
                #readers_file = FileCreator('palmsSetup',self.pnrd.file,f'ipnrd_reader_{e["readerName"]}','ino')
                readers_file.set_text(
                    ipnrd_arduino_uno_template(
                        n_places=self.pnrd.len_places,
                        n_transitions = self.pnrd.len_transitions,
                        readerId = e["readerName"],
                        IncidenceMatrix = str_array_matrix,
                        StartingTokenVector = str_starting_token_vector
                    )
                )
        self.ui.popup_info = PopupInfo("Successfully created PALMS file!\nTo open file and use runtime mode press (Ctrl + F)")
        self.ui.popup_info.show()
        self.ui.createSetup_pushButton.setEnabled(False)
        
#        self.ui.addSerial_pushButton.setEnabled(False) 
        self.ui.addIP_pushButton.setEnabled(False) 


    def append_reader(self):
        palms_type = self.setup_palms_type()
        reader_name = self.ui.readerName_lineEdit.text()

#        serial_connection = self.ui.serialConection_comboBox.currentText()
#        self.serial_port.remove(serial_connection)
#        self.set_comboBox(self.serial_port,'COM')

        ip_connection = self.ui.IP_lineEdit.text() #########################################
# TODO: config that the same IP cannot be used twice        

        if palms_type =='PNRD':
            temp_antenna,count_antennas =self.set_antennas()
            print(count_antennas)
            if count_antennas <=0:

#                self.ui.addSerial_pushButton.setEnabled(False) 
                self.ui.addIP_pushButton.setEnabled(False) 

            qtd_antena = temp_antenna

#            self.reader_list.append({"readerName":reader_name,"qtdAntenna":qtd_antena,"serialPort":serial_connection})
            self.reader_list.append({"readerName":reader_name,"qtdAntenna":qtd_antena,"IP":ip_connection}) 

#            self.text_setup += f"Reader: {reader_name} Port: '{serial_connection}' Ant: {qtd_antena} units\n"
            self.text_setup += f"Reader: {reader_name} IP: '{ip_connection}' Ant: {qtd_antena} units\n" 
            
        else:
       
#            self.reader_list.append({"readerName":reader_name,"qtdAntenna":1,"serialPort":serial_connection})
            self.reader_list.append({"readerName":reader_name,"qtdAntenna":1,"IP":ip_connection}) 

#            self.text_setup += f"Reader: {reader_name} Port: '{serial_connection}' Ant: 1 unit\n"
            self.text_setup += f"Reader: {reader_name} IP: '{ip_connection}' Ant: 1 unit\n"

#            self.ui.addSerial_pushButton.setEnabled(False)
            self.ui.addIP_pushButton.setEnabled(False) 

        self.ui.setupInfo_label.setText(f'P: {self.pnrd.len_places} | T: {self.pnrd.len_transitions}\n{self.text_setup}')

    def get_transition_names(self,n_row,n_col):
        self.transition_names = []
        for i in range(n_row):
            matrix_transition_item = self.ui.incMatrix_tw.item(i,n_col)
            self.transition_names.append(matrix_transition_item.text())


    def set_antennas(self):
        if self.count_antenna>=self.ui.nAntennas_spinBox.value():
            self.count_antenna -=self.ui.nAntennas_spinBox.value() 
            qtd_reader_antenna = self.ui.nAntennas_spinBox.value() 
        self.ui.nAntennas_spinBox.setMaximum(3)    
        self.ui.qtdTotalTansitions_label.setText(f'(Left: {self.count_antenna})')
        if self.count_antenna>0 and self.count_antenna<=3:
            self.ui.nAntennas_spinBox.setMaximum(self.count_antenna)
        if self.count_antenna==0:
            self.ui.nAntennas_spinBox.setMaximum(0)
            self.ui.nAntennas_spinBox.setMinimum(0)
        return qtd_reader_antenna,self.count_antenna




#    def set_comboBox(self,lista,fonte):
#        if fonte =='setup':
#            pass
#            # self.ui.comboBox_tabela_origem.clear()
#            # self.ui.comboBox_tabela_origem.addItems(lista)
#        elif fonte =='COM':
#            self.ui.serialConection_comboBox.clear() ###########################################
#            self.ui.serialConection_comboBox.addItems(lista) ###################################


    def pnrd_setup(self,filename):
        _,ok = self.pnrd.set_pnml(filename)
        if ok:
            _,created = self.pnrd.create_net()
            if created:
                self.setup_matrix_view(self.pnrd.len_transitions,self.pnrd.len_places)
                self.setup_matrix_vector(self.pnrd.len_places,self.pnrd.len_transitions)
                self.setup_marking_vector(self.pnrd.len_places)
                self.pnrd_setup_is_ok = True
                self.count_antenna = self.pnrd.len_transitions
                self.ui.nAntennas_spinBox.setRange(1, self.pnrd.len_transitions)
                self.ui.qtdTotalTansitions_label.setText(f'(Left: {self.count_antenna})')
                self.setup_palms_type()


    def pnrd_palms_runtime(self,filename):
        with open(filename, 'r') as palms_file:
            palms = json.load(palms_file)
            _,ok = self.pnrd.set_pnml(palms["pnmlFile"])
            if ok:
                _,created = self.pnrd.create_net()
                if created:
                    self.pnrd.transition_names = palms["transitionNames"]
                    self.setup_matrix_view(self.pnrd.len_transitions,self.pnrd.len_places,"palms")
                    self.setup_matrix_vector(self.pnrd.len_places,self.pnrd.len_transitions)
                    self.setup_marking_vector(self.pnrd.len_places)
                    self.pnrd_setup_is_ok = True
                    self.setup_palms_type()
                    self.ui.palmsType_label.setText(f'Type: {palms["type"]}')
                    self.ui.qtdReader_label.setText(f'Qtd Readers: {palms["qtdReaders"]}')
                    readers_list = ''
                    for i in palms["readerListConfig"]:

#                        readers_list += f'Reader: {i["readerName"]} \n  Qtd Ant:{i["qtdAntenna"]} \n  Port: {i["serialPort"]}\n\n' 
                        readers_list += f'Reader: {i["readerName"]} \n  Qtd Ant:{i["qtdAntenna"]} \n  IP: {i["IP"]}\n\n' 

                    self.ui.readerList_label.setText(readers_list)
                    self.reader_list = palms["readerListConfig"]


    def setup_matrix_view(self,n_row,n_col,_type="pnml"):
        self.ui.incMatrix_tw.setRowCount(n_row)
        self.ui.incMatrix_tw.setColumnCount(n_col+1)
        self.ui.incMatrix2_tw.setRowCount(n_row)
        self.ui.incMatrix2_tw.setColumnCount(n_col+1)
        count_row = 0
        horizontalHeader = []
        verticalHeader = []
        for row in self.pnrd.incidence_matrix:
            count_col = 0
            for i in row:
                    if len(horizontalHeader) < n_col:
                        horizontalHeader.append(f" P{count_col} ")
                    if count_col==(n_col -1):
                        if _type=="palms":
                            self.ui.incMatrix_tw.setItem( count_row,count_col+1, QTableWidgetItem(f"{self.pnrd.transition_names[count_row]}"))
                            self.ui.incMatrix2_tw.setItem( count_row,count_col+1, QTableWidgetItem(f"{self.pnrd.transition_names[count_row]}"))
                        else:
                            self.ui.incMatrix_tw.setItem( count_row,count_col+1, QTableWidgetItem(f"transition {count_row}"))
                            self.ui.incMatrix2_tw.setItem( count_row,count_col+1, QTableWidgetItem(f"transition {count_row}"))
                        

                    self.ui.incMatrix_tw.setItem( count_row,count_col, QTableWidgetItem(f"{i}"))
                    self.ui.incMatrix2_tw.setItem( count_row,count_col, QTableWidgetItem(f"{i}"))
                    count_col+=1                 
            verticalHeader.append(f" T{count_row} ")
            count_row+=1
        horizontalHeader.append(f"  ")
        self.ui.incMatrix_tw.setHorizontalHeaderLabels(horizontalHeader)
        self.ui.incMatrix2_tw.setHorizontalHeaderLabels(horizontalHeader)
        self.ui.incMatrix_tw.setVerticalHeaderLabels(verticalHeader) 
        self.ui.incMatrix2_tw.setVerticalHeaderLabels(verticalHeader)     
        self.ui.places_label.setText(f'Places: {self.pnrd.len_places}')
        self.ui.transitions_label.setText(f'Transitions: {self.pnrd.len_transitions}')


    def setup_matrix_vector(self,n_row,n_col):
        self.array_matrix = []
        for row in self.pnrd.incidence_matrix_t:
            for i in row:
                    self.array_matrix.append(i)
        self.ui.matrix_array.setText(f"{self.array_matrix}")


    def setup_marking_vector(self,n_row):
        count_row = 0

        self.ui.markingVector_tw.setRowCount(n_row)
        self.ui.markingVector_tw.setColumnCount(1)
        self.ui.markingVector2_tw.setRowCount(n_row)
        self.ui.markingVector2_tw.setColumnCount(1)
        verticalHeader = []
        self.array_marking= []
        self.starting_token_vector = []

        for i in self.pnrd.marking_vector:
            if count_row==0:
                self.starting_token_vector.append(1)
            else:
                self.starting_token_vector.append(0)

            verticalHeader.append(f" P{count_row} ")
            self.ui.markingVector_tw.setItem(count_row,0, QTableWidgetItem(f"{i}"))
            self.ui.markingVector2_tw.setItem(count_row,0, QTableWidgetItem(f"{i}"))

            self.array_marking.append(i)
            count_row+=1

        self.ui.marking_array.setText(f"{self.array_marking}")    
        self.ui.markingVector_tw.setHorizontalHeaderLabels([""])    
        self.ui.markingVector_tw.setVerticalHeaderLabels(verticalHeader)
        self.ui.markingVector2_tw.setHorizontalHeaderLabels([""])    
        self.ui.markingVector2_tw.setVerticalHeaderLabels(verticalHeader)  


    def open_pnml_file(self):
        self.ui.createSetup_pushButton.setEnabled(True)

#        self.ui.addSerial_pushButton.setEnabled(True) 
        self.ui.addIP_pushButton.setEnabled(True)

        filename, _ = QFileDialog.getOpenFileName(filter ="pnml(*.pnml)")
        self.ui.setup_tabWidget.setCurrentIndex(0)
        self.ui.setup_tabWidget.setTabEnabled(0, True)
        self.ui.setup_tabWidget.setTabEnabled(1, False)

#        _ , self.serial_port = serial_ports()  ##########################################

        if filename !='':
            self.pnrd_setup(filename)

    def open_palms_file(self):
        filename, _ = QFileDialog.getOpenFileName(filter ="palms(*.palms)")
        self.ui.setup_tabWidget.setTabEnabled(1, True)
        self.ui.setup_tabWidget.setTabEnabled(0, False)
        self.ui.setup_tabWidget.setCurrentIndex(1)
        if filename !='':
            self.pnrd_palms_runtime(filename) 
    #----------------------------------------------------------

    def fire_vector(self,vector):
        return self.pnrd.update_pnml(fire_vector=fire_vector)

    def token_vector(self,vector):

        return self.pnrd.update_pnml(token=vector, _type='token')
    

#    def verify_palms_loader(self):
#        if self.pnrd_setup_is_ok:
#            msg =''
#            try:     
#                count = 0  
#                for i in self.reader_list:
#                    self.serial_port = i["serialPort"] ##########################################
#                    ard = serial.Serial(self.serial_port,9600,timeout=5) #####################################
#                    msg = self.serial_port ##################################################
#                    ard.flush()
#                    ard.close()
#                    sleep(0.3)
#                    count+=1
#                if count==len(self.reader_list):
#                    self.connect_serial_port() ###########################################################
#                else:
#                    self.ui.info_label.setText(f"Problem with your Serial Connection on port {msg}") ##############################
#            except OSError as e:
#                self.ui.info_label.setText(f"A Error occurs with your Serial Connection on port {msg}\n{e}") ###########################
#        else:
#            self.ui.info_label.setStyleSheet('QLabel#info_label {color: red}')
#            self.ui.info_label.setText("You need to load PALMS file first")

#    def connect_serial_port(self):
#        self.serial_ports = list()  ###########################################################
#        for i in self.reader_list: 
#            serial_port = i["serialPort"] ##########################################################
#            self.serial_ports.append(serial_port)  #############################################################
#            
#        self.msg_thread = MsgThreadQt(self.serial_ports, parent=None)  ####################################################3
#        self.msg_thread.start()
#        self.msg_thread.msg_status.connect(self.set_msg_status)
#        self.ui.confirmSerialConection_pushButton.setEnabled(False) ##################################################
#        self.ui.info_label.setStyleSheet('QLabel#info_label {color: green}')
#        self.ui.info_label.setText("Successfully connected")
        
    def connect_FTP_IP(self):
        self.FTP_IPs = list()
        for i in self.reader_list:
            ip_connection = i["IP"]
            print(i["IP"])
            self.FTP_IPs.append(ip_connection)

            try:
                with FTP(host=i["IP"], user='myname', passwd='123') as ftp:
                    print(ftp.getwelcome()) 
                    #self.ui.runtimeTerminal_label.setText(ftp.getwelcome())
                    #with open('PNRDINFO.pnrd', 'rb') as text_file:
                    with open(f'palmsSetup/{i["IP"]}/PNRDINFO.pnrd', 'rb') as text_file:
                        ftp.storlines('STOR PNRDINFO.pnrd', text_file)
                        #ftp.storlines(f'STOR palmsSetup/{i["IP"]}/PNRDINFO.pnrd', text_file)

                    self.ui.runtimeTerminal_label.setStyleSheet('QLabel#runtimeTerminal_label {color: green}')
                    self.ui.runtimeTerminal_label.setText('PNRD info sent to Arduinos Successfully.')
                    ftp.close()
            except:
                self.ui.runtimeTerminal_label.setStyleSheet('QLabel#runtimeTerminal_label {color: red}')
               # self.ui.runtimeTerminal_label.setText('tagId: DF Transition: t3 Marking: (01-11-110)   EXCEPTION')
               # print('tagId: DF Transition: t0 Marking: (0101000)   Ok')
                print("Error conecting to "+i["IP"])

    
    
    def publish_mqtt(self,client):
    	self.FTP_IPs = list()
    	for i in self.reader_list:
    		ip_connection = i["IP"]
    		print(i["IP"])
    		self.FTP_IPs.append(ip_connection)
    	while True:
    		time.sleep(1)
    		with open(f'palmsSetup/{i["IP"]}/PNRDINFO.pnrd', 'r') as mqtt:
    			msg = mqtt.read()
    			result = self.client.publish(self.topic, "Atualizar")
    			result = self.client.publish(self.topic, msg)
    			mqtt.close()
    			result = self.client.publish(self.topic, "End")
    		status = result[0]
    		if status == 0:
    			print(f"Sucess to send message to topic {self.topic}")
    			msg = 'break'
    		else:
    			print(f"Failed to send message to topic {self.topic}")
    		if msg == 'break':
    			break
    		
    def publish_inicial(self,client):
    	self.FTP_IPs = list()
    	for i in self.reader_list:
    		ip_connection = i["IP"]
    		print(i["IP"])
    		self.FTP_IPs.append(ip_connection)
    	while True:
    		time.sleep(1)
    		with open(f'palmsSetup/pnrd_initTag.pnrd', 'r') as inicial:
    			init = inicial.read()
    			result = self.client.publish(self.topic, "Iniciar")
    			result = self.client.publish(self.topic, init)
    			inicial.close()
    			result = self.client.publish(self.topic, "Fim")
    		status = result[0]
    		if status == 0:
    			print(f"Sucess to send message to topic {self.topic}")
    			msg = 'break'
    		else:
    			print(f"Failed to send message to topic {self.topic}")
    		if msg == 'break':
    			break
		
    def set_msg_status(self, msg_status, msg):
    

        try:
#            self.pnrd_serial['id'] = msg["id"] 
#            self.pnrd_serial['reader'] = msg["readerId"] 
#            self.pnrd_serial['error'] = msg["pnrd"] 
#            self.pnrd_serial['antenna'] = msg["ant"] 
#            self.pnrd_serial['fire'] = int(msg['fire']) 

            self.pnrd_ftp['id'] = msg["id"] 
            self.pnrd_ftp['reader'] = msg["readerId"] 
            self.pnrd_ftp['error'] = msg["pnrd"] 
            self.pnrd_ftp['antenna'] = msg["ant"] 
            self.pnrd_ftp['fire'] = int(msg['fire'])
        # ----------------------------------------------------    
            today = date.today()          
            now_BR = datetime.now(pytz.timezone('America/Sao_Paulo'))

        #---------------------------------------------------
            msg["date"] =  today.strftime("%d-%m-%Y")
            msg["time"] = now_BR.strftime('%H-%M-%S')
            runtime_file = FileCreator('palmsSetup',self.pnrd.file,'runtime','json')
            runtime_file.set_text_increment(json.dumps(msg, indent=4, sort_keys=True))

#            self.ui.id_label.setText("TagId: "+str( self.pnrd_serial['id'])) 
#            self.ui.reader_label.setText("Reader: "+str( self.pnrd_serial['reader']))
#            self.ui.exception_label.setText("PNRD: "+str( self.pnrd_serial['error']))

            self.ui.id_label.setText("TagId: "+str( self.pnrd_ftp['id']))
            self.ui.reader_label.setText("Reader: "+str( self.pnrd_ftp['reader']))
            self.ui.exception_label.setText("PNRD: "+str( self.pnrd_ftp['error']))

            self.ui.info_label.setStyleSheet('QLabel#info_label {color: green}')
            self.ui.info_label.setText(msg_status)  
            self.update_pnrd(msg)
            for i in range(self.pnrd.len_transitions):

#                if i != self.pnrd_serial['fire']: 
                if i != self.pnrd_ftp['fire']: 

                    self.ui.incMatrix2_tw.item(i,self.pnrd.len_places).setBackground(QtGui.QColor(255, 255, 255))
                else:
                    self.ui.incMatrix2_tw.item(i,self.pnrd.len_places).setBackground(QtGui.QColor(0, 255, 0))


        except:
            if  msg_status !=None: 
                self.ui.info_label.setStyleSheet('QLabel#info_label {color: red}')
                self.ui.info_label.setText(msg_status) 

#                self.ui.confirmSerialConection_pushButton.setEnabled(True)
                self.ui.transferPNRDSetup_pushButton.setEnabled(True)

            else:
                self.ui.info_label.setStyleSheet('QLabel#info_label {color: red}')
                self.ui.info_label.setText("Erro ao carregar dados") 

        

    def update_pnrd(self,pnrd):
        token = pnrd['token']
        msg,is_ok = self.token_vector(token)
        if not is_ok:
            self.ui.info_label.setText(str(msg))
        self.setup_marking_vector(self.pnrd.len_places)
        self.pnrd_setup_is_ok = True
      
      
    def Runtimemqtt(self, client:mqtt_client):
    	self.FTP_IPs = list()
    	for i in self.reader_list:
    		ip_connection = i["IP"]
    		print(i["IP"])
    	def on_message(client, userdata, msg):
    		print(f"Recebido `{msg.payload.decode()}` de `{msg.topic}` topic")
    		msg_flag=msg.payload.decode()
    		local_file = open (f'palmsSetup/{i["IP"]}/PNRDINFOhey.pnrd', 'a')
    		local_file.write (msg_flag)
    		local_file.write ('\n')
    		
    	self.client.subscribe(self.topic)
    	self.client.on_message = on_message
    	
    def receive_mqtt(self): 
    	self.FTP_IPs = list()
    	result = self.client.publish(self.topic, "Info")
    	for i in self.reader_list:
    		ip_connection = i["IP"]
    	with open(f'palmsSetup/{i["IP"]}/PNRDINFOhey.pnrd', 'w') as local_file:
    		local_file.close()
    	self.Runtimemqtt( self.client)
    	self.client.loop_forever()
     	
    
        

    def updateRuntimeInfo(self):
        self.FTP_IPs = list()
        for i in self.reader_list:
            ip_connection = i["IP"]
            print(i["IP"])
            self.FTP_IPs.append(ip_connection)

            try:
                with FTP(host=i["IP"], user='myname', passwd='123') as ftp:
                    print(ftp.getwelcome())
                    #self.ui.runtimeTerminal_label.setText(ftp.getwelcome())
                    #with open('PNRDINFO.pnrd', 'rb') as text_file:
                    with open(f'palmsSetup/{i["IP"]}/PNRDINFOhey.pnrd', 'w') as local_file:
                        #response = ftp.retrlines(f'RETR palmsSetup/{i["IP"]}/PNRDINFOhey.pnrd', local_file.write)
                        res = ftp.retrlines('RETR PNRDINFO.pnrd', local_file.write)

                        if res.startswith('226'):
                            print('Transfer complete')
                            self.ui.runtimeTerminal_label.setStyleSheet('QLabel#runtimeTerminal_label {color: green}')
                            self.ui.runtimeTerminal_label.setText('Transfer complete')
 
                        else:
                            print('Error transferring. Local file may be incomplete or corrupt.')
                            self.ui.runtimeTerminal_label.setStyleSheet('QLabel#runtimeTerminal_label {color: red}')
                            self.ui.runtimeTerminal_label.setText('Error transferring. Local file may be incomplete or corrupt.')

                    ftp.close()
            except:
                self.ui.runtimeTerminal_label.setStyleSheet('QLabel#runtimeTerminal_label {color: red}')
               # self.ui.runtimeTerminal_label.setText('tagId: DF Transition: t3 Marking: (01-11-110)   EXCEPTION')
               # print('tagId: DF Transition: t0 Marking: (0101000)   Ok')
                print("Error conecting to "+i["IP"])

#       try:
#            self.msg_thread.stop()
#            self.ui.info_label.setText("Connection Closed")
#
##            self.ui.confirmSerialConection_pushButton.setEnabled(True)
#            self.ui.transferPRNDSetup_pushButton.setEnabled(True)
#
#            self.ui.getRuntimeInfo_pushButton.setEnabled(False)
#        except:
#            self.ui.info_label.setStyleSheet('QLabel#info_label {color: red}')
#
##            self.ui.info_label.setText("Close Your Serial Connection before Stop") 
#
##            self.ui.confirmSerialConection_pushButton.setEnabled(False)
#            self.ui.transferPNRDSetup_pushButton.setEnabled(False)
#
#            self.ui.getRuntimeInfo_pushButton.setEnabled(False)
