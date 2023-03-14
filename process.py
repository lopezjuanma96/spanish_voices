import os
from pydub import AudioSegment
from zipfile import ZipFile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def prop_path(pth):
    """
    Returns the absolute path for a given pth respective to this script directory, so that it can be run from anywhere and give the same results.
    So if the script is located in path/to/script/ and a certain file is located at path/to/script/subpath/to/file/file.ext then this function
    can be used to get path/to/script/subpath/to/file/file.ext from doing prop_path(subpath/to/file/file.ext)
    """
    return os.path.join(SCRIPT_DIR, pth)

audio_pth_rel = 'spanish_voices/audio'
try:
    os.makedirs(prop_path(audio_pth_rel))
except OSError:
    pass

new_transcript = []
new_transcript_coqui = []
trnsc_pth = prop_path('spanish_voices')
try:
    os.makedirs(trnsc_pth)
except OSError:
    pass

#css10
amt = 300 #how many values to extract from this, can be None if ratio is not None
ratio = None #ratio of values to extract from this, can be None if amt is not None
id = 101

with open(prop_path('sources/css10/transcript.txt'), encoding="utf-8") as f:
    transcript = f.read()

raw = transcript.split('\n')
proc = [l.split('|')[:2] for l in raw if l!="" and not l.isspace()]
sort = list(sorted(proc, key = lambda x: len(x[1])))

if amt is None and ratio is None:
    raise ValueError("One of amt or ratio must be not None")
elif ratio is not None:
    amt = int(len(sort) * ratio)
else:
    amt = int(amt)

start = max(0, (len(sort)//2)-amt//2)
end = min(len(sort), (len(sort)//2)+amt//2 + 1)

for i in range(start, end):
    src_file = prop_path(f'sources/css10/{sort[i][0]}')
    dst_file_rel = f'{audio_pth_rel}/{os.path.split(src_file)[-1]}'
    dst_file = prop_path(dst_file_rel)
    AudioSegment.from_file(
        src_file, format="wav"
    ).set_frame_rate(
        22050
    ).export(
        dst_file, format="wav"
    )
    new_transcript.append(f'{dst_file_rel}|{id}|[ES]{sort[i][1]}[ES]')
    new_transcript_coqui.append(f'{dst_file_rel}|{sort[i][1]}')

#120h
amt = 300 #how many values to extract from this, can be None if ratio is not None
ratio = None #ratio of values to extract from this, can be None if amt is not None
id = 104 #although this dataset has many voices, they are not tagged so they will be treated all as one speaker, maybe later this can be improved

with open(prop_path('sources/120h/files.csv'), encoding="utf-8") as f:
    transcript = f.read()

raw = transcript.split('\n')
proc = [l.split(',')[0:3:2] for l in raw if l!="" and not l.isspace()]
for p in proc:
    if p[1][-1] in [".", ",", "!", "?"]:
        continue
    else:
        p[1] = p[1] + '.'
sort = list(sorted(proc, key = lambda x: len(x[1])))

if amt is None and ratio is None:
    raise ValueError("One of amt or ratio must be not None")
elif ratio is not None:
    amt = int(len(sort) * ratio)
else:
    amt = int(amt)

start = max(0, (len(sort)//2)-amt//2)
end = min(len(sort), (len(sort)//2)+amt//2 + 1)

for i in range(start, end):
    src_file = prop_path(f'sources/120h/{sort[i][0]}')
    dst_file_rel = f'{audio_pth_rel}/{os.path.split(src_file)[-1]}'
    dst_file = prop_path(dst_file_rel)
    AudioSegment.from_file(
        src_file, format="wav"
    ).set_frame_rate(
        22050
    ).export(
        dst_file, format="wav"
    )
    new_transcript.append(f'{dst_file_rel}|{id}|[ES]{sort[i][1]}[ES]')
    new_transcript_coqui.append(f'{dst_file_rel}|{sort[i][1]}')

#commonvoice
amt = 1400 #how many values to extract from this, can be None if ratio is not None
ratio = None #ratio of values to extract from this, can be None if amt is not None

with open(prop_path('sources/commonvoiceWav/transcript.txt'), encoding="utf-8") as f:
    transcript = f.read()

raw = transcript.split('\n')
proc = [l.split('|') for l in raw if l!="" and not l.isspace()]
for p in proc:
    if p[2][-1] in [".", ",", "!", "?"]:
        continue
    else:
        p[2] = p[2] + '.'
sort = list(sorted(proc, key = lambda x: len(x[2])))

if amt is None and ratio is None:
    raise ValueError("One of amt or ratio must be not None")
elif ratio is not None:
    amt = int(len(sort) * ratio)
else:
    amt = int(amt)

start = max(0, (len(sort)//2)-amt//2)
end = min(len(sort), (len(sort)//2)+amt//2 + 1)

for i in range(start, end):
    src_file = prop_path(f'sources/commonvoiceWav/audios/{sort[i][0]}')
    dst_file_rel = f'{audio_pth_rel}/{os.path.split(src_file)[-1]}'
    dst_file = prop_path(dst_file_rel)
    AudioSegment.from_file(
        src_file, format="wav"
    ).set_frame_rate(
        22050
    ).export(
        dst_file, format="wav"
    )
    new_transcript.append(f'{dst_file_rel}|{500 + int(sort[i][1])}|[ES]{sort[i][2]}[ES]')
    new_transcript_coqui.append(f'{dst_file_rel}|{sort[i][2]}')

#transcript
with open(f'{trnsc_pth}/transcript.txt', 'w', encoding="utf-8") as f:
    f.write('\n'.join(new_transcript) + '\n') #transcript requires ending in a newline
with open(f'{trnsc_pth}/transcript_coqui.txt', 'w', encoding="utf-8") as f:
    f.write('\n'.join(new_transcript_coqui) + '\n') #transcript requires ending in a newline

with ZipFile(prop_path('spanish_voices.zip'), 'w') as myzip:
    myzip.write(prop_path('spanish_voices/transcript.txt'), 'spanish_voices/transcript.txt')
    myzip.write(prop_path('spanish_voices/transcript_coqui.txt'), 'spanish_voices/transcript_coqui.txt')
    for audio_f in os.listdir(prop_path('spanish_voices/audio')):
        myzip.write(prop_path(f'spanish_voices/audio/{audio_f}'), f'spanish_voices/audio/{audio_f}')