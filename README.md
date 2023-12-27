# Usage
```
mkdir output

# Download and transcribe a bunch of sermons to a local folder ./output:
docker run --rm -v ./output:/output $(docker build -q .) download https://your-podcast-feed-url.xml

# Combine the transcribed sermons into one big txt file:
docker run --rm -v ./output:/output $(docker build -q .) combine https://your-podcast-feed-url.xml
```
