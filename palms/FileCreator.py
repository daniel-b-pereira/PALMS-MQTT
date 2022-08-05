import os


class FileCreator:

    def __init__(self,dir_name,homedir,file_name,extension):

        self.location = os.path.dirname(os.path.abspath(homedir))+f'/{dir_name}'
        self.file_name = file_name
        self.extension = extension
        self.verify_dir(self.location)

    def set_text(self,txt):
        f= open(f'{self.location}/{self.file_name}.{self.extension}',"w+")
        f.write(txt)
        f.close() 


    def set_text_increment(self,txt):
        if self.verify_if_file(f'{self.location}/{self.file_name}.{self.extension}'):
            f=open(f'{self.location}/{self.file_name}.{self.extension}', "a")
        else:
            f= open(f'{self.location}/{self.file_name}.{self.extension}',"w+")
        f.write(txt)
        f.close() 

    def create_dir(self,dirname):
        if  os.path.isdir(dirname):
            pass
        else:
            try:
                os.mkdir(dirname)
            except OSError:
                print ("A criação do Diretório  %s Falhou" % dirname)
            else:
                print ("Diretório  %s criado com sucesso" % dirname)

    def verify_dir(self, dirname):
        self.create_dir(dirname)


    def verify_if_file(self,file_name):
        if  os.path.isfile(file_name) :
            return True
        else :
            return False