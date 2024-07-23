from GAPdocumenthelper import docuhelper as dh
from lxml import etree as et

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
                    'f': ""             #the word-foot being processed
                    }

        bodyEl=root.find(".//d:body", self._TEIns)
        if bodyEl is not None:
            for child in bodyEl:
                contents += self._renderchild(child, loopdata)

        html="" #clear the slate
        #assemble the pieces
        opening=self._gettemplate(0) 
        style=self._getstyle()
        pretitle=self._gettemplate(1)
        title=self._getheader(True)
        posttitle=self._gettemplate(2)
        header=self._getheader()
        toggles=self._gettemplate(3)
        footer=self._gettemplate(4)

        html += opening + style + pretitle + title + posttitle
        html += header + toggles + contents + footer

        # html += self._gettemplate(0) + self._getstyle() + self._gettemplate(1) + self._getheader(True) + self._gettemplate(2)
        # html += self._getheader() + self._gettemplate(3) + contents + self._gettemplate(4)
        return html

    #the loop delegator
    def _renderchild(self, child, loopdata):
        contents=''
        childtype=''
        fx={'vg':   '_render_line',
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
                except Exception as e: 
                    print(e)
        return contents
    #
    def _render_prose(self, p, loopdata):
        contents=''
        contents += '<span class="line">' + p.text + '</span>'
        return contents

    #the 'line' here is the poetic line, not the manuscript line
    def _render_line(self, line, loopdata):
        contents=''
        lnum = 0 #line number

        #Get the alliteration for this line
        if 'A' in line.attrib: loopdata['A'] = line.get('A')
        else: loopdata['A'] = '' #make sure we're not using an old value 

        #Get the conventional line number; display for every 5th line
        if 'cid' in line.attrib:
            lnum=int(line.get('cid'))
        contents += "<p/>"
        if int(lnum) % 5 == 0:
            contents += '<span class="line">' + str(lnum) + '</span>'
        else:
            contents += '<span class="line"></span>'

        #children of the line will include verses, but also line and page breaks, punctuation, etc.
        for child in line: 
            contents += self._renderchild(child, loopdata)
        return contents

    def _render_verse(self, verse, loopdata):
        contents=""
         #get the verse scan info
        if "type" in verse.attrib:
            typ=verse.get("type")
        else:
            typ=""
        if "contour" in verse.attrib:
            contour= verse.get("contour")
        else:
            contour=""

        on=False
        if "role" in verse.attrib:
            role = verse.get("role")
            if role=="on": 
                on=True
                contents += "<span class='on-verse'/>" #this has to be there
                #stuff these into loopdata to use after the off-verse
                loopdata["scan"]=[typ,contour]
        
        #children of the line will include verses, but also line and page breaks, punctuation, etc.
        for child in verse: 
            contents += self._renderchild(child, loopdata)
    
        #add a caesura here at the end of the on-verse
        if on:
            contents += "<span class='caesura'>&nbsp;&nbsp;&nbsp;</span>"
        else:
            #time to display things
            #first verse
            contents += '<span class="scan"/>'
            try:
                contents += '<span class="scan">' + loopdata["scan"][0] + "&nbsp;&nbsp;" + loopdata["scan"][1] + '</scan>' 
            except:
                contents += '<span class="scan">?</scan>'
            contents += '<span class="scan">' + typ + '&nbsp;&nbsp;' + contour + '</scan>' 
       
        return contents

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
            wc=word.get('expands')
            loopdata['expands']=wc

        if 'emends' in word.attrib:
            wc=word.get('emends')
            loopdata['emends']=wc
        

        if 'msa' in word. attrib: msa=word.get('msa')
        #get the contents ready, but wait to put this after the last syllable of the word
        loopdata['msa']='<span class="msa">' + self._msa2str(msa) + '</span>'
        
        loopdata["firstSyll"]=True
        #get the syllable count
        if 'Σ' in word.attrib: syllables=int(word.get("Σ"))
        else: syllables=0
        loopdata['syllRemain']=syllables #the number of syllables in the word yet to be rendered
        if 'p' in word.attrib: loopdata['prefix']=int(word.get('p'))
        else: loopdata['prefix']=0
        if 'c' in word.attrib: loopdata['compound']=int(word.get('c'))
        else: loopdata['compound']=0
        
        return contents 

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
            print(hoverstr)
            contents += '<span class="syll ' + weight + ' ' + stress + '" title="' + hoverstr + '">' + syll.text + '</span>'

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
                else: contents += ' '
        
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
            contents += '<span class="pagebegin">' + pnum + '</span>'
        else: contents += '<span class="pagebegin"/>'
        return contents

    def _render_manuscript_line(self, lb, loopdata):
        contents=''
        lnum=''
        if 'n' in lb.attrib:
            pnum=lb.get('n')
            contents += '<span class="linebegin">' + lnum + '</span>'
        else: contents += '<span class="linebegin"/>'
        return contents

    def _render_clause(self, cb, loopdata):
        contents=''
        contents = '<span class="clause">§</span>'
        return contents

    def _render_punctuation(self, pc, loopdata):
        contents=''
        contents = '<span class="punc">' + pc.text +'</span>'

        return contents

    #right now these doc parts are just stored in strings; eventually put them in a separate file
    def _gettemplate(self, piece:int=0):

        template=["""<!DOCTYPE html>
        '<!ENTITY % menotaEntities SYSTEM "http://www.menota.org/menota-entities.txt"> %menotaEntities;
        ]>
                    <html>
                        <head>
                            <meta charset="utf-8">
                            <style>
                            """,
        """                 </style>
                            <title>""","""</title>
                        </head>
                        <body>
                            <div id="header">""",
                                """<div class="toggles">
                                    <h2>Toggle annotation</h2>
                                    <div class="toggle" data-target="break"><span class="break">ᚦ</span>&nbsp;syllable breaks</div>
                                    <div class="toggle" data-target="weight"><span class="weight">ᚦ</span>&nbsp;syllable weight</div>
                                    <div class="toggle" data-target="parts"><span class="parts">ᚦ</span>&nbsp;part of speech</div>
                                    <div class="toggle" data-target="alliteration1"><span class="alliteration1">ᚦ</span>&nbsp;alliteration</div>
                                    <div class="toggle" data-target="punctuation"><span class="punctuation">ᚦ</span>&nbsp;punctuation</div>
                                </div>
                            </div>
                            <div id="content">
                    """,

                    """ 
                            </div>
                            <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>

                            <!-- the following attaches a function to the on-click event of the toggles that adds or
                                 removes a class corresponding to the toggle to the body element. These body 
                                 classes are referenced in the relevant CSS to turn on and off various annotations.
                            -->
                            <script>
                            $(function() {
                                $(".toggle").on("click", function() {
                                $("body").toggleClass($(this).data("target"));
                                return false;
                                });
                            });
                            </script>
                        </body>
                    </html>"""]
        if piece<=4:
            return template[piece]
        else: return ""

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

        header += '<div id="title">' + title + '<span id="subtitle">' + subtitle + '</div>'
        header += '<div id="source">' + source + '</div>'
        return header

    #this map will be used to annotate part of speech from the menota msa attribute on a word <w> element
    def _msa2str(self, msa):
        msamap={'xNC': 'n',
                'xNP':'N',
                'xAJ':'aj',
                'xPE':'pr',
                'xPQ':'?',
                'xDP':'d''',
                'xDD':'d',
                'xPD':'pd',
                'xVB fF':'fv',
                'xVB fI':'∞',
                'xVB fP':'vp',
                'xAV':'av',
                'xAR':'ar',
                'xAP':'→',
                'xCC':'ccj',
                'xCS':'scj',
                'xIT':'ix',
                'xIM':'+∞',
                'xRP':'◦',
                'xNX':'-',
                'xPX':'<',
                'xVX fF':'aux'}
        try:
            return msamap[msa]
        except:
            return ""

    def _getstyle(self, language="OE", options={}):    #css code for the HTML output
        if not language in ["OE","ON","OS","OHG"]: language="OE"
        
        style="""   
                                span     {display: inline-block; margin: 0; font-size: 16pt;}
                                img      {float:right; width:400px; padding-left: 20px; padding-right: 40px}
                                p        {padding-left: 30px}
                                p.info   {padding-left: 10px; font-size:80%; color: CadetBlue; float:right; display:block}
                                .pagebegin    {color:LightSkyBlue; padding-right:4px; padding-left: 10px; display:none}
                                .linebegin    {color:CadetBlue; width:40px; display: none}
                                .on-verse {position:absolute; margin-left:30px}
                                .prose   {color:LightSeaGreen}
                                .punc    {color:FireBrick; padding-left:2px; padding-right:2px; display:none}
                                .word    {color:Black}
                                .allit1  {color:FireBrick; font-size:50%; vertical-align: super; display:none}
                                .allit2  {color:FireBrick; font-size:50%; vertical-align: super; display:none}
                                .msa     {color:CadetBlue; font-size:60%; vertical-align: sub; display:none}
                                .syll    {color:DimGrey}

                                .clause  {color:FireBrick}
                                .grouper {color:Indigo}
                                .separator {color:Grey ;font-size:80%; display:none}

                                /* toggle effects */
                                body.break  .separator       {display:inline-block}
                                body.weight .syll.l          {color:LightBlue}
                                body.weight .syll.h          {color:DimGrey}
                                body.weight .syll.o          {color:SteelBlue}
                                body.parts  .msa             {display:inline-block}
                                body.alliteration1  .allit1  {display:inline-block}
                                body.alliteration2  .allit2  {display:inline-block}
                                body.punctuation   .punc     {display:inline-block}

                                /* header and toggles */
                                div#header  {
                                            position: fixed;
                                            top:0px;
                                            left: 0px;
                                            width: 100%;
                                            background-color: WhiteSmoke;
                                            overflow: hidden;
                                            }
                                div#title   {
                                            color: SteelBlue;
                                            padding-left: 20px;
                                            font-size:40pt;
                                            float:left
                                            }
                                span#subtitle {
                                            padding-left: 10px;
                                            color:lightSkyBlue;
                                            font-size: 24pt;
                                            }
                                div#source  {
                                            color:LightSkyBlue;
                                            padding-left: 20px;
                                            padding-top: 10px;
                                            font-size: 16pt;
                                            position: absolute;
                                            
                                            top: 50px;
                                            }
                                div#content { height: 100%; padding-top: 140px; overflow: auto}
                                div.toggles {
                                            float: right;
                                            display: inline-block;
                                            background-color: WhiteSmoke;
                                            padding: 10px 20px;
                                            font-family: "Noto Sans", sans-serif;
                                            font-size: 10pt;
                                            color: DarkSlateGrey;
                                            }
                                div.toggles span { color:LightGrey}
                                div.toggles h2 {
                                                margin: 0;
                                                font-size: 10pt;
                                                color: LightSkyBlue;
                                            }
                                div.toggle {
                                                cursor: pointer;
                                            }
                                div.toggle:hover {
                                                color: Grey;
                                            }
                                body.break div.toggle span.break,
                                body.weight div.toggle > span.weight,
                                body.parts div.toggle > span.parts,
                                body.wclass div.toggle > span.wclass,
                                body.alliteration1 div.toggle > span.alliteration1,
                                body.alliteration2 div.toggle > span.alliteration2,
                                body.punctuation div.toggle > span.punctuation
                                {
                                    color: DarkSlateGrey;
                                }
            """
        return style