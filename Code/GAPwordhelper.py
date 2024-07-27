#the word helper class
class wordhelper:
    import array

    SHORT=0
    LONG=1

    language="oe"
    codamax=False
    
    _types=[]
    _vowels={}
    _consonants={}
    
    def __init__(self,lang:str,codamax=False):
        #set the language if one was passed in; default is oe
        self.language=lang

        #consonant types with their relative sonority values
        liquids=['ġjrlwRLWJ', 9]
        affricates=['ċ', 8]
        nasals=['nmNM', 7]
        vobstruents=['bdđðƀBD', 6]
        vfricatives=['hvHV', 5]
        fricatives=['fxþFXÞ',4]
        vstops=['bdgBDG', 3]
        stops=['ptkcqPTKCQ',2]
        sibilants=['szʃSZ', 1]

        self._types=[liquids,nasals,affricates,sibilants,vobstruents,vfricatives,vstops,fricatives,stops]
        self._consonants={}
        for type in self._types:
            for ltr in type[0]:
                self._consonants[ltr]=type[1]

        #now lets set up our vowels according to length
        shortvowels=["aeiouyæœŒǫǪAEIOUYÆ",self.SHORT]
        longvowels=['âáāêēéīíîôōóöūúûȳýǣĀÁĒÉĪÍŌÓŪÚÜȲÝǢ',self.LONG]

        lengths=[shortvowels,longvowels]
        for length in lengths:  
            for ltr in length[0]:
                self._vowels[ltr]=length[1]
        return None

    #
    #functions for working with sounds represented by characters
    #

    #is the sound a vowel?
    def isvowel(self,sound):
        return self._vowels.get(sound,-1)!=-1

    #returns length of a vowel sound, -1 if the sound is not a vowel.
    def vowellength(self,sound):
        return self._vowels.get(sound,-1) #this will either be SHORT or LONG

    def isconsonant(self,sound):
        return self._consonants.get(sound,-1)!=-1

    # returns relative sonority of a sound. Vowels return 10.
    def sonority(self,sound):
        if self.isvowel(sound): return 10
        return self._consonants.get(sound,-1)

    #
    #functions for working with words and syllables
    #

    def syllweight(self,moras:int):
        #given a mora count, return the syllable weight
        weight=""
        if not self.codamax:     #normal rules
            if moras==1:    weight="l" #light syllable
            elif moras==2:  weight="h" #heavy
            else:           weight="o" #over-heavy
            
        else:               #coda maximalization rules
            if moras<3:     weight="l"
            else:           weight="h" #heavy
        return weight

    #given a stack of letters, collect the next run of either vowels or consonants
    def _collectletters(self,letterstack,type=0):
        VOWELS=0
        CONSONANTS=1
        collectletters=""
        while len(letterstack)>0:
            letter=letterstack.pop()
            if self.isvowel(letter) and type==VOWELS: #if the type of the letter matches the call, collect it
                collectletters +=letter
            elif self.isconsonant(letter) and type==CONSONANTS:
                collectletters +=letter
            else: 
                if self.isvowel(letter) or self.isconsonant(letter): #once we hit a character of a different type, put it back on the stack
                    letterstack.append(letter)
                else:
                    return ""
                break
        return collectletters
    
    #take a word and spell it a friendly way. Returns a structure containing the respelled word and the map to get back.
    #for OS, this means dealing with 'u's. For ON, it means dealing with some glides.
    def _normalize(self,word):
        backmap=[word,-1,0,""]
        trans=""
        length = len(word)
        if length==0: return backmap

        #Old Norse - deal with 'ia' or 'ja' appropriately
        if self.language=="on":
            if self.codamax:
                fromstr="ja"; tostr="ia" #this part is nonsense; the real thing is unimplemented. kept here as placeholder
            else:
                #find an i-vowel combination if there is one
                start=word.find('i')
                if start > 0 and len(word) > start+1:
                    if self.isvowel(word[start+1]):
                        trans=word[:start] + 'j' + word[start+1:]
                        backmap=[trans,start,1,'i']


        #now test for 'uuu' -> 'wu'
        start=word.find("uuu")
        if start > -1:
            trans=word[:start] + "wu" + word[start+3:]
            backmap=[trans,start,2,"uuu"] #=translated word, start of excision, how many chars to excise, what to replace them with
                
        else:
            #now look for 'uu' -> 'w'
            start=word.find("uu")
            if start > -1:
                #first check to see if a consonant follows
                if length>start and self.isconsonant(word[start+1]):
                    trans=word[:start] + "wu" + word[start+2:]
                    backmap=[trans,start,2,"uu"]
                        
                else:
                    trans=word[:start] + "w" + word[start+2:]
                    backmap=[trans,start,1,"uu"]
            else:
                #finally, look for intervocalic 'u' -> 'v'
                start=word.find("u")
                if start > 0:
                    if self.isvowel(word[start-1]) and length>start+1:
                        if self.isvowel(word[start+1]):
                            trans=word[:start] + "v" + word[start+1:]
                            backmap=[trans,start,1,"u"]
                else:
                    return backmap
        return backmap

    #do the reverse of _normalize but now in the syllable domain
    def _mapback(self,backmap,syllables):
        #if nothing was translated, move on; otherwise, un-respell
        locus=backmap[1]
        if locus > -1:
            i=0
            while i < len(syllables):
                syllTxt=syllables[i][0]
                syllLen=len(syllTxt) #length in chars of the current syllable
                if locus > syllLen-1: #the locus is in a later syllable
                    locus -= syllLen
                    i += 1
                else: #we've got the syllable that needs respelling
                    replacement=backmap[3]
                    gap=backmap[2]
                    newTxt=syllTxt[:locus] + replacement + syllTxt[locus+gap:]
                    syllables[i][0]=newTxt
                    break
        return syllables

    #return the onset symbol of a string (word or syllable)
    def allitSymbol(self,str, normalize=False):
        if str=="": return ""
        if normalize==True:
            str=self._normalize(str)

        allit = None
        try: firstletter=str[0][0].capitalize()
        except: return ""
        if len(str[0])>1: 
            secondletter=str[0][1].capitalize()

        if self.isvowel(firstletter):
            allit="Ø" #vocalic onset
            
        elif firstletter=="S" and len(str[0])>1:
            if secondletter=="P":
                allit="SP"
            elif secondletter=="T":
                allit="ST"
            elif secondletter=="C" or secondletter=="K":
                allit="SK"
            else:
                allit="S"
        elif firstletter=="T" and len(str[0])>1:
            if secondletter=="H":
                allit="Þ"
            else:
                allit="T"
        else:
            if firstletter in "CĊKQ": 
                allit="K"
            elif firstletter in "GĠJ": 
                allit="G"
            elif firstletter == "Ð":
                allit="Þ"
            else:
                allit=firstletter
        return allit

    #takes a word and returns an array of syllables and their mora counts
    def _sylbreaker(self, word, codamax=False, syllables=[], recursion=False):
        VOWELS=0
        CONSONANTS=1
        currentsyl=""
        moras=0
        weight=""
        letters=[]
        if not recursion: syllables.clear()

        if word == "": return [] 

        Vs="" #string of vowels
        Cs="" #string of consonants

        #put the letters in a stack
        for letter in word[::-1]: letters.append(letter) 
        #If there's a consonant onsent, let's get it out of the way 
        if self.isconsonant(letters[-1]): #peek at the first letter (last item on the stack)
            Cs = self._collectletters(letters, CONSONANTS)
            #all the consonants in the onset belong to the syllable by definition. No mora count.
            currentsyl += Cs

        #gotta have some vowels
        if len(letters)>0:
            Vs = self._collectletters(letters, VOWELS)
                #all the vowels in the cluster belong to the syllable as well. Look at the first vowel for length. 
            if len(Vs)>0:
                currentsyl += Vs
                moras += 1 + self.vowellength(Vs[0])
                
            #if we are at the end of the word, then the syllable is complete
            if len(letters)==0:
                weight=self.syllweight(moras)
                syllables.append([currentsyl, moras, weight])
                return syllables

            else: #there must be some consonants
                if len(letters)>0:
                    Cs = self._collectletters(letters, CONSONANTS)
                else:
                    Cs=""

                #if we are at the end of the word, then the syllable is complete
                if len(letters)==0:
                    currentsyl += Cs
                    moras += len(Cs)
                
                    weight=self.syllweight(moras)
                    syllables.append([currentsyl, moras, weight])
                    
                    return syllables
                

                #otherwise, we need to divide up the string of consonants between this syllable and the next.
                #in priority order, a syllable should start with a consonant; short syllables should be closed;
                #and syllable breaks should occur before the least sonorous consonant. Unless coda maximalization
                elif len(Cs)>0:
                    if self.codamax:
                        currentsyl +=Cs
                        moras += len(Cs)
                        syllables.append([currentsyl,moras,weight])
                    else:
                        if len(Cs) == 1: #the onset requirement assigns a single consonant to the following syllable
                            weight=self.syllweight(moras)
                            syllables.append([currentsyl, moras, weight])
                            
                        else: 
                            if moras < 2: #close a syllable with a short vowel when possible
                                cons=Cs[0]
                                currentsyl +=cons
                                moras += 1
                                Cs=Cs[1:]
                                # don't split up long (double) consonants
                                if len(Cs)>0:
                                    if Cs[0]==cons:
                                        currentsyl +=Cs[0]
                                        moras +=1
                                        Cs=Cs[1:]
                                    
                            #find the least sonorous consonant
                            i=0; lowIdx=0; son=0; low=10
                            while i<len(Cs):
                                son=self.sonority(Cs[i])
                                if son <= low: 
                                    low=son
                                    lowIdx=i
                                i += 1
                                
                            #add everything before the least sonorous consonant to the current syllable. This may be nothing.
                            currentsyl += Cs[:lowIdx-1]
                            moras += lowIdx
                            weight=self.syllweight(moras)
                            syllables.append([currentsyl, moras, weight])
                        

                    #send the rest of the word on for further syllable breaking
                    if len(currentsyl)<len(word):
                        return self._sylbreaker(word[len(currentsyl):],self.codamax,syllables, True)
                    
                    else:
                        return syllables
        else:
            return syllables

    #this is the public function to take a word and return a list of annotated syllables
    def break_word(self,word):
        if len(word)>0:
            #first, we're going to "normalize" the spelling of the word
            #then get the list of syllables for the respelled word
            #then respell the syllables again to correspond with the original word spelling, if necessary
            translated = self._normalize(word)
            syllables = self._sylbreaker(translated[0])
            #now map them back
            syllables = self._mapback(translated, syllables)
        return syllables