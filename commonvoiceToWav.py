from pydub import AudioSegment
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

src_path = os.path.join(SCRIPT_DIR, "sources", "commonvoice")
dst_path = os.path.join(SCRIPT_DIR, "sources", "commonvoiceWav")

with open(os.path.join(src_path, 'validated.tsv'), encoding='utf-8') as f:
    validated = [l.split('\t') for l in f.read().split('\n')] 
    validated_cols = validated.pop(0) #first line has column data

paths = []
sentences = []
ids = []
id_nums = []
for v in validated: #using transpose would be faster but it does not work bc of irregularities
    try:
        paths.append(v[validated_cols.index('path')])
        sentences.append(v[validated_cols.index('sentence')])
        client_id = v[validated_cols.index('client_id')]
        if client_id in id_nums:
            ids.append(id_nums.index(client_id))
        else:
            ids.append(len(id_nums))
            id_nums.append(client_id)
    except IndexError as e:
        if v[0] == '':
            continue
        else:
            print(v)
            raise e
    except Exception as e:
        print(v)
        raise e
    
transcript = []
try:
    os.mkdir(os.path.join(dst_path, 'audios'))
except FileExistsError:
    pass
for p, i,  s in zip(paths, ids, sentences):
    AudioSegment.from_mp3(
        os.path.join(src_path, 'clips', p)
    ).set_frame_rate(
        22050
    ).export(
        os.path.join(dst_path, 'audios', p.replace('.mp3', '.wav')), format='wav'
    )

    transcript.append(f'{p.replace(".mp3", ".wav")}|{i}|{s}')

    with open(os.path.join(dst_path, 'transcript.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(transcript))