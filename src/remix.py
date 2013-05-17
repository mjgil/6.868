import os
import statics
import dirac
import random
from pyechonest import config
from echonest.remix import audio,modify
config.ECHO_NEST_API_KEY="UJGOWAOWXLAR4SBR9"
REMIXES = {}

def is_number(s):
  """
    Input: s - can really be anything

    tries to cast it to a float
    if it works return True
    else return False
  """
  try:
      float(s)
      return True
  except ValueError:
      return False


class BaseRemix(object):
  def __init__(self, args):
    """
    Input: args -- object created from parsed command line arguments

    Initializes the basic remix class.

    First, it forms the path for the input file from the 
    parameters that were inputted to the program.
    If the file cannot be found, it exits the program.

    Next, parses the remix_amount parameter or sets it to a 
    random float between zero and 1. If the inputted value 
    is not a number or is not between 0 and 1, it exits the 
    program.

    Finally, it sets the remix_type to be a class variable 
    and creates the output file path. It also creates the 
    output folder if it does not already exist.
    """

    self.input_file = os.path.join(statics.input_path,
                                   args.chord_type,
                                   args.base_chord_type) + '.wav'
    assert os.path.exists(self.input_file), 'Chord Music File Does Not Exist'

    self.remix_amount = args.remix_amount or random.random()
    assert is_number(self.remix_amount), 'Remix Amount Must Be A Number'
    self.remix_amount = float(self.remix_amount)
    assert (0.0 <= self.remix_amount <= 1.0), 'Remix Amount Must Be Between 0 and 1'

    self.remix_type = args.remix_type
    self.output_folder = os.path.join(statics.output_path, 
                                      args.chord_type,
                                      args.base_chord_type)
    if not os.path.exists(self.output_folder):
      os.makedirs(self.output_folder)

    remix_str = '%.2f' % self.remix_amount
    output_file_name = "_".join([args.remix_type, remix_str]) + '.mp3'
    self.output_file = os.path.join(self.output_folder, output_file_name)

  def process(self):
    """
    Pre-processes the inputted audio file (self.analyze())

    Then calls the corresponding function passed in through
    the remix_type argument.
    """
    self.analyze()

    fn = getattr(self, self.remix_type)
    assert hasattr(fn, '__call__'), 'Invalid Remix Type'
    fn()

  def change_tempo(self):
    """
    Changes the tempo of the beats in the chord

    Gets the beats from the self.beats list then 
    changes the tempo as specified by the remix_amount
    that was either generated on initialization of this
    class or passed in through the command line
    """
    collect = []
    for x in range(8):
      for beat in self.beats:
        ratio = self.remix_amount + 0.5
        beat_audio = beat.render()
        scaled_beat = dirac.timeScale(beat_audio.data, ratio)
        ts = audio.AudioData(ndarray=scaled_beat, shape=scaled_beat.shape, 
                             sampleRate=self.audiofile.sampleRate, 
                             numChannels=scaled_beat.shape[1])
        collect.append(ts)

    out = audio.assemble(collect, numChannels=2)
    self.encode(out)

  def change_note_order(self):
    """
    Changes the order of the notes played before a chord

    Gets the notes that make up the chord (all of the beats
    except for the last one) and randomly shuffles them.

    Next, it adds the chord back in and renders the audio out
    """
    collect = []
    beats = self.beats[:-1]
    random.shuffle(beats)
    chord = self.beats[-1]
    beats.append(chord)
    for x in range(8):

      for beat in beats:
        beat_audio = beat.render()
        scaled_beat = dirac.timeScale(beat_audio.data, 1.0)
        ts = audio.AudioData(ndarray=scaled_beat, shape=scaled_beat.shape, 
                             sampleRate=self.audiofile.sampleRate,
                             numChannels=scaled_beat.shape[1])
        collect.append(ts)

    out = audio.assemble(collect, numChannels=2)
    self.encode(out)

  def one_note_pitch_shift(self):
    """
    Picks one of the notes at random from the chord and 
    modulates it based on the remix_amount parameter

    Gets all of the notes of the chord from self.beats. 
    Picks one of the notes at random.
    Shifts that note by the remix amount.
    Then combines all of the notes together to generate
    a new chord from the notes.
    """    
    random_index = self.get_random()
    for x in range(8):
      beats = self.beats[:-1]
      beat_list = []
      for j, beat in enumerate(beats):
        shift_ratio = 1
        if j == random_index:
          shift_ratio = shift_ratio * self.remix_amount
        new_beat = self.soundtouch.shiftPitch(self.audiofile[beat], shift_ratio)
        self.out_data.append(new_beat)
        beat_list.append(new_beat)

      new_beat = self.mix_beat_list(beat_list)
      self.out_data.append(new_beat)
    self.encode(self.out_data)

  def all_notes_pitch_shift(self):
    """
    Picks modulates the notes of the chord by an amount
    specified from the remix_amount parameter

    Gets all of the notes of the chord from self.beats. 
    Shifts the notes by the remix amount.
    Then combines all of the notes together to generate
    a new chord from the notes.
    """    
    for x in range(8):
      beats = self.beats[:-1]
      beat_list = []
      for beat in beats:
        shift_ratio = self.remix_amount
        new_beat = self.soundtouch.shiftPitch(self.audiofile[beat], shift_ratio)
        self.out_data.append(new_beat)
        beat_list.append(new_beat)

      new_beat = self.mix_beat_list(beat_list)
      self.out_data.append(new_beat)
    self.encode(self.out_data)

  def encode(self, out):
    """
    Param: out - output audio data

    After all of the audio processing is done,
    renders the newly created audio to the appropriate
    output directories.

    Sends one to the path specified in statics.py and the
    passed in command_line parameters.

    Sends another to the three_note or four_note audio/sample 
    directory named 'previous.wav'. This enables us to chain
    together our audio effects easily.
    """    
    out.encode(self.output_file)
    prev_path = os.path.join(statics.input_path,self.Name,'previous.wav')
    out.encode(prev_path)

  def analyze(self):
    """
    Uses the echonest remix api to analyze the input_audio file.
    Saves the information in class variables.

    Finally calls get_beats() to handle the different types of 
    chords supported.
    """    
    self.soundtouch = modify.Modify()
    self.audiofile = audio.LocalAudioFile(self.input_file)
    self.bars = self.audiofile.analysis.bars
    self.out_shape = (len(self.audiofile.data),)
    self.out_data = audio.AudioData(shape=self.out_shape, numChannels=1, sampleRate=44100)
    self.get_beats()

  def get_beats(self):
    """
    Implemented in subclasses

    Iterates over the list of bars found through the analyze method
    If the length of the bar matches the number of notes expected, 
    4 for a 3 note scale (3 individual notes and then the chord) or
    5 for a 4 note scale then we save the beats in the correct order 
    in self.beats.

    This method is a bit weird because the echonest remix api doesn't
    always do the best job in sorting out the beats. To mitigate this
    we made sure that our audio files followed a certain pattern and 
    then coded to match our pattern.

    All of our audio files play the notes in the scale first and then
    the chord at the end. This is repeated 8 times so that the remix 
    API can do a good job with it's analysis.
    """    
    raise NotImplementedError

  def mix_beat_list(self, beat_list):
    """
    Implemented in subclasses

    Args: beat_list - a list of beats found through the echonest remix API

    Mixes the beats together using the audio.mix method of the remix API.
    There is a megamix but we found that mixing the beats individually 
    resulted in higher quality audio.
    """   
    raise NotImplementedError

  def get_random(self):
    """
    Implemented in subclasses

    Gets a random integer in the range of available notes. 0-2 for the three_note
    class and 0-3 for the four_note class. This is used to pick a random note to 
    shift in the one_note_pitch_shift method.
    """   
    raise NotImplementedError


