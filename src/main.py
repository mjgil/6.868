import argparse
from remix import Remix

def parse_args():
    print 'parsing arguments...'
    description = "Manipulates 3 and 4 note chords by changing pitch, tempo, and arrangement of notes"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('chord_type', 
        help='Specify either three_note or four_note')
    parser.add_argument('base_chord_name', 
        help='Name of base chord that you want to use (ex. major_fifth)')
    parser.add_argument('manipulation_type', 
        help='What to change in the chord (one_note_pitch, tempo, all_notes_pitch)')
    parser.add_argument('manipulation_amount', 
        help='Amount to change the manipulation type (Optional)',
        nargs='?')
    return parser.parse_args()

def main(args):
    print "entering main..."
    remix = Remix(args)
    remix.run()

if __name__ == '__main__':
    args = parse_args()
    main(args)
