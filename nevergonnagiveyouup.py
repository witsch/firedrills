# from https://github.com/robsoncouto/arduino-songs/blob/master/nevergonnagiveyouup/nevergonnagiveyouup.ino

from asyncio import TaskGroup, run, sleep, to_thread
from aiohttp import ClientSession
from dataclasses import dataclass
from pysine import sine


NOTE_B0  = 31
NOTE_C1  = 33
NOTE_CS1 = 35
NOTE_D1  = 37
NOTE_DS1 = 39
NOTE_E1  = 41
NOTE_F1  = 44
NOTE_FS1 = 46
NOTE_G1  = 49
NOTE_GS1 = 52
NOTE_A1  = 55
NOTE_AS1 = 58
NOTE_B1  = 62
NOTE_C2  = 65
NOTE_CS2 = 69
NOTE_D2  = 73
NOTE_DS2 = 78
NOTE_E2  = 82
NOTE_F2  = 87
NOTE_FS2 = 93
NOTE_G2  = 98
NOTE_GS2 = 104
NOTE_A2  = 110
NOTE_AS2 = 117
NOTE_B2  = 123
NOTE_C3  = 131
NOTE_CS3 = 139
NOTE_D3  = 147
NOTE_DS3 = 156
NOTE_E3  = 165
NOTE_F3  = 175
NOTE_FS3 = 185
NOTE_G3  = 196
NOTE_GS3 = 208
NOTE_A3  = 220
NOTE_AS3 = 233
NOTE_B3  = 247
NOTE_C4  = 262
NOTE_CS4 = 277
NOTE_D4  = 294
NOTE_DS4 = 311
NOTE_E4  = 330
NOTE_F4  = 349
NOTE_FS4 = 370
NOTE_G4  = 392
NOTE_GS4 = 415
NOTE_A4  = 440
NOTE_AS4 = 466
NOTE_B4  = 494
NOTE_C5  = 523
NOTE_CS5 = 554
NOTE_D5  = 587
NOTE_DS5 = 622
NOTE_E5  = 659
NOTE_F5  = 698
NOTE_FS5 = 740
NOTE_G5  = 784
NOTE_GS5 = 831
NOTE_A5  = 880
NOTE_AS5 = 932
NOTE_B5  = 988
NOTE_C6  = 1047
NOTE_CS6 = 1109
NOTE_D6  = 1175
NOTE_DS6 = 1245
NOTE_E6  = 1319
NOTE_F6  = 1397
NOTE_FS6 = 1480
NOTE_G6  = 1568
NOTE_GS6 = 1661
NOTE_A6  = 1760
NOTE_AS6 = 1865
NOTE_B6  = 1976
NOTE_C7  = 2093
NOTE_CS7 = 2217
NOTE_D7  = 2349
NOTE_DS7 = 2489
NOTE_E7  = 2637
NOTE_F7  = 2794
NOTE_FS7 = 2960
NOTE_G7  = 3136
NOTE_GS7 = 3322
NOTE_A7  = 3520
NOTE_AS7 = 3729
NOTE_B7  = 3951
NOTE_C8  = 4186
NOTE_CS8 = 4435
NOTE_D8  = 4699
NOTE_DS8 = 4978
REST     =  0


# change this to make the song slower or faster
tempo = 114

# change this to whichever pin you want to use
buzzer = 11

