#defines the scanhandler class for importing scansion of a marked-up document
import csv


class scanhandler():
    # import csv
    import tkinter as tk
    from tkinter import filedialog
    
    _scanfile=None #the file containing the scansion
    _reader=None #this will become the tab-separated-value scanfile reader
    scantype=""

    def __init__(self,filename:str=""):
        root = self.tk.Tk()
        root.withdraw()

        if filename=="":
            print('get scan file')
            filename=self.filedialog.askopenfilename()
        
        self._scanfile=open(filename, 'r', encoding="utf8")
        self._reader=csv.reader(self._scanfile, delimiter="\t")
        self.scantype=next(self._reader)[2] #get the scan type heading the scan column
        print(self.scantype)
        
    #public method to return the next scan record in the file
    #it will be a list containing: [line #, "on"/"off", contour, note]
    def nextscan(self):
        try:
            record=next(self._reader)
            return record
        except Exception as e: 
            print('end of file')
            return e

