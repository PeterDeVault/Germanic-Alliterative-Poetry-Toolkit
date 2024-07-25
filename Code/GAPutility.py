def gettemplate(piece:int=0):
    template=["""<!DOCTYPE html>
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
                """
            </div>
            <div id="poetry">
    """,

    """     </div> <!-- close the content div -->
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

#get the right display toggles for the document markup level
def gettoggles(documentlevel:int=0):
    toggles = '''
    <div class="toggles">
        <h2>Toggle manuscript info</h2>
        <div class="toggle" data-target="manuscript"> <span class="manuscript">ᚦ</span> &nbsp;lines and pages</div>
        <div class="toggle" data-target="punctuation"> <span class="punctuation">ᚦ</span> &nbsp;punctuation</div>
        <div class="toggle" data-target="clauses"> <span class="clauses">ᚦ</span> &nbsp;clause beginnings</div>
        <div class="toggle" data-target="break"> <span class="break">ᚦ</span> &nbsp;syllable breaks</div>
    </div>

    <div class="toggles">
        <h2>Language and meter</h2>
        <div class="toggle" data-target="parts"> <span class="parts">ᚦ</span> &nbsp;POS and word class</div>
        <div class="toggle" data-target="alliteration1"> <span class="alliteration1">ᚦ</span> &nbsp;alliteration</div>
        <div class="toggle" data-target="weight"> <span class="weight">ᚦ</span> &nbsp;syllable weight</div>
        <div class="toggle" data-target="meter"> <span class="meter">ᚦ</span> &nbsp;stress contour</div>
        
    </div>
    '''
    return toggles

def getlegend(documentlevel:int=0):
    legend='''
    <div class="legend">
        <h2>Legend</h2>
        <div class="legenditem parts">
            <span class="key" style="color:Brown">♦</span>
            <span class="text">new page</span>
        </div>
        <div class="legenditem parts">
            <span class="key" style="color:DarkGoldenrod">♦</span>
            <span class="text">new line</span>
        </div>
        <div class="legenditem clauses">
            <span class="key" style="color:FireBrick">§</span>
            <span class="text">new clause</span>
        </div>
    </div>
    '''
    return legend




def getstyle(language="OE", options={}):    #css code for the HTML output
    if not language in ["OE","ON","OS","OHG"]: language="OE"
    
    style="""/* defaults */
    body     {
                overflow: hidden; 
                width: 100%; 
    }
    span     {font-size: 16pt;}
    p        {padding-left: 30px}
    .prose   {color:LightSeaGreen}
    .clause  {color:FireBrick; display:none}
    .punc    {color:FireBrick; padding-left:2px; padding-right:2px; display:none}
    .word    {color:Black}
    .allit1  {color:FireBrick; font-size:70%; vertical-align: super; position:relative; left:4px; display:none}
    .allit2  {color:FireBrick; font-size:70%; vertical-align: super; display:none}
    .msa     {color:CadetBlue; font-size:80%; vertical-align: sub; display:none}
    .wc      {color:Olive; font-size:80%; vertical-align:sub; position:relative; left:4px; display:none}
    .syll    {color:DimGrey; margin:0}

    .pagebegin          {color:Brown; font-size:8pt; vertical-align: super; display:none}
    .pagebegin:hover    {cursor: pointer;}
    .linebegin          {color:DarkGoldenrod; font-size:8pt; vertical-align: super; display: none}
    .linebegin:hover    {cursor: pointer;}

    
    .grouper {color:Indigo}
    .separator {color:Grey ;font-size:70%; display:none}

    /* toggle effects */
    body.break  .separator          {display:inline-block}
    body.weight .syll.l             {color:LightBlue}
    body.weight .syll.h             {color:DimGrey}
    body.weight .syll.o             {color:SteelBlue}
    body.clauses .clause            {display:inline-block}
    body.meter  .syll.high          {font-size:20pt; font-face: bold}
    body.meter  .syll.half          {font-size:18pt}
    body.meter  .syll.low           {font-size:14pt}
    body.meter  .x_sep              {display:inline-block}
    body.parts  .msa                {display:inline-block}
    body.parts  .wc                 {display:inline-block}
    body.alliteration1  .allit1     {display:inline-block}
    body.alliteration2  .allit2     {display:inline-block}
    body.punctuation   .punc        {display:inline-block}
    body.manuscript    .pagebegin   {display:inline-block}
    body.manuscript    .linebegin   {display:inline-block}

    /* header and toggles */
    div#header  {
                display: flex;
                flex-flow: row;
                align-items: flex-start;
                position: absolute;
                top:0; left:0; right:0;
                background-color: WhiteSmoke;
                overflow: hidden;
                }
    div#leftheader {
                flex-grow:1;
                align-self: stretch;
    }
    div#title   {
                display: inline-block;
                color: SteelBlue;
                padding-left: 20px;
                font-size:24pt;
                }
    div#subtitle {
                display: inline-block;
                padding-left: 20px;
                color:lightSkyBlue;
                font-size: 16pt;
                }
    div#source  {
                display: block;
                color:DodgerBlue;
                padding-left: 20px;
                padding-top: 10px;
                font-size: 12pt;
                }
    div.legend  {
                flex: 0 0 200px;
                background-color: WhiteSmoke;
                padding: 10px 20px;
                font-family: "Noto Sans", sans-serif;
                font-size: 10pt;
                color: DarkSlateGrey;
                }
    div.legend h2 {
                margin: 0;
                font-size: 12pt;
                color: LightSkyBlue;
                }
    div.legenditem span {
                font-size: 12pt;
                display:inline-block;
                }
    div.toggles {
                flex: 0 0 200px;
                background-color: WhiteSmoke;
                padding: 10px 20px;
                font-family: "Noto Sans", sans-serif;
                font-size: 12pt;
                color: DarkSlateGrey;
                }
    div.toggles span {color:LightGrey}
    div.toggles h2 {
                    margin: 0;
                    font-size: 12pt;
                    color: LightSkyBlue;
                }
    div.toggle {
                    cursor: pointer;
                }
    div.toggle:hover {
                    color: Grey;
                }
    body.break div.toggle > span.break,
    body.weight div.toggle > span.weight,
    body.parts div.toggle > span.parts,
    body.parts .legenditem.parts span,
    body.wclass div.toggle > span.wclass,
    body.clauses div.toggle > span.clauses,
    body.clauses .legenditem.clauses span,
    body.alliteration1 div.toggle > span.alliteration1,
    body.alliteration2 div.toggle > span.alliteration2,
    body.punctuation div.toggle > span.punctuation,
    body.manuscript div.toggle > span.manuscript,
    body.meter div.toggle > span.meter
    {
        color: DarkSlateGrey;
    }
                    
    .caesura, .linesummary, .verse, .linecontent, .lineintro, .lineintro5, .scan, .verse {
        display: inline-block;
    }

    div#poetry  {
                position:fixed;
                display:inline-block;
                top:140px;
                width: 100%;
                height: 100%;
                overflow: auto;
                }

    div.poeticline {
                display:inline-block;
                width: 100%
                overflow: hidden;
                }

    div.linecontent {
                margin-bottom: 15px;
                }

    div.linesummary {
                width: 400px;
                display:inline-block;
                }
    .verse {width:520px;}
    .caesura {width:10px;}
    .scan {
            position:relative;

            left:400px;
            display:inline-block;
            color:DarkSlateGrey
            }
    .scan > span {
        margin-right:20px;
    }
    .versetype {
            color:SteelBlue;
    }
    .versecontour {
            color:Turquiose;
    }
    .lineintro {
            margin-left:10px;
            color:DimGrey;
            width: 100px;
            }
    .lineintro5 {
            margin-left:10px;
            color:Brown;
            width: 100px;
            }

        """
    return style

#this map will be used to annotate part of speech from the menota msa attribute on a word <w> element
def msa2str(msa):
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
            'xPX':'&lt;',
            'xVX fF':'aux'}
    try:
        return msamap[msa]
    except:
        return ''

