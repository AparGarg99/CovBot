from cfg import Config
from collections import Counter
from imblearn.over_sampling import SMOTE
from joblib import dump, load
from keras.layers import Conv1D, MaxPool1D, GlobalMaxPooling1D, Dropout, Dense 
from keras.layers import Conv2D, MaxPool2D, Flatten, LSTM, TimeDistributed, LayerNormalization
from keras.models import load_model
from keras.models import Sequential
from numpy import set_printoptions
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import MidTermFeatures as aF
from pydub import AudioSegment
from pydub.silence import split_on_silence
from python_speech_features import logfbank
from python_speech_features import mfcc
from scikitplot.metrics import plot_cumulative_gain
from scikitplot.metrics import plot_lift_curve
from scipy.io import wavfile
from scipy.io.wavfile import write
from scipy.stats import entropy
from sklearn import preprocessing
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import VarianceThreshold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.metrics import RocCurveDisplay
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils import compute_class_weight
from tensorflow.keras.callbacks import ModelCheckpoint,CSVLogger,EarlyStopping
from tqdm import tqdm
import glob
import IPython.display as ipd
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pickle
import pywt
import re
import scikitplot as skplt
import seaborn as sns
import sounddevice
import statistics
import time
import warnings
warnings.filterwarnings("ignore")