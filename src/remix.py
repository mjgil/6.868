from pyechonest import config
import echonest.remix.audio as audio

config.ECHO_NEST_API_KEY="UJGOWAOWXLAR4SBR9"


input_filename = "../music/orig/02 Justin Timberlake - Suit & Tie.mp3"
output_filename = "../music/processed/suitAndTie"
# change tempo

# change pitch

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

reverse_beats()
# extract_first_beat()