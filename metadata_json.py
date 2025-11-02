from math import ceil
import os
import json
from BunnyCDN.Storage import Storage
from BunnyCDN.CDN import CDN
from tqdm import tqdm
import config as Config

storageName, storageKey = Config.getBunnyStorageData()
accountKey, pullzoneId = Config.getBunnyAccountAPIKeys()

storage = Storage(storageKey, storageName)
cdn = CDN(accountKey)

_metadata = None

def metadata():
    global _metadata
    if _metadata: return _metadata
    with open("metadata.json", "r") as file:
        _metadata = json.load(file)
    return _metadata

def write(data, name):
    with open(f"jsons/metadata_{name}.json", "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def toArray():
    array = []
    for anime_id, anime_data in metadata().items():
        anime_entry = {"id": anime_id}
        anime_entry.update(anime_data)
        array.append(anime_entry)
    write(array, "array")

def sortByGenresId():
    data = {}
    for id in metadata():
        for genreId in metadata()[id]['g'].split(" "):
            if genreId not in data: data[genreId] = {}
            data[genreId][id] = metadata()[id]
    for id in data:
        write(data[id], f"genre_{id}")
    
def sortByPages():
    items = list(metadata().items())
    page_size = 18
    total_pages = ceil(len(items) / page_size)

    for page in tqdm(range(total_pages), desc="Generating pages", unit="page"):
        array = []
        start = page * page_size
        end = start + page_size
        for animeId, anime in items[start:end]:
            animeEntry = {"id": animeId}
            animeEntry.update(anime)
            array.append(animeEntry)
        write({"animes": array, "meta": {
            "showPrev": False if page+1 == 1 else True,
            "showNext": True if page+1 != total_pages else False
        }}, page+1)
    
def sortByAnimes():
    for id, anime in tqdm(metadata().items(), desc="Generating json for each anime", unit="anime"):
        anime.update({"id": id})
        write(anime, id)

def upload():
    files = os.listdir("jsons")
    storage.PutFile("metadata.json", "metadata.json")
    for file in tqdm(files, desc="Uploading files", unit="file"):
        storage.PutFile(file, file, "jsons")
    cdn.PurgePullZoneCache(pullzoneId)

def sync():
    os.system("rm metadata.json")
    storage.DownloadFile("metadata.json")

def setup():
    toArray()
    sortByGenresId()
    sortByPages()
    sortByAnimes()
    upload()

def addEntry(id, title="", original="", poster="", genres="", years="", whereToUpload="", seasons=""):
    global _metadata
    if id in metadata():
        title = metadata()[id]['t']
        original = metadata()[id]['o']
        poster = metadata()[id]['p']
        genres = metadata()[id]['g']
        years = metadata()[id]['y']
        whereToUpload = metadata()[id]['u']
        seasons = metadata()[id]['s']
        del metadata()[id]
    entry = {
        "t": title,
        "o": original,
        "p": poster,
        "g": genres,
        "y": years,
        "u": whereToUpload,
        "s": seasons
    }
    data = {id: entry, **metadata()}
    with open("metadata.json", "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    _metadata = None
    setup()