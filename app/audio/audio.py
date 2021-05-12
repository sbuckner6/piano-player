import subprocess, wave

# p = pyaudio.PyAudio()
# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
#
#
# def genHeader(sampleRate, bitsPerSample, channels):
#     datasize = 2000*10**6
#     o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
#     o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
#     o += bytes("WAVE",'ascii')                                              # (4byte) File type
#     o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
#     o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
#     o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
#     o += (channels).to_bytes(2,'little')                                    # (2byte)
#     o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
#     o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
#     o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
#     o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
#     o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
#     o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
#     return o
#
#
#
#
#
# def stream_audio(midi_file, audio_file):
#     render_audio(midi_file, audio_file)
#     wf = wave.open(audio_file, 'rb')
#     wav_header = genHeader(sampleRate=wf.getframerate(), bitsPerSample=16, channels=wf.getnchannels)
#
#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                     channels=wf.getnchannels(),
#                     rate=wf.getframerate(),
#                     output=True)
#
#     first_run = True
#
#     while True:
#         if first_run:
#             data = wav_header + stream.read(CHUNK)
#             first_run = False
#         else:
#             data = stream.read(CHUNK)
#         yield data


def render_audio(midi_file, mp3_file):
    cmd = f"timidity {midi_file} -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k {mp3_file}"
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
