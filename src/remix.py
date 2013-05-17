import os
import statics
import dirac
import random
from pyechonest import config
from echonest.remix import audio,modify
config.ECHO_NEST_API_KEY="UJGOWAOWXLAR4SBR9"
REMIXES = {}

def is_number(s):
  try:
      float(s)
      return True
  except ValueError:
      return False


class BaseRemix(object):
  def __init__(self, args):
    self.input_file = os.path.join(
      statics.input_path, args.chord_type, args.base_chord_type) + '.wav'

    print self.input_file
    assert os.path.exists(self.input_file), 'Chord Music File Does Not Exist'
    self.remix_amount = args.remix_amount or random.random()
    assert is_number(self.remix_amount), 'Remix Amount Must Be A Number'
    self.remix_amount = float(self.remix_amount)
    assert (0.0 <= self.remix_amount <= 1.0), 'Remix Amount Must Be Between 0 and 1'

    self.remix_type = args.remix_type
    self.output_folder = os.path.join(statics.output_path, args.chord_type, args.base_chord_type)
    print self.output_folder
    if not os.path.exists(self.output_folder):
      os.makedirs(self.output_folder)

    remix_str = '%.2f' % self.remix_amount
    output_file_name = "_".join([args.remix_type, remix_str]) + '.mp3'
    self.output_file = os.path.join(self.output_folder, output_file_name)

    print self.output_file

  def process(self):
      fn = getattr(self, self.remix_type)
      assert hasattr(fn, '__call__'), 'Invalid Remix Type'
      fn()

  def change_tempo(self):
      raise NotImplementedError

  def one_note_pitch_shift(self):
      raise NotImplementedError

  def all_notes_pitch_shift(self):
      raise NotImplementedError

class ThreeNoteRemix(BaseRemix):
  Name = "three_note"
  def __init__(self, args):
    super(ThreeNoteRemix, self).__init__(args)


  def change_tempo(self):
    audiofile = audio.LocalAudioFile(self.input_file)
    bars = audiofile.analysis.bars
    collect = []

    for bar in bars:
      if (len(bar.children()) > 3):

        top = bar.children()[0]
        chord = bar.children()[1]
        root = bar.children()[2]
        middle = bar.children()[3]
        beats = [root, middle, top, chord]

        for i, beat in enumerate(beats):
          ratio = self.remix_amount + 0.5
          beat_audio = beat.render()
          scaled_beat = dirac.timeScale(beat_audio.data, ratio)
          ts = audio.AudioData(ndarray=scaled_beat, shape=scaled_beat.shape, 
                          sampleRate=audiofile.sampleRate, numChannels=scaled_beat.shape[1])
          collect.append(ts)

    out = audio.assemble(collect, numChannels=2)
    out.encode(self.output_file)

  def one_note_pitch_shift(self):
    soundtouch = modify.Modify()
    audiofile = audio.LocalAudioFile(self.input_file)
    out_shape = (len(audiofile.data),)
    out_data = audio.AudioData(shape=out_shape, numChannels=1, sampleRate=44100)
    bars = audiofile.analysis.bars
    random_index = random.randrange(0,3)
    for i, bar in enumerate(bars):
      if (len(bar.children()) > 3):
        top = bar.children()[0]
        chord = bar.children()[1]
        root = bar.children()[2]
        middle = bar.children()[3]

        beats = [root, middle, top]
        beat_list = []
        for j, beat in enumerate(beats):
          shift_ratio = self.remix_amount
          if j == random_index:
            shift_ratio = shift_ratio * random.random()
          new_beat = soundtouch.shiftPitch(audiofile[beat], shift_ratio)
          out_data.append(new_beat)
          beat_list.append(new_beat)

        new_beat = audio.mix(beat_list[0], beat_list[1], 0.5)
        new_beat = audio.mix(new_beat, beat_list[2], 0.66)
        out_data.append(new_beat)
    out_data.encode(self.output_file)

  def all_notes_pitch_shift(self):
    soundtouch = modify.Modify()
    audiofile = audio.LocalAudioFile(self.input_file)
    out_shape = (len(audiofile.data),)
    out_data = audio.AudioData(shape=out_shape, numChannels=1, sampleRate=44100)
    bars = audiofile.analysis.bars
    for i, bar in enumerate(bars):
      if (len(bar.children()) > 3):
        top = bar.children()[0]
        chord = bar.children()[1]
        root = bar.children()[2]
        middle = bar.children()[3]


        beats = [root, middle, top]
        beat_list = []
        for j, beat in enumerate(beats):
          shift_ratio = self.remix_amount
          new_beat = soundtouch.shiftPitch(audiofile[beat], shift_ratio)
          out_data.append(new_beat)
          beat_list.append(new_beat)

        new_beat = audio.mix(beat_list[0], beat_list[1], 0.5)
        new_beat = audio.mix(new_beat, beat_list[2], 0.66)
        out_data.append(new_beat)
    out_data.encode(self.output_file)

class FourNoteRemix(BaseRemix):
  Name = "four_note"
  def __init__(self, args):
    super(FourNoteRemix, self).__init__(args)


  def change_tempo(self):
      raise NotImplementedError

  def one_note_pitch_shift(self):
      raise NotImplementedError

  def all_notes_pitch_shift(self):
      raise NotImplementedError

for remix in BaseRemix.__subclasses__():
    REMIXES[remix.Name] = remix

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