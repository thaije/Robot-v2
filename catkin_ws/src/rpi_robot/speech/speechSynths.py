import subprocess



def espeak(text):
    subprocess.call('espeak '+text, shell=True)
