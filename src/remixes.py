import os
import statics
import dirac
import random
from pyechonest import config
from echonest.remix import audio,modify
config.ECHO_NEST_API_KEY="UJGOWAOWXLAR4SBR9"
REMIXES = {}


class BaseRemix(object):
  def __init__(self, args):
    self.input_file = os.path.join(
      statics.input_path, args.chord_type, args.base_chord_type) + '.wav'

    print self.input_file
    assert os.path.exists(self.input_file), 'Chord Music File Does Not Exist'
    self.remix_amount = args.remix_amount or random.random()

    self.output_folder = os.path.join(statics.output_path, args.chord_type, args.base_chord_type)
    print self.output_folder
    if not os.path.exists(self.output_folder):
      os.makedirs(self.output_folder)

    self.remix_amount = args.remix_amount or random.random()
    remix_str = '%.2f' % self.remix_amount
    output_file_name = "_".join([args.remix_type, remix_str]) + '.mp3'
    self.output_file = os.path.join(self.output_folder, output_file_name)

    print self.output_file

  def process(self):
      raise NotImplementedError

  def change_tempo(self):
      raise NotImplementedError

  def one_note_pitch_shift(self):
      raise NotImplementedError

  def all_note_pitch_shift(self):
      raise NotImplementedError

class ThreeNoteRemix(BaseRemix):
  Name = "three_note"
  def __init__(self, args):
    super(ThreeNoteRemix, self).__init__(args)

  def process(self):
    pass

class FourNoteRemix(BaseRemix):
  Name = "four_note"
  def __init__(self, args):
    super(FourNoteRemix, self).__init__(args)

  def process(self):
    pass

for remix in BaseRemix.__subclasses__():
    REMIXES[remix.Name] = remix