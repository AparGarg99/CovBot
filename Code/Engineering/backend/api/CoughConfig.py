import os

class Config:
    def __init__(self, mode='conv', nfilt=26, nfeat=13, nfft=512, rate=16000):
        base_path = os.getcwd()

        self.mode = mode
        self.nfilt = nfilt
        self.nfeat = nfeat
        self.nfft = nfft
        self.rate = rate
        self.step = int(rate/10)
        self.min = -84.38018560007893
        self.max = 62.979127432635984
        # self.model_path = os.path.join(base_path, 'models', mode + '.model')
        # self.p_path = os.path.join(base_path, 'models', mode + '.p')


# Audio chunk size = 1/10 sec = 1/10 * 16000 samples = 1600 samples
# nfft (frame size) = 25 ms = 0.025 * 16000 samples = 400 samples (we add 112 samples with padding to make it 512 which is nearest power of 2)
# STFT using 25 ms frames
# MFCC from STFT