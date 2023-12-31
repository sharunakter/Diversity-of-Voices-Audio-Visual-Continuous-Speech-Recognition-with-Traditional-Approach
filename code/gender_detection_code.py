# -*- coding: utf-8 -*-
"""Gender_detection_code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RCbFS-TCAGtv-2US43QqNoZvrDRuf2s0
"""

# Commented out IPython magic to ensure Python compatibility.
import os
import csv
import librosa
import numpy as np
# %matplotlib inline
from glob import glob
import pandas as pd
import seaborn as sns
import librosa.display
from itertools import cycle
import IPython.display as ipd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import roc_curve
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import confusion_matrix, classification_report

header = 'chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
for i in range(1, 21):
    header += f' mfcc{i}'
header += ' label'
header = header.split()

ok from google.colab import drive
drive.mount('/content/drive')

data_path = "/content/drive/MyDrive/Thesis/Dataset"
file = open('data.csv', 'w', newline='')
with file:
    writer = csv.writer(file)
    writer.writerow(header)
words =[]
for file in os.listdir(data_path):
  words.append(file)
for g in words:
    for filename in os.listdir(f'{data_path}/{g}'):
        recording = f'{data_path}/{g}/{filename}'
        y, sr = librosa.load(recording, sr=48000,mono=True,dtype=np.float32)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        rms = librosa.feature.rms(y=y)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        to_append = f' {np.mean(chroma_stft)} {np.mean(rms)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
        for e in mfcc:
            to_append += f' {np.mean(e)}'
        to_append += f' {g}'
        file = open('data.csv', 'a', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(to_append.split())

data = pd.read_csv('/content/data.csv')

data.head()

le = preprocessing.LabelEncoder()
le.fit(data['label'])
s=le.transform(data['label'])
data['label']=s

y = data['label']
X = data.drop(['label'],1)

""")))))))))))))))))))))))))))"""

# count ploting of label column
import seaborn as sns
sns.set()
sns.countplot(data.label)
plt.show()

# visualization of MFCC
plt.figure(figsize=(25,10))
librosa.display.specshow(mfcc,
                      x_axis="time",
                       sr=sr)
plt.colorbar(format="%+2f")
plt.show()

"""**Female Audio visualization**"""

Audio_female = glob("/content/drive/MyDrive/Thesis/Dataset/female/1m5.7s - 1m10.7s (2jnM7ZYaXdo).mp3")

ipd.Audio(Audio_female[0])

y_female, srr = librosa.load("/content/drive/MyDrive/Thesis/Dataset/female/1m5.7s - 1m10.7s (2jnM7ZYaXdo).mp3")

pd. Series (y_female).plot(figsize=(10, 5))

color_pal = plt.rcParams ["axes.prop_cycle"].by_key ( ) ["color"]
pd. Series (y_female[30000:30500]).plot(figsize=(10, 5),
                lw=1,
                title='Raw Audio Zoomed In Example',
                color=color_pal[2])
plt.show()

D = librosa.stft(y_female)
S_db = librosa. amplitude_to_db(np.abs (D), ref=np.max)
S_db.shape

# Plot the transformed audio data
fig, ax = plt.subplots (figsize=(10, 5))
img= librosa.display.specshow (S_db,
                              x_axis='time',
                              y_axis='log',
                              ax=ax)
ax.set_title('Spectogram Example', fontsize=20)
fig.colorbar (img, ax=ax, format=f'%0.2f')
plt.show()

"""**Male Audio visualization**"""

Audio_male = glob("/content/drive/MyDrive/Thesis/Dataset/male/1 - Mohammad Sajid Miah.mp3")

ipd.Audio(Audio_male[0])

y_male, srr = librosa.load("/content/drive/MyDrive/Thesis/Dataset/male/1 - Mohammad Sajid Miah.mp3")

pd. Series (y_male).plot(figsize=(10, 5))

"""Third_Gender Audio Visualization"""

Audio_third_gender = glob("/content/drive/MyDrive/Thesis/Dataset/third_gender/Audio_0001.mp3")

ipd.Audio(Audio_third_gender[0])

y_third_gender, srr = librosa.load("/content/drive/MyDrive/Thesis/Dataset/third_gender/Audio_0001.mp3")

pd. Series (y_third_gender).plot(figsize=(10, 5))

color_pal = plt.rcParams ["axes.prop_cycle"].by_key ( ) ["color"]
y_trimmed, _ = librosa.effects.trim(y_third_gender, top_db=20)
pd. Series (y_trimmed).plot(figsize=(10, 5),
                    lw=1,
                    title='Raw Audio Trimmed Example',
                    color=color_pal[1])
plt.show()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=88)

