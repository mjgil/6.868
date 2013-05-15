from pyechonest import config
from echonest.remix import audio,modify

config.ECHO_NEST_API_KEY="UJGOWAOWXLAR4SBR9"


input_filename = "../audio/sample/fifth.mp3"
output_filename = "../audio/processed/fifth"
# change tempo

# change pitch
def extract_first_beat_and_shift():
  soundtouch = modify.Modify()
  audiofile = audio.LocalAudioFile(input_filename)
  out_shape = ((len(audiofile.data)/4),)
  out_data = audio.AudioData(shape=out_shape, numChannels=1, sampleRate=44100)
  bars = audiofile.analysis.bars
  for i, bar in enumerate(bars):
      beat = bar.children()[0]
      print i
      print beat.local_context()
      print beat
      new_beat = soundtouch.shiftPitchSemiTones(audiofile[beat], i*2)
      out_data.append(new_beat)
  out_data.encode(output_filename + "FirstBeatShifted.mp3")

# change loudness

# change melody - arrangement of notes

# change rhythm recurring pattern or beat
def extract_first_beat():
  audiofile = audio.LocalAudioFile(input_filename)
  bars = audiofile.analysis.bars
  collect = audio.AudioQuantumList()
  for bar in bars:
      collect.append(bar.children()[0])
  out = audio.getpieces(audiofile, collect)
  out.encode(output_filename + "FirstBeat.mp3")

def reverse_beats():
  """Reverse a song by playing its beats forward starting from the end of the song"""

  # Easy around wrapper mp3 decoding and Echo Nest analysis
  audio_file = audio.LocalAudioFile(input_filename)

  # You can manipulate the beats in a song as a native python list
  beats = audio_file.analysis.segments
  beats.reverse()

  # And render the list as a new audio file!
  audio.getpieces(audio_file, beats).encode(output_filename + "Segreverse.mp3")

# reverse_beats()
# extract_first_beat()
extract_first_beat_and_shift()