from contextlib import contextmanager
import json
import os
import random
import string
from camoufox import Camoufox
from dotenv import load_dotenv
from playwright.sync_api import Page
import requests
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

@contextmanager
def openBrowser(block_images=True, humanize=False, headless=False):
    with Camoufox(
        block_images=block_images,
        i_know_what_im_doing=True,
        humanize=humanize,
        headless=headless
    ) as browser:
        page: Page = browser.new_page(reduced_motion="reduce")
        yield page

def uploadToImageKit(nextId, link):
    finalImagePath = os.path.expanduser(f"~/tmpfs/{nextId}.avif")
    os.system(f"ffmpeg -i {link.replace(".jpg", ".webp")} {finalImagePath}")
    imagekit = ImageKit(
        public_key=os.getenv("IMAGEKITPUBLIC"),
        private_key=os.getenv("IMAGEKITPRIVATE"),
        url_endpoint=os.getenv("IMAGEKITURL")
    )
    imagekit.upload_file(
        file=open(finalImagePath, "rb"),
        file_name=f"{nextId}.avif",
        options=UploadFileRequestOptions(
            use_unique_file_name=False
        )
    )
    os.system(f"rm {finalImagePath}")

def getAnimeJson():
    return requests.get(os.getenv("ANIMESJSON")).json()
def getGenresJson():
    return requests.get(os.getenv("GENRESJSON")).json()

def getTransformedGenres(fullGenres):
    genresJson = {name: id for id, name in getGenresJson().items()}
    genresIds = sorted([int(genresJson[genre]) for genre in fullGenres.split(" • ")])
    return " ".join(str(genre) for genre in genresIds)

def getLastSeason(original):
    json = getAnimeJson()
    for id, entry in json.items():
        if entry['o'] != original: continue
        lastSeasonKey, lastSeason = next(reversed(entry['s'].items()))
        return lastSeasonKey, lastSeason, id
    return None

def getNextIdForAnime():
    letters = string.ascii_lowercase + string.ascii_uppercase
    json = getAnimeJson()
    sorted_keys = sorted(json.keys(), key=lambda k: (k[0], int(k[1:])))
    id = sorted_keys[-1]
    prefix = id[0]
    nextId = int(id[1:]) + 1
    position = letters.find(prefix)
    if nextId > 99:
        nextId = 1
        prefix = letters[position + 1]
    return f"{prefix}{nextId}"

def getRandomString(lenght):
    characters = string.ascii_lowercase + string.digits
    return "".join(random.choice(characters) for _ in range(lenght))

def getRandomEmail():
    id = getRandomString(25)
    email = f"{os.getenv("EMAIL")}+{id}@gmail.com"
    return id, email

def downloadAnime():
    with open("anime.json", "r") as file:
        data = json.load(file)

    for anime in data:
        for season in data[anime]:
            for episode in data[anime][season]:
                number = episode.split("/")[7]
                quality = episode.split("/")[8]

                speed = "7000K"
                if quality == "720": speed = "11000K"
                elif quality == "1080": speed = "15000K"

                os.system(f"mkdir -p ~/tmpfs/{anime}/{season}/{number}")
                os.system(f"yt-dlp --limit-rate {speed} '{episode}' -o ~/tmpfs/{anime}/{season}/{number}/{quality}.mp4")