""".

**Gboost**
"""

from sklearn.ensemble import GradientBoostingClassifier
Gb = GradientBoostingClassifier(n_estimators=1000, learning_rate=.1,max_depth=10, random_state=43).fit(X_train, y_train)

Gb.score(X_test, y_test)

Predicted_classes_Gb =Gb.predict(X_test)
from sklearn.metrics import accuracy_score
accuracy_score(y_test, Predicted_classes_Gb)

pred_LR = Gb.predict(X_test)
print(classification_report(y_test, Predicted_classes_Gb))

matrix = plot_confusion_matrix(Gb, X_test, y_test, cmap=plt.cm.Reds)
matrix.ax_.set_title('Confusion Matrix', color='white')
plt.xlabel('label', color='white')
plt.ylabel('True Label', color='white')
plt.gcf().axes[1].tick_params (colors='white')
plt.gcf().axes[0].tick_params (colors='white')
plt.gcf().set_size_inches (10,6)
plt.show()

""".

**RandomForest**
"""

from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(max_depth=10000,random_state=50).fit(X_train, y_train)
clf.score(X_test, y_test)

from sklearn.metrics import classification_report
import pandas as pd

predclf = clf.predict(X_test)
print(classification_report(y_test, predclf))

"""**Cross validation**"""

from sklearn.model_selection import cross_val_score
Scores_LR = cross_val_score(clf, X, y, cv = 10)

Scores_LR

"""KNN"""

from sklearn.neighbors import KNeighborsClassifier
KNN = KNeighborsClassifier(n_neighbors= 6, metric= 'minkowski', p = 1)
KNN.fit(X_train, y_train)
KNN.score(X_train, y_train)

pred_KNN = KNN.predict(X_test)
print(classification_report(y_test, pred_KNN))

from sklearn.svm import SVC # "Support vector classifier"
classifier = SVC(kernel='linear', random_state=0)
classifier.fit(X_train, y_train)
classifier.score(X_train, y_train)

pred_classifier = classifier.predict(X_test)
print(classification_report(y_test, pred_classifier))

classifier.score(X_train, y_train)

""".

**DecisionTree**
"""

from sklearn.tree import DecisionTreeClassifier

Dt = DecisionTreeClassifier()
Dt.fit(X_train, y_train)
Dt.score(X_test, y_test)

pred_Dt = Dt.predict(X_test)
print(classification_report(y_test, pred_Dt))

""".

**Naive Bayes**
"""

from sklearn.naive_bayes import GaussianNB
NB  = GaussianNB()
NB.fit(X_train, y_train)
NB.score(X_train, y_train)

pred_NB = NB.predict(X_test)
print(classification_report(y_test, pred_NB))

""".

XGBoost
"""

from xgboost import XGBClassifier
xgb = XGBClassifier()
xgb.fit(X_train,y_train)
predxgb = xgb.predict(X_test)
xgb.score(X_test, y_test)

print(classification_report(y_test, predxgb))

""".

**LR**
"""

from sklearn.linear_model import LogisticRegression
Lr = LogisticRegression()
Lr.fit(X_train, y_train)
Lr.score(X_train, y_train)

pred_LR = Lr.predict(X_test)
print(classification_report(y_test, pred_LR))

Predicted_classes_Lr = Lr.predict(X_test)
from sklearn.metrics import accuracy_score
accuracy_score(y_test, Predicted_classes_Lr)

Lr_prediction = Lr.predict(X_test)
confusion_matrix(y_test, Lr_prediction)

matrix = plot_confusion_matrix(Lr, X_test, y_test, cmap=plt.cm.Reds)
matrix.ax_.set_title('Confusion Matrix', color='white')
plt.xlabel('Predicted label', color='white')
plt.ylabel('label', color='white')
plt.gcf().axes[0].tick_params (colors='white')
plt.gcf().axes[1].tick_params (colors='white')
plt.gcf().set_size_inches (15,6)
plt.show()