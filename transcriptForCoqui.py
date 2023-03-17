import os

def transcript_for_coqui(transcript: list):
    for_coqui = []
    for l in transcript:
        if l == "" or l.isspace():
            continue
        splits = l.split('|')
        for_coqui.append(f'{splits[0]}|{splits[2].replace("[ES]", "")}')
    return for_coqui

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

    with open(f'{SCRIPT_DIR}/user_voice.txt.cleaned', 'r', encoding="utf-8") as f:
        transformed = transcript_for_coqui(f.read().split('\n'))
    with open(f'{SCRIPT_DIR}/user_voice_coqui.txt.cleaned', 'w', encoding="utf-8") as f:
        f.write('\n'.join(transformed) + '\n')