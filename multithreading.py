import parselmouth
from glob import glob
from multiprocessing import Pool, cpu_count
from time import time
import matplotlib.pyplot as plt


def get_mean_pitch(filename):
    try:
        pitch = parselmouth.Sound(filename).to_pitch()
        mean_pitch = parselmouth.praat.call(pitch, "Get mean", 0, 0, "Hertz")
    except:
        mean_pitch = 0
    return mean_pitch


def get_formants(filename):
    formant_path_object = parselmouth.praat.call(parselmouth.Sound(filename),
                                                 "To FormantPath (burg)",
                                                 0.0025,
                                                 5.5,
                                                 5500,
                                                 0.025,
                                                 50,
                                                 0.05,
                                                 4)

    # Extract the Praat Formant Object from the Formant Path Object
    formant_object = parselmouth.praat.call(formant_path_object, "Extract Formant")
    formants = [parselmouth.praat.call(formant_object, "Get mean", fn, 0, 0, "hertz") for fn in range(1,5)]
    return formants


if __name__ == '__main__':
    sound_filenames = sorted(glob("/all_vowels/*.wav"))
    timediffs = []
    time1s = []
    time2s = []
    x =  range(0, len(sound_filenames), 250)
    cpus = cpu_count()
    print(f"{cpus = }")
    for i in x:
        sound_filenames = sorted(glob("/all_vowels/*.wav"))
        sound_filenames = sound_filenames[:i]
        pool = Pool(cpus)
        start1 = time()
        results = pool.map(get_formants, sound_filenames)
        time1 = time() - start1
        start2 = time()
        results = [get_formants(filename) for filename in sound_filenames]
        time2 = time() - start2
        timediffs.append(time2 - time1)
        time1s.append(time1)
        time2s.append(time2)

    number_of_voices = x
    plt.scatter(number_of_voices, time1s, label="Multiprocessing")
    plt.scatter(number_of_voices, time2s, label="Single Process")
    plt.xlabel("Number of wav files measured")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.title('Multiprocessing formant measurements')
    plt.show()
