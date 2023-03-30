import os
import time
from pydub import AudioSegment
from pydub.playback import play

def transcript_to_sentences(text: str, row_sep: str = "\n", col_sep: str = "|", sentence_pos: int = 1, start_row: int = None, end_row: int = None):

    table = [row.split(col_sep) for row in text.split(row_sep) if row != '']

    start_row = 0 if start_row is None else start_row
    end_row = len(table) if end_row is None else end_row

    return [row[sentence_pos] for row in table[start_row:end_row]]


def sentences_to_transcript(audio_path: str, sentences: str, row_sep: str = "\n", col_sep: str = "|", prepend: str = "", file_sorting = lambda x: x):

    transcript = []
    s = 0
    for fname in sorted(os.listdir(audio_path), key=file_sorting):
        transcript.append(f'{prepend}{fname}{col_sep}{sentences[s]}')
        s += 1

    return row_sep.join(transcript)

def validate_transcript(transcript, row_sep: str = "\n", col_sep: str = "|", audio_pos: int = 0, sentence_pos: int = 1, prepend: str = ""):

    for row in transcript.split(row_sep):
        
        row_split = row.split(col_sep)
        
        audio_path = row_split[audio_pos]
        audio_segment = AudioSegment.from_wav(f'{prepend}{audio_path}')
        
        text = row_split[sentence_pos]

        print(audio_path, ':', text)
        play(audio_segment)
        time.sleep(1)

if __name__ == "__main__":

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(SCRIPT_DIR, "user_voice_coqui.txt.cleaned"), encoding="utf-8") as f:
        transcript_text = f.read()

    sentences = transcript_to_sentences(transcript_text, start_row=93)

    all_transcript = []
    skip_validation = []

    for voice in ["hc", "eh", "mr"]:
        transcript = sentences_to_transcript(os.path.join(SCRIPT_DIR,"results",voice), sentences)
        
        if voice not in skip_validation:
            validate_transcript(transcript, prepend=os.path.join(SCRIPT_DIR,"results/eh/"))

        all_transcript.append(transcript)

    with open(os.path.join(SCRIPT_DIR, "results/transcript.txt"), 'w', encoding="utf-8") as f:
        f.write('\n'.join(all_transcript))

