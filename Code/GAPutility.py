def getstyle(language="OE", options={}):    #css code for the HTML output
    if not language in ["OE","ON","OS","OHG"]: language="OE"
    
    style="""   
                            span     {font-size: 16pt;}
                            p        {padding-left: 30px}
                            .pagebegin    {color:Brown; font-size:8pt; vertical-align: super; display:none}
                            .pagebegin:hover {cursor: pointer;}
                            .linebegin    {color:DarkGoldenrod; font-size:8pt; vertical-align: super; display: none}
                            .linebegin:hover {cursor: pointer;}
                            .prose   {color:LightSeaGreen}
                            .punc    {color:FireBrick; padding-left:2px; padding-right:2px; display:none}
                            .word    {color:Black}
                            .allit1  {color:FireBrick; font-size:70%; vertical-align: super; display:none}
                            .allit2  {color:FireBrick; font-size:50%; vertical-align: super; display:none}
                            .msa     {color:CadetBlue; font-size:60%; vertical-align: sub; display:none}
                            .syll    {color:DimGrey;}
                            .lineintro {
                                    color:DimGrey;
                                    width: 50px;
                                    }
                            .lineintro5 {
                                    color:Brown;
                                    width: 50px;
                                    }

                            .clause  {color:FireBrick}
                            .grouper {color:Indigo}
                            .separator {color:Grey ;font-size:80%; display:none}

                            /* toggle effects */
                            body.break  .separator       {display:inline-block}
                            body.weight .syll.l          {color:LightBlue}
                            body.weight .syll.h          {color:DimGrey}
                            body.weight .syll.o          {color:SteelBlue}
                            body.meter  .syll.high       {font-size:20pt; font-face: bold}
                            body.meter  .syll.half       {font-size:18pt}
                            body.meter  .syll.low        {font-size:14pt}
                            body.meter  .x_sep           {display:inline-block}
                            body.parts  .msa             {display:inline-block}
                            body.alliteration1  .allit1  {display:inline-block}
                            body.alliteration2  .allit2  {display:inline-block}
                            body.punctuation   .punc     {display:inline-block}
                            body.manuscript    .pagebegin   {display:inline-block}
                            body.manuscript    .linebegin   {display:inline-block}

                            /* header and toggles */
                            div#header  {
                                        display: flex;
                                        flex-flow: row-end;
                                        background-color: WhiteSmoke;
                                        overflow: hidden;
                                        }
                            div#title   {
                                        color: SteelBlue;
                                        padding-left: 20px;
                                        font-size:24pt;
                                        }
                            div#subtitle {
                                        padding-left: 20px;
                                        color:lightSkyBlue;
                                        font-size: 16pt;
                                        }
                            div#source  {
                                        color:DodgerBlue;
                                        padding-left: 20px;
                                        padding-top: 10px;
                                        font-size: 12pt;
                                        }
                            div.toggles {
                                        flex-align:end;
                                        background-color: WhiteSmoke;
                                        padding: 10px 20px;
                                        font-family: "Noto Sans", sans-serif;
                                        font-size: 12pt;
                                        color: DarkSlateGrey;
                                        }
                            div.toggles span { color:LightGrey}
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
                            body.break div.toggle span.break,
                            body.weight div.toggle > span.weight,
                            body.parts div.toggle > span.parts,
                            body.wclass div.toggle > span.wclass,
                            body.alliteration1 div.toggle > span.alliteration1,
                            body.alliteration2 div.toggle > span.alliteration2,
                            body.punctuation div.toggle > span.punctuation
                            body.meter div.toggle > span.meter
                            {
                                color: DarkSlateGrey;
                            }
                            div#poetry  {
                                        display: inline;
                                        width: 100%
                                        overflow: auto
                                        }
                            div.poeticline {
                                        display: inline-block;
                                        }
                            .caesura, .linesummary, .verse, .linecontent, .lineintro, .lineintro5, .clause {
                                display: inline-block;
                                margin-bottom: 10px;
                            }
                            .caesura {width:5%}
                            .verse {width:300px}
                            .linesummary {float: right}
                            .scan {width:200px}

        """
    return style

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
                            """<div class="toggles">
                                <h2>Toggle annotation</h2>
                                <div class="toggle" data-target="break"><span class="break">ᚦ</span>&nbsp;syllable breaks</div>
                                <div class="toggle" data-target="weight"><span class="weight">ᚦ</span>&nbsp;syllable weight</div>
                                <div class="toggle" data-target="parts"><span class="parts">ᚦ</span>&nbsp;part of speech</div>
                                <div class="toggle" data-target="alliteration1"><span class="alliteration1">ᚦ</span>&nbsp;alliteration</div>
                                <div class="toggle" data-target="punctuation"><span class="punctuation">ᚦ</span>&nbsp;punctuation</div>
                                <div class="toggle" data-target="meter"><span class="meter">ᚦ</span>&nbsp;meter</div>
                                <div class="toggle" data-target="manuscript"><span class="parts">ᚦ</span>&nbsp;manuscript parts</div>
                            </div>
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

