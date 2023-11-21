# Usage
```
mkdir output
docker run --rm -v ./output:/output $(docker build -q .) https://your-podcast-feed-url.xml
```
