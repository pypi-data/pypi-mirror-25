import  zipfile,os,tarfile,sys
class Extract:
    def __init__(self,path,remove_files_zip=True):
        self.path=path
        self.remove_source_zip=remove_files_zip
        print('Analysing Directory and extracting')
        self.count = 0
        self.extract(self.path)
        print('Extracted total '+str(self.count)+' files')

    def extract(self,path):
        for root, dirs, file in os.walk(path):
            for file_ in file:
                temp = os.path.join(root, file_)
                try:
                    if temp.endswith('zip'):
                        z = zipfile.ZipFile(temp)
                        z.extractall(temp.split('.')[0])
                        z.close()
                        self.count += 1
                    elif temp.endswith('tar.gz'):
                        z=tarfile.open(temp,'r:gz')
                        z.extractall(temp.split('.')[0])
                        self.count += 1
                        z.close()
                    elif temp.endswith('tar') :
                        z=tarfile.open(temp,'r:')
                        z.extractall(temp.split('.')[0])
                        self.count += 1
                        z.close()
                    self.extract(temp.split('.')[0])
                    if self.remove_source_zip:
                        os.remove(temp)
                except Exception as e:
                    print(temp.split('/')[-1]+' is not a supported file type')

