import spacy
from spacy import displacy
NER = spacy.load("en_core_web_sm")
raw_text=" The Metaverse is an online virtual world that combines tech from augmented reality, virtual reality, 3D holographics (think: avatars), video, and other communication methods as an alternative world to coexist in. Facebook’s Mark Zuckerberg says that in 10 years, the Metaverse will be our new internet reality and available mainstream. Investors are spending millions, recently, on “virtual real estate” in the realms of Metaverse. "
text1= NER(raw_text)

for word in text1.ents:
    print(word.text,word.label_)


#displacy.render(text1,style="ent")    
displacy.render(text1, jupyter=True, style='ent')