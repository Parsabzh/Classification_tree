import os
import glob
from sklearn.base import _pprint
from sklearn.linear_model import LogisticRegression
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn import preprocessing
import numpy as np


def create_dataset():
    # path=r"C:\Users\Parsa\Desktop\University\Data Mining\Project\Classification_treev3\Classification_tree\op_spam_v1.4\op_spam_v1.4\negative_polarity"
    dirname = os.path.dirname(__file__)
    path= os.path.join(dirname, r"op_spam_v1.4/op_spam_v1.4/negative_polarity")
    n=1
    df = pd.DataFrame(columns=['class','comment','type', 'filename'])
    # find deceptive comment in dataset and give type(test or train) to it 
    while n<6:
        lst_comment=[]
        lst_class=[]
        lst_type=[]
        lst_file=[]

        for child in os.scandir(path):
            if 'deceptive' in child.path:

                    for file in os.listdir(child.path+r'/fold{}'.format(n)):
                        if file.endswith(".txt"):
                            with open(child.path+r'/fold{}'.format(n)+"/"+file) as f:
                                lines=f.read()
                                lst_comment.append(lines)
                                lst_class.append('deceptive')
                                lst_file.append(file)
        lst_type.clear()    
        if n==5:
            for i in range(len(lst_class)):
                lst_type.append("test")
            # dt=pd.DataFrame(pd.DataFrame({'class':lst_class,'comment':lst_comment,'type':lst_type}))
            df = pd.concat((df, pd.DataFrame({'class':lst_class,'comment':lst_comment,'type':lst_type, 'filename':lst_file})))
        else:
            
            for i in range(len(lst_class)):
                lst_type.append("train")
            # dt=pd.DataFrame(pd.DataFrame({'class':lst_class,'comment':lst_comment,'type':lst_type}))
            df = pd.concat((df, pd.DataFrame({'class':lst_class,'comment':lst_comment,'type':lst_type, 'filename':lst_file})))

        n=n+1
    n=1
    
    # find truthful comment in dataset and give type(test or train) to it
    while n<6:
        lst_comment=[]
        lst_class=[]
        lst_type=[]
        lst_file=[]

        for child in os.scandir(path):
            if 'truthful' in child.path:
                    for file in os.listdir(child.path+r'/fold{}'.format(n)):
                        if file.endswith(".txt"):
                            with open(child.path+r'/fold{}'.format(n)+"/"+file) as f:
                                lines=f.read()
                                lst_comment.append(lines)
                                lst_class.append('truthful')
                                lst_file.append(file)
   
        lst_type.clear()
        if n==5:
            for i in range(0,len(lst_class)):
                lst_type.append("test")
            # dt=pd.DataFrame(pd.DataFrame({'class':lst_class,'comment':lst_comment,'type':lst_type}))
            df = pd.concat((df, pd.DataFrame({'class':lst_class,'comment':lst_comment,'type':lst_type, 'filename':lst_file})))

        else:
            for i in range(0,len(lst_class)):
                lst_type.append("train")
            # dt=pd.DataFrame(pd.DataFrame({'class':lst_class,'comment':lst_comment,'type':lst_type}))
            df = pd.concat((df, pd.DataFrame({'class':lst_class,'comment':lst_comment,'type':lst_type, 'filename':lst_file})))


        n=n+1
    return df.reset_index()

def vectorize(dt):
    #vectorize feactures and labels to change the text to the number
    
    vectorizer = CountVectorizer(min_df=5, encoding='latin-1', ngram_range=(1, 2), stop_words='english')

    vec = vectorizer.fit_transform(dt['comment']).toarray()#.astype(np.float32)

    vectorized = pd.DataFrame(data=vec, columns=vectorizer.get_feature_names_out())

    vectorized.insert(0, 'class_label', dt['class'])
    vectorized.insert(1, 'set_type', dt['type'])
    vectorized.insert(2, 'original_file', dt['filename'])

    return vectorized



# dt = create_dataset()

# dt.to_csv('original.csv')


dt = pd.read_csv('original.csv')
dt = vectorize(dt)

dt['class_label'] = dt['class_label'].transform(lambda x: 0 if x == 'deceptive' else 1)

dt = dt.drop(['original_file'], axis=1)

print(dt.head)
dt.to_csv('converted.csv')

X_train = dt.loc[dt['set_type'] == 'train', ~dt.columns.isin(['class_label', 'set_type'])]
y_train = dt.loc[dt['set_type'] == 'train', dt.columns.isin(['class_label'])]

X_test = dt.loc[dt['set_type'] == 'test', ~dt.columns.isin(['class_label', 'set_type'])]
y_test = dt.loc[dt['set_type'] == 'test', dt.columns.isin(['class_label'])]

print(y_test)



print(len(dt))




# x_train=dt_train['comment']
# y_train=dt_train['class']
# lr=LogisticRegression(penalty="l2")
# lr.fit(x_train,y_train)
# print(lr.score())

