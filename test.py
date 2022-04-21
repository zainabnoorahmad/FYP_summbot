import spacy
from spacy import displacy
NER = spacy.load("en_core_web_sm")
raw_text=" European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices "
text1= NER(raw_text)

for word in text1.ents:
    print(word.text,word.label_)


#displacy.render(text1,style="ent")    
displacy.render(text1, jupyter=True, style='ent')