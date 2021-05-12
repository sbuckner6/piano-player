# Piano Player

## Overview

A procedural music generator created in Python that arranges and plays classical, blues, waltz, and 12-tone pieces using the Fibonacci sequence.

## Docker Instructions

1. Install Docker: https://docs.docker.com/get-docker/
2. In the root project directory, run `docker image build -t piano-player .`
3. Run `docker run -d -p 5000:5000 piano-player`
4. Navigate to http://localhost:5000
5. Click the piano
6. If you don't hear anything or get an error, just refresh (I'm still investigating this bug)

## Non-Docker Instructions

1. Install `ffmpeg`, `portaudio19-dev`, and `timidity` (e.g. via `apt` or `brew`, if you are on Windows, you may have to download the binaries and add them to your environment variables)
2. Ensure you have Python 3 installed
3. In the root project directory, run `python3 -m venv piano-player-env`
4. Run `source venv/bin/activate` (or `piano-player-env\Scripts\activate.bat` if you are on Windows)
5. Run `pip install -r requirements.txt`
6. Run `cd app`
7. Run `python main.py`
8. Navigate to http://localhost:5000
9. Click the piano
10. If you don't hear anything or get an error, just refresh (I'm still investigating this bug)
