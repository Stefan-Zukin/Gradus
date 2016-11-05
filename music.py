from abjad import *
import pickle
from random import *


class chord():

    def __init__(self, bass = 'c', third = 'e', fifth = 'g'):
        self.bass, self.third, self.fifth = bass, third, fifth

    def __str__(self):
        return str([self.bass, self.third, self.fifth])

    def __repr__(self):
        return str([self.bass, self.third, self.fifth])

    def other_two(self, note):
        if self.bass == note:
            return self.third + self.fifth
        elif self.third == note:
            return self.bass + self.fifth
        else:
            return self.bass + self.third

    def contains(self,note):
        return self.bass == note or self.third == note or self.fifth == note

    def bass_or_third(self,note=None):
        if not note:
            return self.bass
        elif note == self.bass:
            return self.third
        else:
            return self.bass

chords = {
        #Sharp Major Chords
        'c':chord('c','e','g'), 'g':chord('g','b','d'), 'd':chord('d','f#','a'), 'a':chord('a','c#','e'),
        'e':chord('e','g#','b'), 'b':chord('b','d#','f#'), 'f#':chord('f#','a#','c#'), 'c#':chord('c#','e#','g#'),
        'g#':chord('ab','a','c'), 'e#':chord('f','a','c'), 'a#':chord('bb','d','f'), 'd#':chord('eb','g','bb'), 'b#':chord('c','e','g'),
        #Flat Major Chords
        'f':chord('f','a','c'), 'bb':chord('bb','d','f'), 'eb':chord('eb','g','bb'), 'ab':chord('ab','a','c'),
        'db':chord('db','fb','ab'), 'gb':chord('gb','bb','db'), 'cb':chord('cb','eb','gb'), 'fb':chord('e','g#','b'),
        #Sharp Minor Chords
        'am':chord('a','c','e'), 'em':chord('e','g','b'), 'bm':chord('b','d','f#'), 'f#m':chord('f#','a','c#'),
        'c#m':chord('c#','e','g#'), 'g#m':chord('g#','b','d#'), 'd#m':chord('d#','f#','a#'), 'a#m':chord('a#','c#','e#'),
        'e#m':chord('f','ab','c'), 'b#m':chord('c','eb','g'),
        #Flat Minor Chords
        'dm':chord('d','f','a'), 'gm':chord('g','bb','d'), 'cm':chord('c','eb','g'), 'fm':chord('f','ab','c'),
        'bbm':chord('bb','db','f'), 'ebm':chord('eb','gb','bb'), 'abm':chord('ab','cb','eb'), 'gbm':chord('a#','c#','e#'),
        'fbm':chord('e','g','b'), 'dbm':chord('c#','e','g#'), 'cbm':chord('b','d','f#')
        }

enharmonics = {'f#':'gb','gb':'f#','g#':'ab','ab':'g#','a#':'bb','bb':'a#','e#':'f',
            'c#':'db','db':'c#','d#':'eb','eb':'d#','c':'c','d':'d','e':'e','f':'f','g':'g','a':'a','b':'b'}

chords_in_key = []

used_notes = []

class my_note():

    def __init__(self,duration = 4,pitch = 'c',octave = 4,variation=0):
        self.duration = duration
        self.pitch = pitch
        self.octave = octave
        self.variation = variation

    def __str__(self):
        return str([self.duration,self.pitch,self.octave,self.variation])

    def __repr__(self):
        return str([self.duration,self.pitch,self.octave,self.variation])

    def compound_pitch(self):
        """returns a string representing the accidental and pitch for use with the chord dictionary"""
        if self.variation == 2:
            return self.pitch +'b'
        elif self.variation == 1:
            return self.pitch + '#'
        else:
            return self.pitch

    def possible_chords(self):
        """returns list of chords that contain this note"""
        possible_chords = []
        for x in list(chords.values()):
            if x.contains(self.compound_pitch()):
                possible_chords.append(x)
        return possible_chords

    def random_chord(self): #placeholder until write algorithm to pick chords.
        chords = self.possible_chords()
        if not chords:
            return 'No Chords'
        else:
            return chords[0]

    def to_Note(self):
        """Converts a my_note() object into a Note() object for use with the abjad library"""
        if self.variation == 1:
                n =  Note(self.pitch[0] + 's' +"'" + str(self.duration))
        elif self.variation == 2:
                n =  Note(self.pitch[0] + 'f' + "'" + str(self.duration))
        else:
            n =  Note(self.pitch + "'" + str(self.duration))
        temp_octave = self.octave

        # """This part makes our representation of octave as an integer value work with
        # the library's representation of the octave as multiple '''' strings"""
        while temp_octave > 4:
            n.written_pitch += 12
            temp_octave -= 1
        while temp_octave < 4:
            n.written_pitch -= 12
            temp_octave += 1
        return n

