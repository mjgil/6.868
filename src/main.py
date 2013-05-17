import argparse
from remix import REMIXES

def parse_args():
    """
    Parses the command line arguments using the argparse python module

    Use -h to see the options.
    """
    print 'parsing arguments...'
    description = "Manipulates 3 and 4 note chords by changing pitch, tempo, and arrangement of notes"
    chord_type_help = 'Specify either three_note or four_note'
    base_chord_type_help = 'Name of base chord that you want to use (ex. major_fifth)'
    remix_type_help = 'What to change in the chord (one_note_pitch_shift, change_tempo, change_note_order, all_notes_pitch_shift)'
    remix_amount_help = 'Amount to change the remix type (Optional - Value between 0 and 1)'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('chord_type', help=chord_type_help)
    parser.add_argument('base_chord_type', help=base_chord_type_help)
    parser.add_argument('remix_type', help=remix_type_help)
    parser.add_argument('remix_amount', help=remix_amount_help, nargs='?')
    return parser.parse_args()

def main(args):
    """
    Main entry point of the application.

    Gets the appropriate Remix class based on the passed in command line
    arguments. Initializes the class if it is not None and then proceeds 
    to process the audio.
    """
    print "entering main..."
    remix = REMIXES.get(args.chord_type, None)
    assert remix is not None, 'Chord Type Invalid'

    remix = remix(args)
    remix.process()

if __name__ == '__main__':
    args = parse_args()
    main(args)
