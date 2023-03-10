import os
import shutil
from zipfile import ZipFile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def prop_path(pth):
    """
    Returns the absolute path for a given pth respective to this script directory, so that it can be run from anywhere and give the same results.
    So if the script is located in path/to/script/ and a certain file is located at path/to/script/subpath/to/file/file.ext then this function
    can be used to get path/to/script/subpath/to/file/file.ext from doing prop_path(subpath/to/file/file.ext)
    """
    return os.path.join(SCRIPT_DIR, pth)

audio_pth = prop_path('combine/audio')
try:
    os.makedirs(audio_pth)
except OSError:
    pass

new_transcript = []
trnsc_pth = prop_path('combine')
try:
    os.makedirs(trnsc_pth)
except OSError:
    pass

#css10
amt = 300 #how many values to extract from this, can be None if ratio is not None
ratio = None #ratio of values to extract from this, can be None if amt is not None
id = 101

with open(prop_path('sources/css10/transcript.txt')) as f:
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

start = (len(sort)//2)-amt//2
end = (len(sort)//2)+amt//2 + 1

for i in range(start, end):
    src_file = prop_path(f'sources/css10/{sort[i][0]}')
    dst_file = prop_path(f'{audio_pth}/{os.path.split(src_file)[-1]}')
    shutil.copyfile(src_file, dst_file)
    new_transcript.append(f'{dst_file}|{id}|[ES]{sort[i][1]}[ES]')

#120h
amt = 700 #how many values to extract from this, can be None if ratio is not None
ratio = None #ratio of values to extract from this, can be None if amt is not None
id = 104 #although this dataset has many voices, they are not tagged so they will be treated all as one speaker, maybe later this can be improved

with open(prop_path('sources/120h/files.csv')) as f:
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

start = (len(sort)//2)-amt//2
end = (len(sort)//2)+amt//2 + 1

for i in range(start, end):
    src_file = prop_path(f'sources/120h/{sort[i][0]}')
    dst_file = prop_path(f'{audio_pth}/{os.path.split(src_file)[-1]}')
    shutil.copyfile(src_file, dst_file)
    new_transcript.append(f'{dst_file}|{id}|[ES]{sort[i][1]}[ES]')

#transcript
with open(f'{trnsc_pth}/transcript.txt', 'w') as f:
    f.write('\n'.join(new_transcript))

with ZipFile(prop_path('combine.zip'), 'w') as myzip:
    myzip.write(prop_path('combine/transcript.txt'), 'transcript.txt')
    for audio_f in os.listdir(prop_path('combine/audio')):
        myzip.write(prop_path(f'combine/audio/{audio_f}'), f'audio/{audio_f}')