from utils     import *
from mydicts   import *
from myschemas import *

def getchichar(request,char):
    cdict_name = request.request.get('dict_name', CHICHARDICT)
    chichars_query = Chichar.query(Chichar.chichar == char)
    qresult = chichars_query.fetch(1)
    if len(qresult) > 0:
        return qresult[0]
    return None

def getallchichars(request):
    dict_name      = request.request.get('dict_name',CHICHARDICT)
    chichars_query = Chichar.query(ancestor=dict_key(dict_name)).order(-Chichar.date)
    chichars       = chichars_query.fetch()
    return chichars

def getallsentences(request):
    sdict_name      = request.request.get('dict_name',SENTENCEDICT)
    sentences_query = Sentence.query(ancestor=dict_key(sdict_name))
    sentences       = sentences_query.fetch()
    return sentences


def getsentence(request,chi):
    sdict_name = request.request.get('dict_name', SENTENCEDICT)
    sentences_query = Sentence.query(Sentence.chichar == chi)
    qresult = sentences_query.fetch(1)
    if len(qresult) > 0:
        return qresult[0]
    return None

def getword(request,chi):
    sdict_name = request.request.get('dict_name', WORDDICT)
    words_query = Word.query(Word.chichar == chi)
    qresult = words_query.fetch(1)
    if len(qresult) > 0:
        return qresult[0]
    return None

def getsentencechichars(request,sentence):
    return charsentence2chichars(request,sentence.chichar)

def getwordchichars(request,word):
    return charsentence2chichars(request,word.chichar)

def addchichar(request,chi,translation,pronunciation):
    sdict_name = request.request.get('dict_name', CHICHARDICT)
    ochichar = Chichar(parent=dict_key(sdict_name));
    ochichar.chichar        = chi
    ochichar.translation    = translation
    ochichar.pronunciation  = pronunciation
    ochichar.put()
    return ochichar

def addsentence(request,chi,translation,pronunciation):
    sdict_name = request.request.get('dict_name', SENTENCEDICT)
    osentence = Sentence(parent=dict_key(sdict_name));
    osentence.chichar        = chi
    osentence.translation    = translation
    osentence.pronunciation  = pronunciation
    osentence.put()
    return osentence

def addword(request,chi,translation,pronunciation):
    sdict_name = request.request.get('dict_name', WORDDICT)
    oword = Word(parent=dict_key(sdict_name));
    oword.chichar        = chi
    oword.translation    = translation
    oword.pronunciation  = pronunciation
    oword.put()
    return oword


def asciitoremove():
    return [""," ","\n","\t",",",".","!","4","?"]

def sentence2chars(charstring):
    chars  = lsubstract(list(charstring.strip()),     asciitoremove())
    return chars

def sentence2pinyins(charstring):
    pinyins  = lsubstract(list(charstring.strip()),     asciitoremove())
    return pinyins


def charsentence2chichars(request,charstring):
    result = []
    for char in sentence2chars(charstring):
        chichar = getchichar(request,char)
        if chichar != None:
            result.append(chichar)
    return result

def chars2pinyins(request,chars):
    result = []
    for char in chars:
        chichar = getchichar(request,char)
        if chichar != None:
            result.append(chichar.pronunciation)
        else:
            result.append("TODO")
    return result


def checkaddchar(request,char,translation,pronunciation):
    char          = char.strip()
    if translation:
        translation   = translation.strip()
    if pronunciation:
        pronunciation = pronunciation.strip()
    ochichar = getchichar(request,char)
    if ochichar == None:
        request.response.write("need to add " + char)
        result = addchichar(request,char,translation,pronunciation)
    else:
        # TODO:check everything is the same  
        request.response.write("char " + char + " already known")
        result = ochichar
    return result

def checkaddsentence(request,chi,translation,pronunciation):
    osentence = getsentence(request,chi)

    if osentence == None:
        chars  = sentence2chars(chi.strip())
        pinyins = iff( pronunciation.strip() == "TODO", chars2pinyins(request,chars), sentence2pinyins(pronunciation))

        if not (len(chars) == len(pinyins)):
            request.response.write("<div>  error matching char " + "@".join(chars) + " pynyin " + "@".join(pinyins) + "</div>\n")
            result = None
        else:
            request.response.write("need to add sentence " + chi)
            result = addsentence(request,chi,translation,pronunciation)
            for (char,pinyin) in zip(chars,pinyins):
                chichar = checkaddchar(request,char,None,pinyin)
    else:
        request.response.write("sentence " + chi + " already known")
        result = osentence

    return result

def checkaddword(request,chi,translation,pronunciation):
    oword = getword(request,chi)

    if oword == None:
        chars  = sentence2chars(chi.strip())
        pinyins = iff( pronunciation.strip() == "TODO", chars2pinyins(request,chars), sentence2pinyins(pronunciation))

        if not (len(chars) == len(pinyins)):
            request.response.write("<div>  error matching char " + "@".join(chars) + " pynyin " + "@".join(pinyins) + "</div>\n")
            result = None
        else:
            request.response.write("need to add word " + chi)
            result = addword(request,chi,translation,pronunciation)
            for (char,pinyin) in zip(chars,pinyins):
                chichar = checkaddchar(request,char,None,pinyin)
    else:
        request.response.write("word " + chi + " already known")
        result = oword

    return result

def allocatedata(request,chichar,translation,pronunciation):
    result = None
    if len(chichar) == 1:
        # this is a new char
        result = checkaddchar(request,chichar,translation,pronunciation)
    else:
        if len(translation.split(" ")) > 1:
            # this is a sentence
            result = checkaddsentence(request,chichar,translation,pronunciation)
        else:
            result = checkaddword(request,chichar,translation,pronunciation)
    return result


def datatype(data):
    if not data:
        return None
    if isinstance(data,Chichar):
        return "Chichar"
    if isinstance(data,Sentence):
        return "Sentence"
    if isinstance(data,Word):
        return "Word"
    
