import pandas as pd

from gensim import corpora, models, similarities
from gensim.models.coherencemodel import CoherenceModel
import jieba
import jieba.analyse
import re


class CutMessage():
    def __init__(self, dic_path):
        jieba.load_userdict(dic_path)
        self.sw = self.loadstopwords()

    def loadstopwords(self):
        f_stop = open("/Users/casfive-public/CasfiveProject/08短信营销/stopwords.txt")
        sw = [line.strip() for line in f_stop]
        f_stop.close()
        return sw

    def leaveword(self, text):
        text = re.sub('[^\u4e00-\u9fa5]', ',', str(text))  # 去除所有的非汉字，如英文、数字和标点符号
        return text.strip()

    def cutsegment(self, line):
        line = self.leaveword(",".join(jieba.cut(line, cut_all=False))).split(",")
        return [i for i in line if (len(i) > 1 and i not in self.sw)]


class TrainTestLDA():
    def __init__(self, dic_path):
        self.ct = CutMessage(dic_path)

    def initdata(self, input_data_path, output_data_path):
        #输入数据分词，再去停止词，保存
        sms = pd.read_excel(input_data_path, usecols=['messages'])
        cut_res = []

        with open(output_data_path, 'w', encoding='utf-8') as f:
            for sm in sms['messages']:
                # print(sm)
                if "验证码" in sm:
                    continue
                else:
                    sm = self.ct.cutsegment(sm)
                    cut_res.append(sm)
                    for i in sm:
                        f.write(i + ',')
                    f.write("\n")

    def reloaddata(self, datapath):
        filelist = []
        with open(datapath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            filelist.append([i for i in line.split(',') if len(i) > 1])
        return filelist

    def prepare_lda(self, data, model_save_path):
        self.model_save_path = model_save_path
        self.dictionary = corpora.Dictionary(data)
        self.dictionary.save(self.model_save_path + "dictory.dict")
        self.corpus = [self.dictionary.doc2bow(text) for text in data]
        self.datalenth = len(data)
        corpora.MmCorpus.serialize(self.model_save_path + 'sms.mm', self.corpus)
        return self.dictionary, self.corpus

    def train_lda(self, topic_num):
        corpusTfidf = models.TfidfModel(self.corpus)[self.corpus]
        alpha = round(1 / topic_num, 4)
        self.ldam = models.LdaModel(corpusTfidf, num_topics=topic_num, id2word=self.dictionary, alpha=alpha, eta=0.01,
                                    minimum_probability=0.001, update_every=0, chunksize=int(self.datalenth * 0.8),
                                    passes=1, random_state=51)
        self.ldam.save(self.model_save_path + "ldamodel.model")
        return self.ldam

    def get_scores(self, c_type='u_mass', data="-"):
        #lda分类效果用主题连贯性评价
        if c_type == "u_mass":
            ldac = CoherenceModel(model=self.ldam, corpus=self.corpus, dictionary=self.dictionary, coherence='u_mass')
        elif c_type == "c_v":
            ldac = CoherenceModel(model=self.ldam, texts=data, dictionary=self.dictionary, coherence='c_v')
        return ldac.get_coherence()

    def reload_model(self, model_path="_"):
        if model_path == "_":
            model_path = self.model_save_path
        self.ldam = models.ldamodel.LdaModel.load(model_path + "ldamodel.model")
        self.dictionary = corpora.Dictionary.load(model_path + "dictory.dict")
        self.corpus = corpora.MmCorpus(model_path + "sms.mm")
        return {"model": self.ldam, "dictionary": self.dictionary, "corpus": self.corpus}

    def predict_terms(self, term):
        bow_vector = self.dictionary.doc2bow(term)
        return self.ldam[bow_vector]

if __name__ == "__main__":
    #ldamodel init
    dic_path = "/"
    m_save_path = "/"
    input_data_path = "/"
    output_data_path = "/"

    lda_handle = TrainTestLDA(dic_path)
    lda_handle.initdata(input_data_path=input_data_path, output_data_path=output_data_path)
    dataset = lda_handle.reloaddata(output_data_path)
    dictionary, corpus = lda_handle.prepare_lda(dataset, m_save_path)
    lda_model = lda_handle.train_lda(20)
    lda_score = lda_handle.get_scores("c_v", dataset)
