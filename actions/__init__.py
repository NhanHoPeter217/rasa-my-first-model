import spacy
nlp = spacy.load("vi_core_news_lg")
doc = nlp("Nếu không đủ điểm bậc B1 thì có được nhận bậc A1, A2 không?. Tôi là Hồ Thanh Nhân")
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)