
import json
import os
from time import sleep
import helper as Helper
import config as Config
import wasabi as Wasabi

import click

from notifier import Notifier


def checkResponse(response, linksList):
    url = response.url
    if ".m3u8" not in url or url in linksList: return
    linksList.append(url)
    print(url)

def _getEpisodesAmount(page):
    for _ in range(10):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        sleep(.3)
    sleep(1)
    return page.locator("div.pa-4:nth-child(1) > div").count()

def _getEpisodesLinks(page, start, end):
    episodesList = []
    for i in range(start, end, -1):
        episode = page.locator(f"div.pa-4:nth-child(1) > :nth-child({i}) > a").get_attribute("href")
        episodesList.append(episode)
    return episodesList

def _login(page):
    page.goto("https://anilibria.top/app/auth/login")
    sleep(1)
    page.fill('input[name="login"]', os.getenv("ANILIRBIAUSERNAME"))
    page.fill('input[name="current-password"]', os.getenv("ANILIRBRIAPASSWORD"))
    page.click("#__nuxt > div > div.v-application.v-theme--dark.v-layout.v-layout--full-height.v-locale--is-ltr > div > div > div > div.v-row.v-row--no-gutters.v-row--dense.justify-center.h-100 > div.v-col-md-8.v-col-lg-6.v-col-10 > div > div.d-flex.flex-column.text-center.align-center > div.v-card.v-card--flat.v-theme--dark.bg-transparent.v-card--density-default.v-card--variant-elevated.py-4 > div.mt-2 > button")
    sleep(4)

def _parseSeason(link):
    with Helper.openBrowser(headless=True) as page:
        fullM3u8Links = []
        page.on("response", lambda response: checkResponse(response, fullM3u8Links))
        _login(page)
        page.goto(link)
        sleep(5)
        original = page.text_content("div.mb-3:nth-child(2)")
        episodes = _getEpisodesAmount(page)
        print(episodes)
        lastSeasonId, lastSeason, animeId = Helper.getLastSeason(original)
        if animeId and Helper.getAnimeJson()[animeId]['u'] == Config.getWhereToUpload():
            episodesLinks = _getEpisodesLinks(page, episodes - lastSeason['e'], 0)
        else: episodesLinks = _getEpisodesLinks(page, episodes, 0)
        for link in episodesLinks:
            for i in range(3):
                page.evaluate(codeForQuality[i])
                page.goto("https://anilibria.top" + link)
                page.click(".v-btn")
                sleep(2)
        page.wait_for_load_state("networkidle")
        m3u8Links = [link.split("?")[0] for link in fullM3u8Links]
        data = {
            Helper.getNextIdForAnime() if not animeId else animeId: {
                "s1" if not lastSeasonId else lastSeasonId: m3u8Links
            }
        }
        with open("anime.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return animeId, lastSeasonId, episodes


codeForQuality = [
    'localStorage.setItem("app.settings", JSON.stringify({video: {selectedTrack: "HLS_480"}}))',
    'localStorage.setItem("app.settings", JSON.stringify({video: {selectedTrack: "HLS_720"}}))',
    'localStorage.setItem("app.settings", JSON.stringify({video: {selectedTrack: "HLS_1080"}}))'
]

@click.command()
@click.argument("link", required=True)
def parse_season(link):
    _parseSeason(link)

@click.command()
@click.argument("link", required=True)
def update(link):
    animeId, lastSeasonId, episodes = _parseSeason(link)
    Helper.downloadAnime()
    Wasabi.upload.callback()
    notifier = Notifier()
    notifier.send_notification(f"NIGGA UPDATE {animeId} > {lastSeasonId} > \"e\" TO {episodes}")

@click.command()
@click.argument("link", required=True)
def new_anime(link):
    with Helper.openBrowser(block_images=False) as page:
        page.goto(link)
        title = page.text_content(".text-autosize")
        original = page.text_content("div.mb-3:nth-child(2)")
        year = page.text_content("div.d-flex:nth-child(4) > div:nth-child(2)")
        genres = Helper.getTransformedGenres(page.text_content("div.fz-80:nth-child(4) > div:nth-child(3) > div:nth-child(2)"))
        episodes = _getEpisodesAmount(page)
        newId = Helper.getNextIdForAnime()

        page.goto(f"https://myanimelist.net/anime.php?q={original}", wait_until="domcontentloaded")
        page.click("#accept-btn")
        page.goto(page.get_attribute(".js-categories-seasonal > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > div:nth-child(1) > a:nth-child(2)", "href") + "/pics")

        hrefs = [a.get_attribute("href") for a in page.locator(".rightside > table:nth-child(6) > tbody > tr > td:not([colspan=\"2\"]) > :nth-child(1) > a").all()]
        pirctureLink = hrefs[int(input(f"({len(hrefs)}) Choose a poster: ")) - 1]
        Helper.uploadToImageKit(newId, pirctureLink)

        notifier = Notifier()
        notifier.send_notification(f"""```json
"{newId}": {{
    "t": "{title}",
    "o": "{original}",
    "p": "{newId}",
    "g": "{genres}",
    "y": "{year}",
    "u": {Config.getWhereToUpload()},
    "s": {{
        "s1": {{
            "t": "1 сезон",
            "e": {episodes}
        }}
    }}
}},
        ```""")
        parse_season.callback(link)
        Helper.downloadAnime()
        Wasabi.upload.callback()