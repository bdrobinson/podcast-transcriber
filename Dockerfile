FROM python:3.9.0

# install deepspeech
# RUN pip3 install deepspeech
# RUN curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
# RUN curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer

RUN apt update -y && apt install ffmpeg -y
RUN pip install openai-whisper
RUN pip install podcastparser
RUN pip install requests

COPY podcast-transcriber.py ./podcast-transcriber.py

# run model
ENTRYPOINT ["python", "./podcast-transcriber.py"]