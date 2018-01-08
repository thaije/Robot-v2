
#Installation
- Install: `sudo apt-get install festival`
-Download voices from http://www.cstr.ed.ac.uk/downloads/festival/2.4/voices/ or http://www.speech.cs.cmu.edu/cmu_arctic/packed/ (for latter see https://ubuntuforums.org/showthread.php?t=677277)
- Uncompress and move voices to `/usr/share/festival/voices/us/`
- Edit `default-voice-priority-list` in `/usr/share/festival/voices.scm`
- Test with: `echo "Hello, how are you doing. I am doing fine."|festival --tts`

Nice voices:
- cmu_us_awb_cg (scottish male)
- cmu_us_axb_cg (scottish female)
- cmu_us_fem_cg (Arnold Schwarzenegger)
- cmu_us_slt_cg (clear female voice)
- cmu_us_clb_arctic_clunits (even clearer female voice)
- cmu_us_jmk_arctic_clunits (zwoele male voice)
- cmu_us_rms_arctic_clunits (clear but robotlike)
- Other voices: https://ubuntuforums.org/showthread.php?t=751169