# notes of the moledy followed by the duration.
# a 4 means a quarter note, 8 an eighteenth , 16 sixteenth, so on
# !!negative numbers are used to represent dotted notes,
# so -4 means a dotted quarter note, that is, a quarter plus an eighteenth!!
melody = (
    # Never Gonna Give You Up - Rick Astley
    # Score available at https://musescore.com/chlorondria_5/never-gonna-give-you-up_alto-sax
    # Arranged by Chlorondria

    NOTE_D5,-4, NOTE_E5,-4, NOTE_A4,4, # 1
    NOTE_E5,-4, NOTE_FS5,-4, NOTE_A5,16, NOTE_G5,16, NOTE_FS5,8,
    NOTE_D5,-4, NOTE_E5,-4, NOTE_A4,2,
    NOTE_A4,16, NOTE_A4,16, NOTE_B4,16, NOTE_D5,8, NOTE_D5,16,
    NOTE_D5,-4, NOTE_E5,-4, NOTE_A4,4, # repeat from 1
    NOTE_E5,-4, NOTE_FS5,-4, NOTE_A5,16, NOTE_G5,16, NOTE_FS5,8,
    NOTE_D5,-4, NOTE_E5,-4, NOTE_A4,2,
    NOTE_A4,16, NOTE_A4,16, NOTE_B4,16, NOTE_D5,8, NOTE_D5,16,
    REST,4, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_D5,8, NOTE_E5,8, NOTE_CS5,-8,
    NOTE_B4,16, NOTE_A4,2, REST,4,

    REST,8, NOTE_B4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,4, NOTE_A4,8, # 7
    NOTE_A5,8, REST,8, NOTE_A5,8, NOTE_E5,-4, REST,4,
    NOTE_B4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8, NOTE_D5,8, NOTE_E5,8, REST,8,
    REST,8, NOTE_CS5,8, NOTE_B4,8, NOTE_A4,-4, REST,4,
    REST,8, NOTE_B4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8, NOTE_A4,4,
    NOTE_E5,8, NOTE_E5,8, NOTE_E5,8, NOTE_FS5,8, NOTE_E5,4, REST,4,

    NOTE_D5,2, NOTE_E5,8, NOTE_FS5,8, NOTE_D5,8, # 13
    NOTE_E5,8, NOTE_E5,8, NOTE_E5,8, NOTE_FS5,8, NOTE_E5,4, NOTE_A4,4,
    REST,2, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8,
    REST,8, NOTE_E5,8, NOTE_FS5,8, NOTE_E5,-4, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
    NOTE_FS5,-8, NOTE_FS5,-8, NOTE_E5,-4, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,

    NOTE_E5,-8, NOTE_E5,-8, NOTE_D5,-8, NOTE_CS5,16, NOTE_B4,-8, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16, # 18
    NOTE_D5,4, NOTE_E5,8, NOTE_CS5,-8, NOTE_B4,16, NOTE_A4,8, NOTE_A4,8, NOTE_A4,8,
    NOTE_E5,4, NOTE_D5,2, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
    NOTE_FS5,-8, NOTE_FS5,-8, NOTE_E5,-4, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
    NOTE_A5,4, NOTE_CS5,8, NOTE_D5,-8, NOTE_CS5,16, NOTE_B4,8, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,

    NOTE_D5,4, NOTE_E5,8, NOTE_CS5,-8, NOTE_B4,16, NOTE_A4,4, NOTE_A4,8,  # 23
    NOTE_E5,4, NOTE_D5,2, REST,4,
    REST,8, NOTE_B4,8, NOTE_D5,8, NOTE_B4,8, NOTE_D5,8, NOTE_E5,4, REST,8,
    REST,8, NOTE_CS5,8, NOTE_B4,8, NOTE_A4,-4, REST,4,
    REST,8, NOTE_B4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8, NOTE_A4,4,
    REST,8, NOTE_A5,8, NOTE_A5,8, NOTE_E5,8, NOTE_FS5,8, NOTE_E5,8, NOTE_D5,8,

    REST,8, NOTE_A4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8, # 29
    REST,8, NOTE_CS5,8, NOTE_B4,8, NOTE_A4,-4, REST,4,
    NOTE_B4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8, NOTE_A4,4, REST,8,
    REST,8, NOTE_E5,8, NOTE_E5,8, NOTE_FS5,4, NOTE_E5,-4, REST,0,
    NOTE_D5,2, NOTE_D5,8, NOTE_E5,8, NOTE_FS5,8, NOTE_E5,4,
    NOTE_E5,8, NOTE_E5,8, NOTE_FS5,8, NOTE_E5,8, NOTE_A4,8, NOTE_A4,4,

    REST,-4, NOTE_A4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8, # 35
    REST,8, NOTE_E5,8, NOTE_FS5,8, NOTE_E5,-4, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
    NOTE_FS5,-8, NOTE_FS5,-8, NOTE_E5,-4, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
    NOTE_E5,-8, NOTE_E5,-8, NOTE_D5,-8, NOTE_CS5,16, NOTE_B4,8, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
    NOTE_D5,4, NOTE_E5,8, NOTE_CS5,-8, NOTE_B4,16, NOTE_A4,4, NOTE_A4,8,

    NOTE_E5,4, NOTE_D5,2, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16, # 40
    NOTE_FS5,-8, NOTE_FS5,-8, NOTE_E5,-4, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
    NOTE_A5,4, NOTE_CS5,8, NOTE_D5,-8, NOTE_CS5,16, NOTE_B4,8, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
    NOTE_D5,4, NOTE_E5,8, NOTE_CS5,-8, NOTE_B4,16, NOTE_A4,4, NOTE_A4,8,
    NOTE_E5,4, NOTE_D5,2, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,

    NOTE_FS5,-8, NOTE_FS5,-8, NOTE_E5,-4, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16, # 45
    NOTE_A5,4, NOTE_CS5,8, NOTE_D5,-8, NOTE_CS5,16, NOTE_B4,8, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
    NOTE_D5,4, NOTE_E5,8, NOTE_CS5,-8, NOTE_B4,16, NOTE_A4,4, NOTE_A4,8,
    NOTE_E5,4, NOTE_D5,2, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
    NOTE_FS5,-8, NOTE_FS5,-8, NOTE_E5,-4, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16, # 45
 
    NOTE_A5,4, NOTE_CS5,8, NOTE_D5,-8, NOTE_CS5,16, NOTE_B4,8, REST,0, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
    NOTE_D5,4, NOTE_E5,8, NOTE_CS5,-8, NOTE_B4,16, NOTE_A4,4, NOTE_A4,8,

    NOTE_E5,4, NOTE_D5,2, REST,4
)