class my_note_line():

    def __init__(self, note_list = []):
        self.list = note_list

    def __str__(self):
        return str(self.list)

    def __getitem__(self,index):
        return self.list[index]

    def __len__(self):
        return len(self.list)

    def __repr__(self):
        return str(self.list)

    def __iter__(self):
        return iter(self.list)

    def to_Notes(self):
        return my_note_line([x.to_Note() for x in self.list])

    def append(self, note):
        if isinstance(note,list):
            self.list += note
        else:
            self.list.append(note)

def find_key(note_line):
    best_guess = ''
    def major_or_minor(guess):
        if whole_step(whole_step(guess)) in [x.compound_pitch() for x in note_line]:
            return 'm'
        else:
            return ''
    if note_line[0].pitch == note_line[len(note_line)-1].pitch:
        best_guess = note_line[0].pitch
    elif max([x.pitch for x in note_line]) == note_line[len(note_line)-1].pitch:
        best_guess = note_line[len(note_line)-1].pitch
    else:
        best_guess = note_line[len(note_line)-1].pitch
    return best_guess + major_or_minor(best_guess)

def mode(x):
    """Not very accurate mode function.
    Used to find the average beat over a melody"""
    return sum(x)//len(x)

def whole_step(pitch):
    if pitch == 'e#':
        pitch = 'f'
    elif pitch == 'b#':
        pitch = 'c'
    elif pitch == 'fb':
        pitch = 'e'
    elif pitch == 'cb':
        pitch = 'b'
    elif pitch == 'b':
        return 'c#'
    elif pitch == 'e':
        return 'f#'
    elif pitch == 'b':
        return 'c#'
    """Returns the pitch up a whole step"""
    if pitch[0] == 'g':
        pitch = 'a' + pitch[1:]
    else:
        pitch = chr(ord(pitch[0])+1) + pitch[1:]
    if len(pitch) > 2 and pitch[1] == 'm' :
        return clean_up(pitch[0] + pitch[2])
    elif len(pitch) > 1 and pitch[1] == 'm':
        return clean_up(pitch[0])
    else:
        return clean_up(pitch)

def clean_up(pitch):
    if pitch == 'b#':
        return 'c'
    elif pitch == 'e#':
        return 'f'
    elif pitch == 'cb':
        return 'b'
    elif pitch == 'fb':
        return 'e'
    else:
        return pitch

def ws(p):
    #Quicker wat to do it because I don't want to implement step up/down
    return whole_step(p)

def hs(p):
    return half_step(p)

def hsd(p):
    return half_step_down(p)

def wsd(p):
    if p == 'd':
        return 'c'
    return hsd(hsd(p))

def half_step_down(pitch):
    return ws(half_step((ws(ws(ws(ws(pitch)))))))

def half_step(pitch):
    """Returns the pitch up a half step"""
    if len(pitch) > 1 and pitch[1] == '#':
        return whole_step(pitch)[0]
    elif len(pitch) > 1 and pitch[1] == 'b':
        return pitch[0]
    else:
        return pitch[0] + '#'

def set_chords_in_key(key):
    """Sets the chords_in_key list to contain the diatonic chords from the key"""

    if key[len(key)-1] == 'm':
        key = key[:len(key)-1]
        tones = [key]
        key = clean_up(ws(key))
        tones.append(key)
        key = clean_up(hs(key))
        tones.append(key)
        key = clean_up(ws(key))
        tones.append(key)
        key = clean_up(ws(key))
        tones.append(key)
        key = clean_up(hs(key))
        tones.append(key)
        key = clean_up(ws(key))
        tones.append(key)
    else:
        tones = [key]
        key = clean_up(ws(key))
        tones.append(key)
        key = clean_up(ws(key))
        tones.append(key)
        key = clean_up(hs(key))
        tones.append(key)
        key = clean_up(ws(key))
        tones.append(key)
        key = clean_up(ws(key))
        tones.append(key)
        key = clean_up(ws(key))
        tones.append(key)
    chords_in_key.append(chord(tones[0],tones[2],tones[4]))
    chords_in_key.append(chord(tones[1],tones[3],tones[5]))
    chords_in_key.append(chord(tones[2],tones[4],tones[6]))
    chords_in_key.append(chord(tones[3],tones[5],tones[0]))
    chords_in_key.append(chord(tones[4],tones[6],tones[1]))
    chords_in_key.append(chord(tones[5],tones[0],tones[2]))
    chords_in_key.append(chord(tones[6],tones[1],tones[3]))

