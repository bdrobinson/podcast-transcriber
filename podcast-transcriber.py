import requests
import shutil
import podcastparser
import urllib.request
import urllib.parse
import sys
import pprint
import os
from os import path
import subprocess
import json

OUTPUT_DIR = "/output"

def main():
    command = sys.argv[1]
    if command == "download":
        download(sys.argv[2])
    elif command == "combine":
        combine(sys.argv[2])

def combine(feedurl):
    print("Downloading and parsing podcast...")
    parsed = podcastparser.parse(feedurl, urllib.request.urlopen(feedurl))
    sermons = []
    for episode in parsed["episodes"]:
        title = episode["title"] 
        guid = parse_guid(episode["guid"])
        description = episode["description"]
        published_ts = episode["published"]
        preacher = episode["itunes_author"]
        text_path = path.join(OUTPUT_DIR, guid, f"{guid}.txt")
        if os.path.exists(text_path):
            with open(text_path, "r") as f:
                text = f.read()
                sermons.append({
                    "title": title,
                    "description": description,
                    "preacher": preacher,
                    "published_timestamp": published_ts,
                    "transcript": text
                })
    with open(path.join(OUTPUT_DIR, "sermons.json"), 'w') as f:
        f.write(json.dumps(sermons))

def download(feedurl):
    print("Downloading and parsing podcast...")
    parsed = podcastparser.parse(feedurl, urllib.request.urlopen(feedurl))

    for episode in parsed["episodes"]:
        title = episode["title"]
        guid = parse_guid(episode["guid"]) # urlencode as we'll be using it for file stuff
        url = episode["enclosures"][0]["url"]
        print(f"Handling episode \"{title}\" with guid {guid}")


        
        output_directory_path = path.join(OUTPUT_DIR, guid)

        guid_already_handled = os.path.exists(path.join(output_directory_path, f"{guid}.json"))
        if guid_already_handled:
            print("Already handled, skipping")
            continue
        
        print("Not already handled.")
        shutil.rmtree(output_directory_path, ignore_errors=True)
        transcribe_episode(guid, url, output_directory_path)

def transcribe_episode(guid, url, output_directory_path):
    audio_file_location = path.join("/tmp", guid)
    print("Downloading...")
    download_file(url, audio_file_location)
    print("Transcribing...")
    transcribe_audio(audio_file_location, output_directory_path)

    os.remove(audio_file_location)

def download_file(url, destination):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(destination, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

def transcribe_audio(audio_file_path, output_dir):
    subprocess.run(["whisper", audio_file_path, "--model", "tiny.en", "-o", output_dir, "--verbose", "False"])

def parse_guid(raw_guid):
    return urllib.parse.quote_plus(raw_guid).replace(".", "_")

if __name__ == "__main__":
    main()