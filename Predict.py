import librosa
import soundfile
import numpy as np


def predictGivenFileName(filename):
    theta1 = np.loadtxt("Theta1.txt", delimiter=" ")
    theta2 = np.loadtxt("Theta2.txt", delimiter=" ")
    mu = np.loadtxt("mu.txt", delimiter=" ")
    sigma = np.loadtxt("sigma.txt", delimiter=" ")
    result = extract_feature(filename)
    for j in range(len(result)):
        result[j] -= mu[j]
        result[j] /= sigma[j]
    prediction = predict(theta1, theta2, result)
    return prediction


def extract_feature(file_name):
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        stft = np.abs(librosa.stft(X))
        result = np.array([])

        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
        result = np.hstack((result, mfccs))

        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
        result = np.hstack((result, chroma))

        mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T, axis=0)
        result = np.hstack((result, mel))

        return result


def predict(theta1, theta2, example):
    theta1 = np.transpose(theta1)
    theta2 = np.transpose(theta2)
    c = np.hstack((np.ones(2), example))
    h1 = sigmoid(multiply_matrices(c, theta1))
    c = np.hstack((np.ones(1), h1))
    h2 = sigmoid(multiply_matrices(c, theta2))
    pred = np.argmax(h2, axis=0)
    return pred


def multiply_matrices(mat1, mat2):
    return np.dot(mat1, mat2)


def sigmoid(example):
    z = 1/(1 + np.exp(-example))
    return z
