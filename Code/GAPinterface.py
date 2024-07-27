#interface driver
class ix:
    import tkinter as tk
    from tkinter import filedialog
    from lxml import etree as et
    from GAPdocumenthelper import docuhelper
    from GAPdisplay import displaydriver 

    def __init__(self):
        root = self.tk.Tk()
        root.withdraw()

    def _getinfilename(self,type:str=""):
        print("get input file")
        file_path = self.filedialog.askopenfilename()
        return file_path

    def _parsein(self, fin:str=""):
        if fin=="":
            fin=self._getinfilename("anno")
        if len(fin)>0:
            try:
                parser = self.et.XMLParser(load_dtd=True, no_network=False, resolve_entities=False)
                doc=self.et.parse(fin,parser)
                print("In: ", '/' + fin)
                return doc
            except Exception as e: return e
    
    def _getoutfilename(self,type:str=""):
        print("get output file")
        file_path = self.filedialog.askopenfilename()
        return file_path

    def _savexmlfile(self, doc, fout, type:str=""):
        if fout=="":
            fout = self._getoutfilename("")
                        
        if len(fout)>0:
            f = open(fout, 'w')
            xml = self.et.tostring(doc, encoding="unicode")
            #this will typically result in the Menota entity list being expanded at the beginning of the xml; replace with reference
            xml=xml[xml.find('<TEI'):len(xml)]
            f.writelines('<?xml version="1.0" encoding="UTF-8"?>\n\n')
            f.writelines('<!DOCTYPE TEI[\n')
            f.writelines('<!ENTITY % menotaEntities SYSTEM "http://www.menota.org/menota-entities.txt"> %menotaEntities;\n')
            f.writelines(']>\n\n')
            f.write(xml)
            f.close()
            print("Out: ", '/' + fout)
            return 0
        return -1

    def _savehtmlfile(self, html, fout):
        if fout=="":
            fout = self._getoutfilename("htm")
        if len(fout)>0:
            f = open(fout, 'w')
            f.write(html)
            f.close
            print("Out: ", '/' + fout)
            return 0
        return -1
   
    #     
    #     This is the one to call...
    def process(self, funcname, fin:str="", fout:str=""):
        """Pass in a public GAPdocumenthelper.docuhelper method as a string in func.
        If either fin or fout filenames are missing, this object will ask for them. 
        The function will be called with fin loaded into self.dh"""
        docin=self._parsein(fin)
        if docin is not None:
            dh=self.docuhelper(docin)
            try:
                docout=dh.process(funcname)
            except Exception as e: return e
            #now save the result to another file
            self._savexmlfile(docout, fout)
            return 0
        return -1

    #     ...unless you want to generate a display (html) document, then call this one
    def display(self, fin:str="", fout:str="", options:dict={}):
        """Transform an analyzed GAP document in HTML. 
           If either fin or fout filenames are missing, this object will ask for them.
           if options{} are passed in, they will be given to the display driver.
           """
        docin=self._parsein(fin)
        if docin is not None:
            dh=self.docuhelper(docin)
            try:
                dd=self.displaydriver(dh, options)
                html=dd.generatehtml()
            except Exception as e: return e
            #now save the result to another file
            self._savehtmlfile(html, fout)
            return 0
        return -1


    #if anything needs to get a file of any kind, call this; purpose and filetype will limit the possibilities
    def getfilename(self, purpose:str="", filetype=""):
            try:
                filename=self.filedialog.askopenfilename()
                return filename
            except Exception as e: return e
