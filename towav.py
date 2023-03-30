from pydub import AudioSegment

filename = ""
AudioSegment.from_file(
            filename,
            format=filename.split('.')[-1]
        ).set_frame_rate(
            22050
        ).export(
            f'{".".join(filename.split(".")[:-1])}.wav',
            format="wav"
        )
