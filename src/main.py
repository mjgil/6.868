import argparse
from remix import REMIXES

def parse_args():
    print 'parsing arguments...'
    description = "Manipulates 3 and 4 note chords by changing pitch, tempo, and arrangement of notes"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('chord_type', 
        help='Specify either three_note or four_note')
    parser.add_argument('base_chord_type', 
        help='Name of base chord that you want to use (ex. major_fifth)')
    parser.add_argument('remix_type', 
        help='What to change in the chord (one_note_pitch_shift, change_tempo, change_note_order, all_notes_pitch_shift)')
    parser.add_argument('remix_amount', 
        help='Amount to change the remix type (Optional)',
        nargs='?')
    return parser.parse_args()

def main(args):
    print "entering main..."
    remix = REMIXES.get(args.chord_type, None)
    assert remix is not None, 'Chord Type Invalid'

    remix = remix(args)
    remix.process()

if __name__ == '__main__':
    args = parse_args()
    main(args)