#  this calculates the duration of a whole note in ms
wholenote = (60000 * 4) / tempo


@dataclass
class Note:
    frequency: int
    duration: int


def notes():
    # iterate over the notes of the melody.
    # Remember, the array is twice the number of notes (notes + durations)
    for thisNote in range(0, len(melody), 2):
        # calculates the duration of each note
        divider = melody[thisNote + 1];
        if divider > 0:
            # regular note, just proceed
            noteDuration = (wholenote) / divider;
        elif divider < 0:
            # dotted notes are represented with negative durations!!
            noteDuration = (wholenote) / abs(divider);
            noteDuration *= 1.5; #  increases the duration in half for dotted notes
        else:
            noteDuration = 0
        yield Note(frequency=melody[thisNote], duration=noteDuration)


def words():
    lyrics = """
        We're no strangers to love
        You know the rules and so do I
        A full commitment's what I'm thinking of
        You wouldn't get this from any other guy
        I just wanna tell you how I'm feeling
        Gotta make you understand
        Never gonna give you up
        Never gonna let you down
        Never gonna run around and desert you
        Never gonna make you cry
        Never gonna say goodbye
        Never gonna tell a lie and hurt you
        We've known each other for so long
        Your heart's been aching but you're too shy to say it
        Inside we both know what's been going on
        We know the game and we're gonna play it
        And if you ask me how I'm feeling
        Don't tell me you're too blind to see
        Never gonna give you up
        Never gonna let you down
        Never gonna run around and desert you
        Never gonna make you cry
        Never gonna say goodbye
        Never gonna tell a lie and hurt you
        Never gonna give you up
        Never gonna let you down
        Never gonna run around and desert you
        Never gonna make you cry
        Never gonna say goodbye
        Never gonna tell a lie and hurt you
        Never gonna give, never gonna give
        (Give you up)
        (Ooh) Never gonna give, never gonna give
        (Give you up)
        We've known each other for so long
        Your heart's been aching but you're too shy to say it
        Inside we both know what's been going on
        We know the game and we're gonna play it
        I just wanna tell you how I'm feeling
        Gotta make you understand
        Never gonna give you up
        Never gonna let you down
        Never gonna run around and desert you
        Never gonna make you cry
        Never gonna say goodbye
        Never gonna tell a lie and hurt you
        Never gonna give you up
        Never gonna let you down
        Never gonna run around and desert you
        Never gonna make you cry
        Never gonna say goodbye
        Never gonna tell a lie and hurt you
        Never gonna give you up
        Never gonna let you down
        Never gonna run around and desert you
        Never gonna make you cry """
    separations = {
        'Gotta': 'Got-/-ta',
        'Inside': 'In-/-side',
        'Never': 'Ne-/-ver',
        'aching': 'a-/-ching',
        'any': 'a-/-ny',
        'around': 'a-/-round',
        "commitment's": "com-/-mit-/-ment's",
        'desert': 'de-/-sert',
        'feeling': 'fee-/-ling',
        'gonna': 'gon-/-na',
        'goodbye': 'good-/-bye',
        'love': 'lo-/-oho-/-hove',
        'never': 'ne-/-ver',
        'other': 'ot-/-her',
        'rules': 'ru-/-hules',
        'strangers': 'stran-/-gers',
        'thinking': 'thin-/-king',
        'understand': 'un-/-der-/-stand',
        'wanna': 'wan-/-na'}
    for word in lyrics.strip().replace('\n', ' ... ').split():
        if word in separations:
            yield from separations[word].split('/')
        else:
            yield word


async def at(time, coro):
    await sleep(time / 1000)
    await coro


async def say(note, word):
    print(f'{str(note):50s} {word}')


async def play():
    sing, pause = False, False
    start = 1000
    w = words()
    async with ClientSession() as session:
        async with TaskGroup() as group:
            schedule = lambda coro: group.create_task(at(start, coro))
            for note in notes():
                if pause and note.frequency != REST:
                    sing = True
                word = next(w) if sing else '...'
                # we only play the note for 90% of the duration, leaving 10% as a pause
                duration = note.duration * 0.9 / 1000
                url = f'https://www.zeit.de/-/freebies/rpc/check?select=-{note.frequency}hz'
                payload = dict(token=f'{note.frequency}hz', path='/entdecken/2023-10/rick-astley-wochenende-tipps-podcast')
                headers = {
                    'User-Agent': word or '...',
                    'Referer': 'https://www.zeit.de/entdecken/2023-10/rick-astley-wochenende-tipps-podcast'
                }
                if note.frequency:
                    schedule(session.post(url, data=payload, headers=headers))
                    schedule(to_thread(sine, frequency=note.frequency, duration=duration))
                    schedule(say(note, word))
                start += note.duration
                # Wait for the specief duration before playing the next note.
                sing &= word != '...'
                pause = note.frequency == REST
            print("let's roll...")


run(play())