class ThreeNoteRemix(BaseRemix):
  Name = "three_note"
  def __init__(self, args):
    super(ThreeNoteRemix, self).__init__(args)

  def get_beats(self):
    # for docs see method definition in BaseRemix
    for bar in self.bars:
      if (len(bar.children()) > 3):
        top = bar.children()[0]
        chord = bar.children()[1]
        root = bar.children()[2]
        middle = bar.children()[3]
        self.beats = [root, middle, top, chord]
        break

  def mix_beat_list(self, beat_list):
    # for docs see method definition in BaseRemix
    new_beat = audio.mix(beat_list[0], beat_list[1], 0.5)
    new_beat = audio.mix(new_beat, beat_list[2], 0.66)
    return new_beat

  def get_random(self):
    # for docs see method definition in BaseRemix
    return random.randrange(0,3)

class FourNoteRemix(BaseRemix):
  Name = "four_note"
  def __init__(self, args):
    super(FourNoteRemix, self).__init__(args)

  def get_beats(self):
    # for docs see method definition in BaseRemix
    for bar in self.bars:
      if (len(bar.children()) > 4):
        top = bar.children()[4]
        chord = bar.children()[0]
        root = bar.children()[1]
        middle = bar.children()[2]
        middle1 = bar.children()[3]
        self.beats = [root, middle, middle1, top, chord]
        break

  def mix_beat_list(self, beat_list):
    # for docs see method definition in BaseRemix
    new_beat = audio.mix(beat_list[0], beat_list[1], 0.5)
    new_beat = audio.mix(new_beat, beat_list[2], 0.66)
    new_beat = audio.mix(new_beat, beat_list[3], 0.75)
    return new_beat

  def get_random(self):
    # for docs see method definition in BaseRemix
    return random.randrange(0,4)

# stores subclasses of BaseRemixes in the REMIXES
# dictionary so that they can be read in main.py
for remix in BaseRemix.__subclasses__():
    REMIXES[remix.Name] = remix