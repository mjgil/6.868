from remixes import REMIXES

class Remix:
  def __init__(self, args):
    self.remix = REMIXES.get(args.chord_type, None)
    assert self.remix is not None, 'Chord Type Invalid'

    self.remix = self.remix(args)

  def run():
    self.remix.process()

# change tempo
def change_tempo():
    audiofile = audio.LocalAudioFile(input_filename)
    bars = audiofile.analysis.bars
    collect = []

    for bar in bars:
      if (len(bar.children()) > 3):
        bar_ratio = (bars.index(bar) % 4) / 2.0

        top = bar.children()[0]
        chord = bar.children()[1]
        root = bar.children()[2]
        middle = bar.children()[3]
        beats = [root, middle, top, chord]

        for i, beat in enumerate(beats):
          beat_index = i
          ratio = beat_index / 2.0 + 0.5
          ratio = ratio + bar_ratio 
          beat_audio = beat.render()
          scaled_beat = dirac.timeScale(beat_audio.data, ratio)
          ts = audio.AudioData(ndarray=scaled_beat, shape=scaled_beat.shape, 
                          sampleRate=audiofile.sampleRate, numChannels=scaled_beat.shape[1])
          collect.append(ts)

    out = audio.assemble(collect, numChannels=2)
    out.encode(output_filename + 'TempoChange.mp3')

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
  audio_file = audio.LocalAudioFile(input_filename)
  beats = audio_file.analysis.beats
  beats.reverse()
  audio.getpieces(audio_file, beats).encode(output_filename + "BeatReverse.mp3")

# reverse_beats()
# extract_first_beat()
# extract_first_beat_and_shift()
shift_each_bar_arbitrary()
# shift_each_bar_semitones()
# change_tempo()