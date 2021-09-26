import parselmouth
from glob import glob
from multiprocessing import Pool
from multiprocessing import Process, Manager


sound_filenames = sorted(glob("/all_vowels/*.wav"))[:20]
sounds = []


def get_sound_object(L, filename):
    pitch = parselmouth.Sound(filename).to_pitch()
    mean_pitch = parselmouth.praat.call(pitch, "Get mean", 0, 0, "Hertz")
    L.append(mean_pitch)

if __name__ == '__main__':
    with Manager() as manager:
        L = manager.list()  # <-- can be shared between processes.
        processes = []
        for filename in sound_filenames:
            p = Process(target=get_sound_object, args=(L, filename))  # Passing the list
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
        print(L)