def find_best_chord(notes = [], key = 'c'):
    #See if any chords have two of the notes in them.
    if len(notes) > 1:
        for x in chords_in_key:
            if (x.contains(notes[0].compound_pitch()) or x.contains(enharmonics[notes[0].compound_pitch()])) and (x.contains(notes[1].compound_pitch()) or x.contains(enharmonics[notes[1].compound_pitch()])):
                return x
    note = notes[0]
    if chords_in_key[0].contains(note.compound_pitch()) or chords_in_key[0].contains(enharmonics[note.compound_pitch()]):
        return chords_in_key[0]
    elif chords_in_key[4].contains(note.compound_pitch() or chords_in_key[4].contains(enharmonics[note.compound_pitch()])):
        return chords_in_key[4]
    elif chords_in_key[3].contains(note.compound_pitch()) or chords_in_key[3].contains(enharmonics[note.compound_pitch()]):
        return chords_in_key[3]
    elif chords_in_key[5].contains(note.compound_pitch()) or chords_in_key[5].contains(enharmonics[note.compound_pitch()]):
        return chords_in_key[5]
    else:
        return chords_in_key[0]

def find_close_note(note, chord):
    if(randint(0,3) == 2):
        if randint(0,3) == 1:
            return chord.bass
        elif randint(0,3) == 1:
            return chord.third
        else:
            return chord.fifth
    for x in [chord.bass,chord.third,chord.fifth]:
        if note.pitch == x:
            return x
    note.pitch = hs(note.pitch)
    for x in [chord.bass,chord.third,chord.fifth]:
        if note.pitch == x:
            return x
    note.pitch = wsd(note.pitch)
    for x in [chord.bass,chord.third,chord.fifth]:
        if note.pitch == x:
            return x
    note.pitch = ws(hs(note.pitch))
    for x in [chord.bass,chord.third,chord.fifth]:
        if note.pitch == x:
            return x
    return None

def find_best_note(used_notes = [my_note(1,'f',4,0)],ch = chord()):
    if len(used_notes) == 2 and find_close_note(used_notes[0], ch):
        return find_close_note(used_notes[0], ch)
    else:
        for x in [ch.bass, ch.third, ch.fifth]:
            if x not in [x.pitch for x in used_notes]:
                return x
        return "ERROR"

def create_bassline(melody = [my_note(1,'f',4,0)]):
    bassline = my_note_line([])
    avg_duration = mode([x.duration for x in melody.list])
    skip = 0
    for n in melody.list:
        if skip > 0:
            skip -= 1
        else:
            """This section fixes the difference btween sharps and flats being represented in strings in the chords
            dictionary, and them being represented numerically in the my_note object"""
            new_note = find_best_note([n],find_best_chord([n],key))
            duration = n.duration
            variation = 0
            if len(new_note) > 1:
                if new_note[1] == 'b':
                    variation = 2
                elif new_note[1] =='#':
                    variation = 1
                new_note = new_note[0]
            """Adds the bass note of a random chord containing the melody note to the bassline my_note_line"""
            if duration == avg_duration*2:
                skip = 1
                duration = avg_duration
            if(n.octave > 0):
                bassline.append(my_note(duration,find_best_note([n],find_best_chord([n],key)),n.octave-2,variation))
            else:
                bassline.append(my_note(duration,find_best_note([n],find_best_chord([n],key)),n.octave-3,variation))
    return bassline

def create_altoline(melody = [my_note(1,'f',4,0)], bassline = [my_note(1,'f',4,0)]):
    altoline = my_note_line([])
    for n in melody.list:
        """This section fixes the difference btween sharps and flats being represented in strings in the chords
        dictionary, and them being represented numerically in the my_note object"""
        new_note = find_best_note([n],find_best_chord([n],key))
        variation = 0
        if len(new_note) > 1:
            if new_note[1] == 'b':
                variation = 2
            elif new_note[1] =='#':
                variation = 1
            new_note = new_note[0]

        """Adds the bass note of a random chord containing the melody note to the altoline my_note_line"""
        if(n.octave > 0):
            altoline.append(my_note(n.duration,find_best_note([n, my_note(4,find_best_chord([n],key).fifth,4,0)],find_best_chord([n],key)),n.octave-1,variation))
        else:
            altoline.append(my_note(n.duration,find_best_note([n],find_best_chord([n],key)),n.octave,variation))
    return altoline

