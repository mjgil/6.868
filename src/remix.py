from pyechonest import config
from echonest.remix import audio,modify

config.ECHO_NEST_API_KEY="UJGOWAOWXLAR4SBR9"


input_filename = "../audio/sample/fifth_test3.wav"
output_filename = "../audio/processed/fifth_test3"
# change tempo

# change pitch
def shift_each_bar_semitones():
  soundtouch = modify.Modify()
  audiofile = audio.LocalAudioFile(input_filename)
  out_shape = (len(audiofile.data),)
  out_data = audio.AudioData(shape=out_shape, numChannels=1, sampleRate=44100)
  bars = audiofile.analysis.bars
  for i, bar in enumerate(bars):
    if (len(bar.children()) > 3):
      top = bar.children()[0]
      chord = bar.children()[1]
      root = bar.children()[2]
      middle = bar.children()[3]

      new_beat1 = soundtouch.shiftPitchSemiTones(audiofile[root], (i*2))
      out_data.append(new_beat1)

      new_beat2 = soundtouch.shiftPitchSemiTones(audiofile[middle], (i*2))
      out_data.append(new_beat2)

      new_beat3 = soundtouch.shiftPitchSemiTones(audiofile[top], (i*2))
      out_data.append(new_beat3)

      new_beat = audio.mix(new_beat1, new_beat3, 0.5)
      new_beat = audio.mix(new_beat, new_beat2, 0.66)
      out_data.append(new_beat)
  out_data.encode(output_filename + "EachBarShiftedSemiTones.mp3")

def shift_each_bar_arbitrary():
  soundtouch = modify.Modify()
  audiofile = audio.LocalAudioFile(input_filename)
  out_shape = (len(audiofile.data),)
  out_data = audio.AudioData(shape=out_shape, numChannels=1, sampleRate=44100)
  bars = audiofile.analysis.bars
  for i, bar in enumerate(bars):
    if (len(bar.children()) > 3):
      top = bar.children()[0]
      chord = bar.children()[1]
      root = bar.children()[2]
      middle = bar.children()[3]

      new_beat1 = soundtouch.shiftPitch(audiofile[root], ((i+1)*2)*0.1)
      out_data.append(new_beat1)

      new_beat2 = soundtouch.shiftPitch(audiofile[middle], ((i+1)*2)*0.1)
      out_data.append(new_beat2)

      new_beat3 = soundtouch.shiftPitch(audiofile[top], ((i+1)*2)*0.1)
      out_data.append(new_beat3)

      new_beat = audio.mix(new_beat1, new_beat3, 0.5)
      new_beat = audio.mix(new_beat, new_beat2, 0.66)
      out_data.append(new_beat)
  out_data.encode(output_filename + "EachBarShiftedArbitrary.mp3")

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
      new_beat = soundtouch.shiftPitchSemiTones(audiofile[beat], (i+1)*2)
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
# extract_first_beat_and_shift()
shift_each_bar_arbitrary()