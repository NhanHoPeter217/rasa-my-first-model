import spacy
nlp = spacy.load("vi_core_news_lg")
doc = nlp("chứng chỉ yêu cầu những tài liệu gì?")
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)