def create_tenorline(melody = [my_note(1,'f',4,0)], bassline = [my_note(1,'f',4,0)]):
    tenorline = my_note_line([])
    for n in melody.list:
        """This section fixes the difference btween sharps and flats being represented in strings in the chords
        dictionary, and them being represented numerically in the my_note object"""
        new_note = find_best_note([n],find_best_chord([n],key))
        variation = 0
        if len(new_note) > 1:
            if new_note[1] == 'b':
                variation = 2
            elif new_note[1] =='#':
                variation = 1
            new_note = new_note[0]

        """Adds the bass note of a random chord containing the melody note to the tenorline my_note_line"""
        if(n.octave > 0):
            tenorline.append(my_note(n.duration,find_best_note([n,my_note(4,find_best_chord([n],key).fifth,4,0)],find_best_chord([n],key)),n.octave-1,variation))
        else:
            tenorline.append(my_note(n.duration,find_best_note([n],find_best_chord([n],key)),n.octave,variation))
    return tenorline

def display(treble = [Note(pitch,Duration(1,4)) for pitch in range(8)], alto = [], tenor = [], bass = []):
    duration = sum([x.written_duration for x in treble])
    multimeasure_rest = scoretools.MultimeasureRest('R1')

    #Make Treble Staff
    treble_staff = Staff(treble)
    treble_voice = instrumenttools.SopranoVoice()
    attach(treble_voice, treble_staff)
    clef1 = Clef(name='treble')
    attach(clef1, treble_staff)

    #Make Alto Staff
    """The if/else statement fills the alto/tenor/bass staves with full measure rests
    if no notes are given"""
    if len(alto) == 0:
        alto_rest = scoretools.MultimeasureRest('R1')
        attach(Multiplier(duration), alto_rest)
        alto_staff = Staff([alto_rest])
    else:
        alto_staff = Staff(alto)
    alto_voice = instrumenttools.AltoVoice()
    attach(alto_voice, alto_staff)
    clef2 = Clef(name='alto')
    attach(clef2, alto_staff)

    #Make Tenor Staff
    if len(tenor) == 0:
        tenor_rest = scoretools.MultimeasureRest('R1')
        attach(Multiplier(duration), tenor_rest)
        tenor_staff = Staff([tenor_rest])
    else:
        tenor_staff = Staff(tenor)
    tenor_voice = instrumenttools.TenorVoice()
    attach(tenor_voice, tenor_staff)
    clef3 = Clef(name='tenor')
    attach(clef3, tenor_staff)

    #Make Bass Staff
    if len(bass) == 0:
        bass_rest = scoretools.MultimeasureRest('R1')
        attach(Multiplier(duration), bass_rest)
        bass_staff = Staff([bass_rest])
    else:
        bass_staff = Staff(bass)
    bass_voice = instrumenttools.BassVoice()
    attach(bass_voice, bass_staff)
    clef4 = Clef(name='bass')
    attach(clef4, bass_staff)
    score = Score([treble_staff,alto_staff,tenor_staff, bass_staff])
    show(score)

def static_demo():
    n = my_note_line([my_note(2,'a',5,0),my_note(4,'g',4,0),my_note(4,'f',4.0),my_note(1,'d',4,0),my_note(1,'g',4,0)])
    display(n.to_Notes())
    display(n.to_Notes(), create_altoline(n).to_Notes(),create_tenorline(n).to_Notes(),create_bassline(n).to_Notes())

def dynamic_demo():
    display(input_line.to_Notes())
    display(input_line.to_Notes(),create_altoline(input_line).to_Notes(),create_tenorline(input_line).to_Notes(),create_bassline(input_line).to_Notes())


input_line = []
key = 'c'

def main(name='working.pcl'):
    # if len(my_list) == 0:
    #     static_demo()
    # else:
    with open('working.pcl', 'rb') as f:
        my_list = pickle.load(f)
        global input_line
        global key
        input_line = my_note_line()
        for x in my_list:
            input_line.append(my_note(x[0],x[1],x[2],x[3]))
        # key = find_key(input_line)
        set_chords_in_key(key)
    dynamic_demo()

if __name__ == "__main__":
    main()
