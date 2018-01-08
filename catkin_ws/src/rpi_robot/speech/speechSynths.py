import subprocess



def espeak(text):
    subprocess.call('espeak '+text, shell=True)


def festival(text):
    subprocess.call('echo '+text + '|festival --tts', shell=True)


def flite(text):
    subprocess.call('flite -voice file://cmu_us_bdl.flitevox' + text)
