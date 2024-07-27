#the document helper contains document transformers for syllabifying, lineating, etc.
#unlike wordhelper, it understands the XML structure of the document
class docuhelper:
    from lxml import etree as et
    from GAPwordhelper import wordhelper as wh
    from GAPscanhandler import scanhandler as sh

    NONE=0
    ANNOTATED=1
    LINEATED=2
    SYLLABIFIED=3
    ANALYZED=4

    #instance variables
    _et=et
    _sh = None
    _doc = None #these three should become public properties
    _root = None
    _wh = None
    lang=""
    syllabification=""
    markuplevel=NONE

    #hold the default TEI namespace used to qualify element searches, etc.
    _TEIns={'d': 'http://www.tei-c.org/ns/1.0'}

    def __init__(self, doc):
        self._doc=doc #the parsed xml document tree to work on
        self._root=doc.getroot()
        if self._root == None: return None

        #dig out the other instance variable values 
        lang=""
        langEl=self._root.find(".//d:language", self._TEIns)
        if 'ident' in langEl.attrib: lang=str(langEl.get('ident'))

        codamax=False
        syll_method=""
        if 'syllabification' in langEl.attrib: syll_method=str(langEl.get('syllabification'))
        else: syll_method=""
        if syll_method=="coda" or syll_method=="codamax": codamax=True
        self.lang=lang
        self.syllabification=syll_method

        ml=""
        markupEl=self._root.find(".//d:markupLevel", self._TEIns)
        ml=markupEl.text
        if ml=="annotated": self.markuplevel=self.ANNOTATED
        elif ml=="lineated": self.markuplevel=self.LINEATED
        elif ml=="syllabified": self.markuplevel=self.SYLLABIFIED
        elif ml=="analyzed": self.markuplevel=self.ANALYZED

        #instantiate a worderhelper object
        self._wh=self.wh(lang,codamax)

    #rather than calling the transformer methods below directly, 
    # they can be called indirectly through this method
    def process(self, funcname:str):
        #do the thing
        self.__getattribute__(funcname)()
        return self._doc

    #
    # public methods for transforming the document self._doc
    #
    def syllabify(self):

        #get all the word elements
        words = self._root.findall(".//d:w", self._TEIns)
        syllables=[]
        syllables.clear
        #this is where we will do the work of restructuring the xml and attaching the syllables
        def buildWord(word, wordvars,parent=None):
            #first assign the word an ID and increment the counter
            word.set("id",str(wordvars['id']))
            wordvars['id'] +=1

            #now get the text of the word to break into syllables
            try:
                text_exists=(len(word.text)!=0)
            except:
                text_exists=False
            if text_exists: 
                text = word.text
                syllables = self._wh.break_word(text)
                if syllables != None:
                    syllCount=len(syllables)
                    word.set("Σ",str(syllCount)) #store the syllable count on the <w> element to make later calculations
                    i=syllCount-1
                    for syl in syllables:
                        #create a new, unattached syllable node
                        # sylEl=doc.createElement("s")
                        sylEl=self.et.Element("s")

                        #add the syllable text
                        sylEl.text=syllables[i][0]
                        #put the mora count in an attribute
                        sylEl.set("m", str(syllables[i][1]))
                        sylEl.set("wt", str(syllables[i][2]))

                        #now attach the syllable element to the parent word element 
                        if parent==None:
                            word.addnext(sylEl)
                            word.tail=None
                        else:
                            parent.addnext(sylEl)
                            word.tail=None
                        i -=1 
                    #the word text is now in the <s> elements; get rid of the text node in <w>
                    word.text = None
            return 0

        #we will assign an ID to each word as part of the syllabification process
        wordvars={"id":0}
        for word in words: 
            if len(word)>0: #if there are child words
                for subword in reversed(word): 
                    buildWord(subword, wordvars, word)
                    word.addnext(subword) #promote it to a sibling
            buildWord(word, wordvars)
                
        return self._doc

    #take a prepared document and find the verse and line boundaries.
    def lineate(self):
        return self._doc

    #add alliterative symbols to all <w> elements
    def alliterate(self):
        #first let's get all the words
        words = self._root.findall(".//d:w", self._TEIns)
        allit=""
        for word in words:
            #if there are other words beneath this one, skip it
            if len(word)>0: continue
            #get the text of the word
            text=word.text
            #get its alliterative symbol
            if not text is None:
                allit=self._wh.allitSymbol(text,True)
            if len(allit)>0:
                #now set the alliterative symbol attribute (@A) of the <w>
                word.set('A', allit)
        return self._doc
        
    #set some atrributes on line verse groups (<vg> type="line")
    def decoratelines(self):
        groups=self._root.findall(".//d:vg", self._TEIns)
        if len(groups)==0: return None
        for group in groups:
            group.set('type', "line")
            group.set('cid',"")
            group.set('A',"")
            idx=0
            verses=group.findall(".//d:v", self._TEIns)
            for verse in verses:
                #not all child elements are <v>s, some are <lb>, <cb>, etc.
                # if child.tag=="{" + self._TEIns['d'] + "}v":
                if idx==0: 
                    verse.set('role', "on")
                    idx +=1
                    continue
                if idx==1: 
                    verse.set('role', "off")

        return self._doc

    #
    #public methods for reverting a document to a lower level of annotation
    #
    #take an analyzed document back to the syllabified state
    def de_analyze(self):
        #first get rid of any position or feet tags
        positions=self._root.findall(".//d:z", self._TEIns)
        for pos in positions: pos.getparent().remove(pos)

        feet=self._root.findall(".//d:f", self._TEIns)
        for foot in feet: foot.getparent().remove(foot)
        
        #now get rid of resolution and suspension correlators
        words=self._root.findall(".//d:w", self._TEIns)
        for word in words:
            if "res" in word.attrib: word.attrib.pop('res')
            if "sus" in word.attrib: word.attrib.pop('sus')

        #finally rid the verses of their annotations
        verses=self._root.findall(".//d:v", self._TEIns)
        for verse in verses:
            if "type" in verse.attrib: verse.attrib.pop('type')
            if "contour" in verse.attrib: verse.attrib.pop('contour')
            if "restr" in verse.attrib: verse.attrib.pop('restr')
        
        return self._doc

    #take an syllabified soducment back to the lineated state
    def de_syllabify(self):
        #for each word, gather the syllable text from its sibling <s> elements
        words=self._root.findall(".//d:w", self._TEIns)
        for word in words:
            wordtext=""
            node=word.getnext()
            wordstr="{" + self._TEIns['d'] + "}w"
            syllstr="{" + self._TEIns['d'] + "}s"
            #loop through the following siblings of the word milestone <w/> until
            #run out of siblings or hit the next word. Not all of the siblings will be <s>
            while (node is not None) and (node.tag!=wordstr):
                if node.tag==syllstr: #we are in a syllable
                    wordtext += (node.text or '')
                node=node.getnext()
            word.text=wordtext
            #now remove the syllable count and id added during syllabification
            if "Σ" in word.attrib: word.attrib.pop('Σ')
            if "id" in word.attrib: word.attrib.pop('id')

        #kill all syllables
        syllables=self._root.findall(".//d:s", self._TEIns)
        for syll in syllables: syll.getparent().remove(syll)
        return self._doc

    #take a lineated document back to the annotated state.
    #in a lineated doc, words are in verses and verses are 
    #in groups. This moves them up the hierarchy. Other things are
    #also in the verses and groups, so these need to move as well.
    def de_lineate(self):
        body=self._root.find(".//d:body", self._TEIns)
        if body is None: return None

        groups=self._root.findall(".//d:vg", self._TEIns)
        for group in groups:
            cursor=1
            
            for node in group.getchildren():
                #some of the children aren't verses
                if len(node)==0:
                    body.insert(body.index(group)+cursor, node)
                    cursor+=1
                #some are
                else:
                    for subnode in node.getchildren():
                        body.insert(body.index(group)+cursor, subnode)
                        cursor+=1
                        #now get rid of these empty elements
                    group.remove(node)
            body.remove(group)
        return self._doc

    def numberlines(self,start:int=1):
        n=start
        lines=self._root.findall(".//d:vg", self._TEIns)
        for line in lines:
            line.set('cid',str(n))
            n+=1
        return self._doc

    def markallit(self):
        groups=self._root.findall(".//d:vg", self._TEIns)
        for group in groups:
            if 'A' not in group.attrib:
                group.set('A',"")
        return self._doc

    #
    #
    #take a scansion file and import it into an analyzed document
    def importscan(self):
        from GAPscanhandler import scanhandler as sh

        global syllables
        #initialize the scanhelper -- this will ask the user for the file
        self._sh=sh()
        sh=self._sh
        record = sh.nextscan()
        while isinstance(record, list): #loop until the iterator through the scan file is done
            #unpack the current verse-scan record
            print('[[[[',record,']]]]') ###debug
            lineid=record[0]
            verse=record[1]
            scanstr=record[2]
            type=record[3]
            restr=record[4]
        
            #dictionary to hold attributes to set on a verse or whatever
            atts={'type': type, 'restr':restr, 'contour':scanstr}
            #find the verse line corresponding to lineid
            lineEl=None
            nodes=self._root.findall(".//d:vg", self._TEIns)
            for node in nodes:
                if 'cid' in node.attrib:
                    if node.get('cid')==lineid:
                        lineEl=node
                        break
            if lineEl != None: 
                # print('we have a line') ###debug
                # we have the verse line. now let's get the right verse, on or off
                verseEl=None
                nodes=lineEl.findall("./d:v", self._TEIns)
                for node in nodes:
                    if 'role' in node.attrib:
                        if node.get('role')==verse:
                            verseEl=node
                            break
                if verseEl != None:
                    # print('we have a verse') ###debug
                    #before we get to the syllables, remove any previous analysis
                    znf=verseEl.findall(".//d:z", self._TEIns) + verseEl.findall(".//d:f", self._TEIns)
                    for zf in znf: zf.getparent().remove(zf)
                    #we have the verse. get the <s> (syllables) inside it
                    syllables=verseEl.findall("./d:s", self._TEIns)
                    if syllables != None:
                        # print('we have', str(len(syllables)), 'syllables') ###debug
                        #we have the target list of syllables; now prepare
                        #the scansion data from the 'scanstr'
                        scanstructions=self._preparescansion(scanstr,atts)

                        # print(scanstructions) ###debug

                        #make it happen
                        self._doscan(syllables, scanstructions)
                    
            record=sh.nextscan()

    #here we are going to turn a scanstr (e.g. xxxpx) into a list of instructions for decorating the verse
    def _preparescansion(self,scanstr:str, atts:list):
        scanstructions=[] #start with nothing
        #create an attribute instruction for each attribute
        for a in atts:
            value=atts[a]
            scanstructions.append(['a', [a,value]])

        #here we branch based on the scan type
        scantype=self._sh.scantype
        # print(scantype, scanstr)
        #now create the scan-type-specific instructions and append them
        if scantype=="suzuki":
            scanstructions+=self._prepsuzuki(scanstr)
        elif scantype=="sievers":
           scanstructions+=self._prepsievers(scanstr)
        elif scantype=="russom":
            scanstructions+=self._preprussom(scanstr)
        return scanstructions

    ##notation specific methods for preparing the scan instructions
    def _prepsuzuki(self, scanstr:str):
        scansion=list(scanstr)
        scanstructions=[]
        # print(syllables[0].getparent().getparent().get('cid')) ##debug

        #safe advance through the scansion list
        def advance(lst):
            if len(lst)> 1: lst=lst[1:]
            else: lst=[]
            return lst

        #if there's a mismatch between the scan and the number of syllables in
        #this verse, then log the error and bail. Attributes will still be
        #applied
        # print(len(scansion), len(syllables)) ###debug
        if len(scansion) != len(syllables): 
            verse=syllables[0].getparent() #they all have the same parent verse
            line=verse.getparent()
            print(line.get('cid'), verse.get('role'), "Syllable count / scan mismatch")
            return scanstructions
        
        #see whether there's an initial dip, if so how long
        initdip=0
        while len(scansion) > 0 and scansion[0] in ['x','X']:
            scansion=advance(scansion)
            initdip += 1

        if initdip > 0: #if there is, create a dip instruction
            scanstructions.append(['d',initdip])

        #now let's look for other tokens
        while len(scansion) > 0:
            token=scansion[0]
            #check for a resolvable lift of any kind
            if token in ['p', 's']:
                scansion=advance(scansion)

                if token == 'p':
                    scanstructions.append(['l']) # primary stress -> lift
                if token == 's':
                    scanstructions.append(['h']) # secondary stress -> half lift

                #Process the dip
                dip=0
                while len(scansion)>0 and scansion[0] in ['x','X']:
                    scansion=advance(scansion)
                    dip+=1

                if dip > 0:
                    #Suzuki doesn't indicate when resolution occurs in his scansion. Typically
                    #we're going to resolve the previous light lift with the first of these unstressed
                    #syllables. But in some cases resolution will be suspended: when the light stressed
                    #syllable sits between two heavies, the earlier of which is not part of a dip
                    #(Goering's "sandwich rule" formulation of Kaluza's law).
                    def GoeringKaluza():
                        scanpos=len(syllables)-len(scansion)-1
                        try:
                            prevstresssyll=syllables[scanpos-2]
                            prevweight=prevstresssyll.get('wt')
                        except: prevweight='l'

                        #is the prior syllable in a stress domain?
                        try:
                            prevstress = scanstructions[-2] in ['h', 'l']
                        except: prevstress = False
                        
                        afterstresssyll = syllables[scanpos]
                        afterweight = afterstresssyll.get('wt')
                        endofline = scansion==[]
                        suspension = (prevstress or endofline) and prevweight != 'l' and afterweight != 'l'
                        return suspension  

                    suspension=GoeringKaluza()

                    if dip==1 and suspension:
                        scanstructions.append(['s']) # suspended resolution
                        scanstructions.append(['d', dip]) # all the x's go in the dip
                    else:
                        scanstructions.append(['r']) # resolution
                        if dip > 1:
                            scanstructions.append(['d', dip-1]) # all but the first x/X goes in the dip

            if token in ['P', 'S']:
                if token == 'P':
                    scansion=advance(scansion)
                    scanstructions.append(['l']) #long primary stress -> lift
                elif token == 'S': 
                    scansion=advance(scansion)
                    scanstructions.append(['h']) #long secondary stress -> half lift

                #See whether there's a dip
                dip=0
                while len(scansion)>0 and scansion[0] in ['x','X']:
                    scansion=advance(scansion)
                    dip+=1
                if dip > 0:
                    scanstructions.append(['d',dip])
        return scanstructions
    
    def _prepsievers(self, scanstr:str):
        scansion=list(scanstr)
        scanstructions=[] #for now
        return scanstructions

    def _preprussom(self, scanstr:str):
        scansion=list(scanstr)
        scanstructions=[] #for now
        return scanstructions

    # implement the instructions by placing either <z> or <f>
    # elements between syllables and filling out attributes, etc.
    def _doscan(self,syllables:list,scanstructions:list):
        # print('doing the scan',scanstructions) ###debug
        scursor=0
        verse=syllables[scursor].getparent() #they all have the same parent verse
        for i in scanstructions:
            cmd=i[0]
            # print('command', cmd) ###debug
            if cmd=='a': #set an attribute value
                # print(i) ###debug
                key=i[1][0]
                value=i[1][1]
                verse.set(key, value)

            
            #metrical positions --> <z>
            elif cmd in ['d','h','l']: 
                # print('command', cmd) ###debug
                if len(syllables)>scursor-1:
                    s=syllables[scursor]
                    z=self._et.Element('z')
                    z.set('h',cmd) #make it a position of the specified height
                    verse.insert(verse.index(s),z) #put it right before
                    #the current syllable
                    if len(i)>1:
                        scursor += i[1]
                    else: scursor += 1
            
            elif cmd=='r': #mark syllables as resolved
                # print('command', cmd) ###debug
                syllables[scursor-1].set('res','1')
                syllables[scursor].set('res','2')
                scursor +=1 #advance the cursor

            elif cmd=='s': #mark suspended resolution
                # print('command', cmd) ###debug
                syllables[scursor-1].set('sus','1')
                syllables[scursor].set('sus','2')
                #do not advance the syllable cursor