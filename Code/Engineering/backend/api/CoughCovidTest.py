"""
    Single instance of cough covid-test
"""
import pickle
import os
import statistics
import numpy as np
import pandas as pd
import json
import librosa
import io
import array
import time
# from tensorflow.keras.models import load_model
from keras.models import load_model
from pydub import AudioSegment
from pydub.silence import split_on_silence
from python_speech_features import mfcc
from scipy.io.wavfile import read, write
from .CoughConfig import Config
# from StringIO import StringIO


class CoughCovidTest():

  def __init__(self):
    # Load the model
    base_path = os.getcwd()
    self.config = Config()
    
    model_path = os.path.join(base_path, 'models', 'conv')
    print('Loading cough model from model path: ', model_path)
    self.model = load_model(model_path)

    pass
  
  def segment(self, bytes_data):
    # AudioSegment document: https://github.com/jiaaro/pydub/blob/master/API.markdown
    # sound = AudioSegment(data=bytes_data, sample_width=2, channels=1, frame_rate=16000)
    # Issues: https://github.com/jiaaro/pydub/issues/145

    sound = AudioSegment.from_wav(io.BytesIO(bytes_data))
    audio_chunks = split_on_silence(sound, min_silence_len=200, silence_thresh=sound.dBFS-16)
    
    first_sample_array = audio_chunks[0].get_array_of_samples()
    sample = np.array(first_sample_array)
    return sample

  def envelope(self, y, rate, threshold):
    mask = []
    y = pd.Series(y).apply(np.abs)
    y_mean = y.rolling(window=int(rate/10), min_periods=1, center=True).mean()
    for mean in y_mean:
        if mean > threshold:
            mask.append(True)
        else:
            mask.append(False)
    return mask
  
  def build_predictions_cnn(self, wav, rate):

    config = self.config
    model = self.model

    # feature extraction and modeling
    y_pred = []
    max_range = min(wav.shape[0]-config.step, 1000)

    print('====> build_predictions max_range', wav.shape[0], config.step, max_range)

    for i in range(0, max_range):
        sample = wav[i:i+config.step] # choose sample of size config.step
        x = mfcc(sample, rate,
                numcep=config.nfeat, nfilt=config.nfilt, nfft=config.nfft)
        x = (x-config.min)/(config.max-config.min)

        x = x.reshape(1, x.shape[0], x.shape[1], 1)

        y_hat = model.predict(x)[0][0]

        y_pred.append(round(y_hat,0))

    # print('predict result', y_pred)
    
    if len(y_pred) == 0:
      return False
    
    fn_prob = int(statistics.mode(y_pred))

    return bool(fn_prob)

  
  def predict (self, raw_data=None, path=''):
    if raw_data is None and path is '':
      return None
    
    start = time.time()

    rate, wav = read(io.BytesIO(raw_data)) # numpy ndarray
    
    print('====> step1. start segment')
    cleaned_wav = self.segment(raw_data)
    
    print('====> step2. start envelope', rate)
    mask = self.envelope(cleaned_wav, rate, 0.0005)
    wav = cleaned_wav[mask]

    print('====> step3. do prediction')
    result = self.build_predictions_cnn(wav, rate)
    print('====> predict result: ', result)
    
    print('Time taken by model for inference:', time.time() - start, 'sec')
    
    return False


covid_test = CoughCovidTest()