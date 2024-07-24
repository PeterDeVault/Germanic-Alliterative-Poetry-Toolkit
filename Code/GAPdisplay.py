from GAPdocumenthelper import docuhelper as dh
from lxml import etree as et
from GAPutility import msa2str, getstyle, gettemplate, gettoggles

#the displaydriver class. Instantiate with a docuhelper object 
#and it will give you an html string suitable for framing and display.
class displaydriver():
    NONE=0
    ANNOTATED=1
    LINEATED=2
    SYLLABIFIED=3
    ANALYZED=4

    #hold the default TEI namespace used to qualify element searches, etc.
    _TEIns={'d': 'http://www.tei-c.org/ns/1.0'}
    _markuplevel=NONE
    _dh=None
    options={} #public
    
    def __init__(self, dh, options={}):
        self._markuplevel=dh.markuplevel
        self._dh=dh
        
    #this is probably what you're after
    def generatehtml(self):
        print('generating html')
        contents=""

        root = self._dh._root

        #the main loop. renderchild will delegate to various element and markup handlers.
        #loopdata is the place to store any data that needs to persist over iterations of the loop
        loopdata=   {'prefix': False,   #a prefix turns this True, the subsequent syllable/word sets it to False
                    'compound': False,  #a compounding word turns this True, the subsequent syllable sets it to False
                    'emends': '',       #un-emended text for the current word
                    'expands': '',      #the abbreviation expanded by the current word
                    'syllRemain': 0,    #how many more syllables remain in the current word
                    'z': "",            #the metrical position being processed
                    'x': "",            #the extra-metrical foot being processed
                    'f': "",            #the word-foot being processed
                    'backlog': []       #storage for processed nodes waiting for a verse context
                    }

        bodyEl=root.find(".//d:body", self._TEIns)
        if bodyEl is not None:
            for child in bodyEl:
                contents += self._renderchild(child, loopdata)

        html="" #clear the slate
        #assemble the pieces
        opening=gettemplate(0) 
        style=getstyle()
        pretitle=gettemplate(1)
        title=self._getheader(True)
        posttitle=gettemplate(2)
        header=self._getheader()
        toggles=gettoggles(self._markuplevel) + gettemplate(3)
        footer=gettemplate(4)

        html += opening + style + pretitle + title + posttitle
        html += header + toggles + contents + footer
        return html

    #for non-verse-specific nodes like <lb>, <cb>, 
    # are they located within or outside a verse or line?
    def _isinversecontext(self, node):
        parenttype=''
        if node is None: return False
        try:
            tag=node.getparent().tag
            parenttype=tag[tag.find('}')+1:]
        except Exception as e: return e
        return parenttype == 'v'

    #the loop delegator
    def _renderchild(self, child, loopdata):
        contents=''
        childtype=''
        fx={'vg':   '_render_group',
             'v':   '_render_verse',
             'w':   '_render_word',
            'pb':   '_render_manuscript_page',
            'lb':   '_render_manuscript_line',
            'cb':   '_render_clause',
            'pc':   '_render_punctuation',
             'p':   '_render_prose',
             's':   '_render_syllable',
             'z':   '_render_position',
             'f':   '_render_foot',
             'x':   '_render_xtrametric'
            }
        if child.tag != et.Comment:
            try:
                childtype=child.tag[child.tag.find('}')+1:] #strip namespace
            except: return ''
            if childtype !='':
                try: contents += self.__getattribute__(fx[childtype])(child, loopdata) or ''
                except Exception as e: return e
        return contents
    #
    def _render_prose(self, p, loopdata):
        contents=''
        contents += '<span class="prose">' + p.text + '</span>\n'
        return contents

    ####################################################
    #the 'group' here is the poetic line
    def _render_group(self, line, loopdata):
        contents=''
        lnum = 0 #line number

        #open the line container
        contents +='\n<div class="poeticline">'

        #Get the alliteration for this line
        if 'A' in line.attrib: loopdata['A'] = line.get('A')
        else: loopdata['A'] = '' #make sure we're not using an old value 

        #Get the conventional line number; display for every 5th line
        if 'cid' in line.attrib:
            lnum=int(line.get('cid'))

        lineclass='lineintro'
        if int(lnum) % 5 == 0: lineclass='lineintro5'
        contents += '\n<div class="' + lineclass + '">' + str(lnum) + '</div>'


        #start off the middle (content) div
        contents += '\n<div class="linecontent">'

        #children of the line will include verses, but also line and page breaks, punctuation, etc.
        for child in line: 
            contents += self._renderchild(child, loopdata)
        return contents

    ###################################################
    #when a verse begins, open and close the right divs
    def _render_verse(self, verse, loopdata):
        contents=""

         #get the verse scan info
        if 'type' in verse.attrib: typ=verse.get("type")
        else: typ=''
        if 'contour' in verse.attrib: contour= verse.get("contour")
        else: contour=''

        on=False
        if "role" in verse.attrib:
            role = verse.get("role")
            if role=="on": 
                on=True
                #stuff these into loopdata to use after the off-verse
                loopdata["scan"]=[typ,contour]

        #open the verse div
        contents += '\n<div class="verse">'

        #before we get to any children of this node, go through the backlog of processed nodes, if any
        i = len(loopdata['backlog'])
        error = False
        while not error:
            try:
                item = loopdata['backlog'].pop(0)
            except: 
                error = True
                break
            contents += item

        #children of the verse will include words and syllables, but also line and page breaks, punctuation, etc.
        for child in verse: 
            contents += self._renderchild(child, loopdata)
    
        #close the verse div
        contents += "</div>\n"
        if on:
            #add a caesura here at the end of the on-verse
            contents += "\n<div class='caesura'/>"
        else: #off
            contents += '</div>\n' #close the linecontent div
            #time to display things
            #first verse

            contents += '\n<div class="linesummary">'
            onscan=loopdata["scan"]
            if len(onscan)>1:
                ontype=loopdata["scan"][0]
                oncontour=loopdata["scan"][1]
            contents += '\n<div class="scan">\n'
            contents += '<span class="versetype">' + ontype + '</span>'
            contents += '<span class="versecontour">' + oncontour + '</span></div>\n'
            contents += '\n<div class="scan">\n'
            contents += '<span class="versetype">' + typ + '</span>'
            contents += '<span class="versecontour">' + contour + '</span></div>\n'
            contents += '</div>' #close the linesummary div

            contents += '</div>' #close off the poeticline div

        return contents

    #######################################################
    def _render_word(self, word, loopdata):
        contents=''
        wc=''
        msa=''
        expands=''
        emends=''
        loopdata['wc']=''   #new word context
        loopdata['msa']=''
        loopdata['expands']=''
        loopdata['emends']=''

        #Unpack the contents of the <w/>, which is entirely attributes
        if 'wc' in word.attrib:
            wc=word.get('wc')
            loopdata['wc']=wc

        if 'expands' in word.attrib:
            expands=word.get('expands')
            loopdata['expands']=expands

        if 'emends' in word.attrib:
            emends=word.get('emends')
            loopdata['emends']=emends

        if 'msa' in word.attrib: 
            msa=word.get('msa')
            #get the contents ready, but wait to put this after the last syllable of the word
            try:
                loopdata['msa']='<span class="msa">' + msa2str(msa) + '</span>'
            except: loopdata['msa']=''

        
        loopdata["firstSyll"]=True
        #get the syllable count
        if 'Σ' in word.attrib: syllables=int(word.get("Σ"))
        else: syllables=0
        loopdata['syllRemain']=syllables #the number of syllables in the word yet to be rendered
        if 'p' in word.attrib: loopdata['prefix']=int(word.get('p'))
        else: loopdata['prefix']=0
        if 'c' in word.attrib: loopdata['compound']=int(word.get('c'))
        else: loopdata['compound']=0
        
        contents +='<span class="wc">' + wc + '</span>'
                    
        
        return contents 

    #####################################################
    def _render_syllable(self, syll, loopdata):
        contents = ''
        allit = ''
        #given the foot or position domain, look at the loop data to see what the stress level is for the current syllable
        def ictus(domain,loopdata):
            if (domain == 'position' and loopdata['z']=='l') or \
               (domain =='foot' and loopdata['f'][0:1]=="S"):
                return 'high'
            elif (domain == 'position' and loopdata['z']=='h') or \
                 (domain == 'foot' and loopdata['f'][0:1]=='s'):
                return 'half'
            return 'low'

        #Are we in a foot? A metrical position? Set the domain variable accordingly.
        if loopdata['z'] != '':     domain='position'
        elif loopdata['f'] != '':   domain='foot'
        else:                       domain='xmetrical'

        if "A" in syll.attrib: allit=syll.get("A")

        #annotate the alliterating syllables, but only if they bear ictus
        stress=ictus(domain, loopdata)
        if loopdata["firstSyll"] and allit==loopdata["A"] and (stress=="high" or stress=="half"):
            contents +='<span class="allit1">' + allit + '</span>'
        
        #deal with extra-metrical syllables
        #if this is the first syllable of an extrametrical position, open it with a '('
        close_xmetrical=False
        if domain=='xmetrical':
            fraction=loopdata['x']
            if len(fraction.split("/"))>1:
                numerator=fraction.split("/")[0] #how many x-metrical syllables remain
                denominator=fraction.split("/")[1] #out of how many in total
                if numerator==denominator: #this is the first                   #these conditions look reversed. keep an eye out.
                    contents +='<span class="x_sep">(</span>'
                if numerator == "1": #if it's the last
                    close_xmetrical=True        #we'll flag it to be closed
                loopdata['x']=str(int(numerator)-1) + "/" + denominator #decrement the numerator
            

        #gather info for the styling of the content
        if syll.text != None:
            #get the syllable weight from the 'wt' attribute if present
            if 'wt' in syll.attrib: weight=syll.get('wt')
            else: weight=''

            #what's the stress level?
            stress=ictus(domain, loopdata)

            #we will place any abbreviations or unemended text for the word in the hover title of each syllable
            hoverstr=loopdata['emends']
            if hoverstr=='': hoverstr=loopdata['expands']
            
            #we have all the details
            contents += '\n<span class="syll ' + weight + ' ' + stress + '" title="' + hoverstr + '">' + syll.text + '</span>'

            #now clean up and update loop variables
            #if we figured out above we're in the last syllable of an extra-metrical position, close it out now
            if close_xmetrical: contents +='<span class="x_sep">)</span>'

            #if there are more syllables coming up, separate them with a dot or the appropriate resolution/suspension symbol
            resolving=False
            suspending=False
            if 'res' in syll.attrib:
                if syll.get('res')=='1': resolving = True
            if 'sus' in syll.attrib:
                if syll.get('sus')=='1': suspending = True
            
            loopdata['syllRemain'] -= 1
            if loopdata['syllRemain']>0:
                if resolving:
                    contents += '<span class="separator">•</span>'
                elif suspending:
                    contents += '<span class="separator">⚬</span>'
                else:
                    contents += '<span class="separator">·</span>'

            else: #last syllable of the word
                
                contents +=loopdata['msa']
                
                if loopdata['prefix']==1 or loopdata['compound']==1: contents += '-'
                # else: contents += ' '
        
        #lop off the current toe of the foot -- unless there's a resolved syllable upcoming
        if domain == 'foot' and not resolving:
            loopdata['f']=loopdata['f'][1:]
        loopdata['firstSyll']=False

        return contents

    

    #the opening of a metrical position
    def _render_position(self, z, loopdata):
        contents = '' 
        height = ''
        if 'h' in z.attrib:
            height=z.get('h')
        else: return contents
        loopdata['z']=height
        loopdata['x']='' #if we were in an extra-metrical position before, we aren't now
        loopdata['f']='' #nor are we in a foot
        return contents   

    #a metrical foot begins
    def _render_foot(self, f, loopdata):
        contents =  ''
        word =''
        if 'w' in f.attrib:
            word=f.get('w')
        else:
            return contents
        loopdata['z']="" #if we were in a metrical position before, we aren't now
        loopdata['f']=word
        loopdata['x']="" #nor are we in an extra-metrical position
        return contents

    #the start of extrametrical material
    def _render_xm(self, xm, loopdata):
        contents = ''
        xsylls = ''
        if 'Σ' in xm.attrib: xsylls = xm.get('Σ')
        else: return contents
        loopdata['z']='' #if we were in a metrical position before, we aren't now
        loopdata['f']='' #nor are we in a foot
        loopdata['x']= xsylls + "/" + xsylls
        return contents

    def _render_manuscript_page(self, pb, loopdata):
        contents=''
        pnum=''
        if 'n' in pb.attrib:
            pnum=pb.get('n')
            contents += '<span class="pagebegin" title="' + pnum + '">♦</span>'
        else: contents += '<span class="pagebegin"/>'

        #we're either going to return the contents now or save it for later
        #depending on whether we're currently in a verse context
        if self._isinversecontext(pb): 
            return contents
        else:
            loopdata['backlog'].append(contents)
            return ''

    def _render_manuscript_line(self, lb, loopdata):
        contents=''
        lnum=''
        if 'n' in lb.attrib:
            lnum=lb.get('n')
        else: lnum='?'
        contents += '<span class="linebegin" title="' + lnum + '">♦</span>'

        #we're either going to return the contents or save it for later
        #depending on whether we're currently in a verse context
        if self._isinversecontext(lb): 
            return contents
        else:
            loopdata['backlog'].append(contents)
            return ''

    def _render_clause(self, cb, loopdata):
        contents=''
        contents = '<span class="clause">§</span>'

        #we're either going to return the contents or save it for later
        #depending on whether we're currently in a verse contenxt
        if self._isinversecontext(cb): return contents
        else:
            loopdata['backlog'].append(contents)
            return ''

    def _render_punctuation(self, pc, loopdata):
        contents=''
        contents = '<span class="punc">' + pc.text +'</span>'

        #we're either going to return the contents or save it for later
        #depending on whether we're currently in a verse contenxt
        if self._isinversecontext(pc): return contents
        else:
            loopdata['backlog'].append(contents)
            return ''

    def _getheader(self, titleonly:bool=False):
        header=""
        title=self._dh._root.findtext(".//{http://www.tei-c.org/ns/1.0}title")
        if title == None: title="Markup error"
        title=title.strip()
        if titleonly: return title

        subtitle=self._dh._root.findtext(".//{http://www.tei-c.org/ns/1.0}subtitle")
        if subtitle == None: subtitle="Markup error"
        subtitle=subtitle.strip()

        source=self._dh._root.findtext(".//{http://www.tei-c.org/ns/1.0}sourceDesc/{http://www.tei-c.org/ns/1.0}p")
        if source == None: source="Markup error"
        source=source.strip()
        header += '<div id="leftheader">'
        header += '<div id="title">' + title + '</div>'
        header += '<div id="subtitle">' + subtitle + '</div>'
        header += '<div id="source">' + source + '</div>'
        header += '</div>'
        return header
