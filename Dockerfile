FROM python:3.9.0

# install deepspeech
# RUN pip3 install deepspeech
# RUN curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
# RUN curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer

RUN apt update -y && apt install ffmpeg -y
RUN pip install openai-whisper
RUN pip install podcastparser

COPY transcribe-url.sh ./transcribe-url.sh

# run model
ENTRYPOINT ["./transcribe-url.sh"]