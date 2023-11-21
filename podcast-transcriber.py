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

def main():
    feedurl = sys.argv[1]

    print("Downloading and parsing podcast...")
    parsed = podcastparser.parse(feedurl, urllib.request.urlopen(feedurl))

    OUTPUT_DIR = "/output"

    for episode in parsed["episodes"]:
        title = episode["title"]
        guid = urllib.parse.quote_plus(episode["guid"]) # urlencode as we'll be using it for file stuff
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

if __name__ == "__main__":
    main()