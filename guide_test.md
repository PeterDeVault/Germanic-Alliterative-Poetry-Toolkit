<p>Germanic Alliterative Poetry Markup Quick Reference</p>
<p>There are four stages of markup: “Initial”, in which the document is
prepared for alliterative analysis and lineation; “Lineated”, in which
are identified the alliterative series in play and words are rearranged
into poetic lines and verses based on alliterative membership;
“Preanalytic”, which is the lineated document provided with syllabic
structure and readied for metrical annotation; and “Metrical” in which
features of the metrical grammar of the poem are annotated. This is the
final document stage. Ideally, the transformation of an Initial document
into an Alliterative one, and thence into Lineated and penultimately
Preanalytic versions, will be accomplished using forthcoming automated
tools, but some manual tweaking is likely to be necessary even with
their use. Each document stage carries with it the information from the
previous and is in that sense conservative. A transform could revert a
Lineated document into an Initial document, etc. While the relationship
between Initial and Preanalytic stages (and the others in between) is to
some degree mechanical, any number of Metrical analyses are possible
from a single Preanalytic document.</p>
<p>Initial stage Description: At this stage, the manuscript is
represented as a series of lines on pages, with the <lb/> and <pb/>
milestone markers used to indicate the beginning of each. <w> elements
are used to enclose prosodic words as members of those lines. Letter
forms should be normalized according to the detailed GAP mark-up
reference (forthcoming). Long vowels or vowel combinations should be
marked with a macron over the first vowel. Palatalized ‘g’ and ‘c’
should be over-dotted. Words that are elements of compounds are
correlated using the <span class="citation" data-cites="c">@c</span>
attributes. Prefixes and roots are similarly correlated using <span
class="citation" data-cites="p">@p</span> attributes. Word class
(Kendall) is captured in the <span class="citation"
data-cites="wc">@wc</span> attribute. Part of speech is captured using
the Menota <span class="citation" data-cites="msa">@msa</span>
(morpho-syntactic analysis) attribute (only the part of speech and verb
finiteness components of this attribute are required).</p>
<p>The manuscript text may be substituted for alternative text in four
standard ways: • Abbreviations are expanded in the content of the <w>
element, with the original abbreviation preserved in an <span
class="citation" data-cites="expands">@expands</span> attribute. •
Emendations are made within the content of the <w> element with the
original text preserved in an <span class="citation"
data-cites="emends">@emends</span> attribute. • A contracted manuscript
form may be preserved in the <span class="citation"
data-cites="contr">@contr</span> attribute and replaced with an
uncontracted form in the contents of the <w> element to permit correct
syllabification at a later stage. • Similarly, manuscript forms with
epenthetic vowels may be preserved in the <span class="citation"
data-cites="epen">@epen</span> attribute and the reduced form supplied
in the contents of the element. Clause beginnings are marked with a
<cb/> milestone. The document is prepared for lineation.</p>
<p>Elements &amp; attributes Explanation Values <pb/> TEI page beginning
milestone <span class="citation" data-cites="n">@n</span> Indicates the
identity of the page within the manuscript, e.g. “12r” 3, 6v, 123r <lb/>
TEI line beginning milestone <span class="citation"
data-cites="n">@n</span> Indicates the line number number on the page 5
<w> Prosodic word <span class="citation" data-cites="wc">@wc</span> Word
class ‘s’= stressed element ‘c’=proclitic ‘t’=particle <span
class="citation" data-cites="msa">@msa</span> TEI morphosyntactic
analysis attribute. See https://www.menota.org/HB3_ch11.xml#sec11.3.
Additionally, the value ‘xPX’ indicates an unstressed prefix; ‘xNX’ =
negative particle. xNC, xVB fF xUP <span class="citation"
data-cites="c">@c</span> Compound word correlator. “1” for the first
word in a compound, “2” for the second. Longer compounds are nested. 1,
2 C Prefix-root correlator. A clitic prefix is marked with a “1”, the
work prefixed is marked with a “2” 1, 2 <span class="citation"
data-cites="expands">@expands</span> Contains the abbreviation expanded
in the contents of the element “ꝥ” “ꝥ” <span class="citation"
data-cites="emends">@emends</span> Contains the original text which is
emended in the contents of the element See example <span
class="citation" data-cites="contr">@contr</span> Contains a contracted
manuscript form which is expanded in the contents of the element. <span
class="citation" data-cites="epen">@epen</span> Contains a manuscript
form with an epenthetic vowel; the earlier form is contained in the
contents of the element.<br />
<span class="citation" data-cites="num">@num</span> Contains manuscript
numerals spelled out in the contents of the element “·XV·” <cb/> Clause
beginning <span class="citation" data-cites="type">@type</span> Clause
type ‘d’=dependent ‘i’=”independent</p>
<p>Example (Cotton Vitellius A.XV) … <pb n="129r"/> <lb n="1"/>…</p>
<p><lb n="2"/> <cb type="i"/> … <w msa="xNC" wc="s" c="1">þeod</w>
<w msa="xNC" wc="s" c="2">cyninga</w><br />
<lb n="3"/> <w msa="xNC" wc="s">þrym</w><br />
<w msa="xUP" wc="c" p="1">ġe</w><!-- no msa category assigned for unstressed prefixes; xUP is a local addition -->
<w msa="xVB fF" wc="t" p="2">frūnon</w> … <pb n="132r"/> … <lb n="15"/>
<w msa="xNP" wc="s" c="1">hrōð</w> <w msa="xNP" wc="s" c="2">gār</w>
<w msa="xCC" wc="t" expands="&#x204A;">ond</w>
<w msa="xNP" wc="s">halga</w> <w msa="xAJ" wc="s">til</w>
<!-- substantivized adjective --> <cb type="i"/>
<w msa="xVB fF" wc="t">hyrde</w> <w msa="xPE" wc="t">ic</w>
<w msa="xPD" wc="t" expands="&#xA765;">þæt</w>
<!-- pronoun/determiner; manuscript abbr. ꝥ -->
<w msa="xNP" wc="t" emends="elan">Onelan</w> &lt;!— <span
class="citation" data-cites="msa">@msa</span> of the emended form –&gt;
<w msa="xNC" wc="s">cwēn</w> …   Lineated stage Description: An
alliteration detector in the Lineator transform will annotate the words
whose root syllable alliterates in a potentially significant
(functional) way. The Lineator will then attempt to restructure the
words into poetic lines (verse pairs) and half-lines (verses). It will
be successful to the extent that (1) the poem’s composition obeys Kuhn’s
laws, (2) there are no clause breaks in the middle of verses, and (3)
the verses are neither hyper- nor hypo-metric. The remainder of the poem
(or its entirety if it differs radically from these expectations) will
need to be annotated by hand to meet the description below. Line, page,
and clause breaks are kept in original word sequence though the words
are now arranged in a different hierarchy.</p>
<p>Elements &amp; attributes Explanation Values <w> The word element
from the Initial stage <span class="citation" data-cites="A">@A</span>
The sound of the onset of the root syllable. May be any
language-appropriate consonant sound, the sound clusters spelled ‘sp’,
‘st’, and ‘sk’, or a vowel, symbolized by ∅ for ‘null’ alliteration. “g”
“sp” “∅” <vg> A verse group. These may be nested, as a pair of verses in
a larger stanza. <span class="citation" data-cites="type">@type</span>
In my target corpus, this will be a verse pair linked by common
alliteration. This corresponds to an Old English poetic line and a line
or pair of verses in Norse fornyrðislag, etc. In other meters this may
be a stanza, etc. “line” “stanza” <span class="citation"
data-cites="A">@A</span> Recapitulates the alliteration annotation at a
higher level. See above. See above <span class="citation"
data-cites="cid">@cid</span> Conventional identifier 384 <v> A poetic
verse.<br />
<span class="citation" data-cites="role">@role</span> For the poetry in
my target corpus, this indicates whether the verse is the “on-” or
“off-” verse (equivalent to “a-” and “b-”). For other meters, this may
indicate other roles, such as the third full line in ljóðaháttr. “on”
“off” <span class="citation" data-cites="cid">@cid</span> Conventional
identifier 384b <span class="citation"
data-cites="clausetype">@clausetype</span> (optional) Clausal type
(Kendall). Clause-restricted, displaceable, etc. Represented as Ia, III,
etc. Ia, Ib, Ic, II, III</p>
<p>Example (Cotton Vitellius A.XV) dropping unnecessary attributes –
these would be kept in a real context <pb n="135v"/>… <lb n="135v;7"/>
<!-- the manuscript and poetic lines coincide here at the beginning of this fitt -->
<vg type="line" A="∅"> <v role="on"> <cb type="i"/>
<w wc="t">Him</w><br />
<w wc="c">se</w> <w wc="s" A="∅">yldesta</w> </v> <v role="off">
<w wc="t" A="∅">andswarode</w> </v> </vg> <vg type="line" A="w">
<v ab="a"> <w wc="s" A="w">werodes</w> <w wc="s" A="w">wīsa</w> </v>
<v ab="b"> <lb n="135v;8"/>
<!-- a new manuscript line begins in the middle of a poetic line -->
<cb type="i"/> <w wc="s" A="w" c=1>word</w><w wc="s" c="2">hord</w>
<w wc="c" p="1">on</w><w wc="t" p="2">lēac</w> </v> </vg></p>
<p>  Preanalytic stage Description: The syllable breaker (syllabifier?,
syllabeler?) will identify the syllable boundaries of each word
according to the onset, closure, and sonority rules appropriate to the
medieval Germanic languages, with an option for the coda-maximizing
approach should an analyst require it. Syllables, the lowest level of
textual markup in the GAP markup scheme, are represented by <σ> elements
and will be marked for weight based on mora count in accordance with the
syllable-breaking algorithm. Words will be structurally demoted from an
enclosure using <w> elements to the <ω/> milestone, which inherits the
attributes of the <w> element other than the alliteration. The
alliterative symbol will be transferred from the word to the root
syllable.</p>
<p>Elements &amp; attributes Explanation Values <pb/> TEI page beginning
milestone <span class="citation" data-cites="n">@n</span> Indicates the
identity of the page within the manuscript, e.g. “12r” 3, 6v, 123r <w/>
The beginning of a sequence of syllables making up a word @… Attributes
inherited from <w>, except <span class="citation"
data-cites="A">@A</span>. See above and below. 5 <s> A syllable. The
lowest level of markup on the text itself. <span class="citation"
data-cites="A">@A</span> Appears on the root syllable of the word only.
See above. <span class="citation" data-cites="wt">@wt</span> Syllable
weight. “L”=light “H”=heavy “O”=over-heavy</p>
<p>Example (Cotton Vitellius A.XV) <vg type="pair" A="∅"> <v ab="a">
<cb type="i"/> <w wc="t"/> <σ wt="H">him</σ><br />
<w wc="t"/> <σ wt="L">se</σ> <w wc="s" A="∅"/> <σ A="∅" wt="H">yl</σ>
<σ wt="L">de</σ> <σ wt="L">sta</σ> </v> <v ab="b"> <w wc="t"/>
<σ A="∅" wt="O" >and</σ> <σ wt="L">swa</σ> <σ wt="L">ro</σ>
<σ wt="L">de</σ> </v> </vg></p>
<p>  Metrical stage Description: This is the stage at which metrical
analysis can be documented. Any number of alternative metrical analysis
can be derived from the same Preanalytic document, and as with each of
the earlier stages, any Metrical document will preserve all of the
information in the Preanalytic document, keeping the promises of
reversability and traceability to the manuscript. This also ensures that
all metrical analysis are starting from the same baseline. Resolution of
a light stressed syllable with the following syllable is expressed using
<span class="citation" data-cites="res">@res</span> correlator
attributes on each syllable. Suspension of resolution is marked the same
way using <span class="citation" data-cites="sus">@sus</span>
correlators.</p>
<p>Immediately we are faced with the question of whether we wish to
annotate a metrical position-based analysis or one based on word-feet;
the annotation schemes are slightly different. For the former, we
introduce the <π/>, position, milestone. For the latter, the <φ/> and
<xm/> elements signal the beginning of feet and extrametrical material,
respectively. The final new element is <k/>, standing for the position
of the kolon (Heusler). This is a concept elaborated by Bliss as the
caesura separating two “breath group” constituents of a normal verse.
(Pope and Creed also employ such a concept to draw a boundary between
half-line (verse) constituents). The kolon may be inserted in the flow
of either metrical positions or word-feet to indicate the possible
phrasing of someone reciting the poem.</p>
<p>In addition to new elements, a Metrical document makes use of new
attributes on the <v> element to memorialize observations yielded by the
metrical analysis.</p>
<p>Elements &amp; attributes Explanation Values <s> A syllable.
Introduced above. <span class="citation" data-cites="res">@res</span>
Correlates a pair of resolved syllables. The first syllable equals “1”
and the second “2”. 1, 2 <span class="citation"
data-cites="sus">@sus</span> Correlates a pair of syllables in suspended
resolution. 1, 2 <z/> Metrical position beginning <span class="citation"
data-cites="h">@h</span> “Hight”, metaphorically speaking, of the
metrical position “l”=lift “d”=dip “h”=half-lift or half-dip <f/> The
beginning of a sequence of one or more syllables in a word-foot. <span
class="citation" data-cites="w">@w</span> The prototypical word pattern
forming the foot. This is not an annotation of the syllables to follow;
it is an index into the list of possible word-foot patterns in medieval
Germanic. “Ssx”, “Sx”, “xx” <x/> In a word-foot analysis, this milestone
marks the beginning of extra-metrical syllables preceding either of the
two feet in a normal verse. In positional analysis, this marks
anacrusis. <k/> Heusler’s kolon or Bliss’s caesura separating two breath
groups. <v> The verse container introduced in previous stages. See
above. <span class="citation" data-cites="type">@type</span> The type of
the verse. By default, this is the Sievers type, but other named type
systems can be employed. “A3” “D2a” <span class="citation"
data-cites="contour">@contour</span> The metrical contour of the verse.
By default, this is the Yakovlev contour, but other named type systems
can be employed. “SxSx” <span class="citation"
data-cites="restr">@restr</span> Clause restriction type of the verse
(Kendall). Verses may be clause initial and displaceable (Ia), clause
initial, non-displaceable (Ib), clause non-initial (II), or
clause-unrestricted (III). Ia, Ib, II, III</p>
<p>The following is incomplete Example I Þrymsqviða 25/7: “né inn Meira
mioð“ <v contour="xx/Sxs"> <ω wc="c"/>
<φ w="xx"/><σ wt="L">né</σ><ω wc="c"/><σ wt="H">inn</σ>
<φ w="Sxs"/><ω wc="p"/><σ wt="H">mei</σ><σ wt="L">ra</σ><ω wc="s"/><σ wt="O">mioð</σ>
</v></p>
<p>Example II Beowulf 3b</p>
<p><v role="off"> <ω wc="s"/> <π h="l"/><σ wt="H">el</σ>
<π h="d"/><σ wt="H">len</σ><ω wc="p"/> <k/>
<π h="l"/><σ wt="H" res="1">fre</σ><σ wt="L" res="2">me</σ>
<π h="d"/><σ wt="H">don</σ> </v></p>
