import time
import re
import jieba
import gensim
import argparse

'''
# 去除常见标点
def removePunctuation(text):
    text = [i for i in text if i not in (' ',',','.','。','?','？','!','！','')]
    return text
'''
'''
def removePunctuation(query):
    rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    query = rule.sub('', query)
    return query
'''


# 去除标点、符号（只留字母、数字、中文)
def removePunctuation(text):
    query = []
    for s in text:
        if (re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", s)):
            query.append(s)
    return query


def get_sim(fo1,fo2,fo3):
    text1 = open(fo1, encoding='UTF-8').read()
    text2 = open(fo2, encoding='UTF-8').read()
    # jieba 进行分词
    text_cut1 = jieba.lcut(text1)
    text_cut1 = removePunctuation(text_cut1)
    # 去除标点符号
    text_cut2 = jieba.lcut(text2)
    text_cut2 = removePunctuation(text_cut2)
    text_cut = [text_cut1, text_cut2]
    # 检验分词内容，成功后可去掉
    print(text_cut)
    # corpora语料库建立字典
    dictionary = gensim.corpora.Dictionary(text_cut)
    # 对字典进行doc2bow处理，得到新语料库
    new_dictionary = [dictionary.doc2bow(text) for text in text_cut]
    num_features = len(dictionary)  # 特征数
    # SparseMatrixSimilarity 稀疏矩阵相似度
    similarity = gensim.similarities.Similarity('-Similarity-index', new_dictionary, num_features)
    text_doc = dictionary.doc2bow(text_cut1)
    sim = similarity[text_doc][1]
    file3 = open(fo3, 'w')
    print('%.2f' % sim, )
    print('文本相似度： %.2f' % sim,file=file3)
    file3.close()

if __name__ == '__main__':
    fo1 = input('请输入原始文件位置')
    fo2 = input('请输入对比文件位置')
    fo3 = input('请输入答案位置')
    start = time.time()
    get_sim(fo1,fo2,fo3)
    end = time.time()
    print('运行时间: %s 秒' % (end - start))