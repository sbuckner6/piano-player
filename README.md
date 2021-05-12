# piano-player

**Docker Instructions**

1. Install Docker: https://docs.docker.com/get-docker/
2. In the root project directory, run `docker image build -t piano-player .`
3. Run `docker run -d -p 5000:5000 piano-player`
4. Navigate to http://localhost:5000
5. Click the piano
6. If you don't hear anything or get an error, just refresh

**Non-Docker Instructions**

1. Install `ffmpeg`, `portaudio19-dev`, and `timidity` (e.g. via `apt` or `brew`, if you are on Windows, you may have to download the binaries and add them to your environment variables)
2. Ensure you have Python 3 installed
3. In the root project directory, run `python3 -m venv piano-player-env`
4. Run `source venv/bin/activate` (or `piano-player-env\Scripts\activate.bat` if you are on Windows)
5. Run `cd app`
6. Run `python main.py`
7. Navigate to http://localhost:5000
8. Click the piano
9. If you don't hear anything or get an error, just refresh
