# Victonime Bot

A bot used to manage the infrastructure of the Russian website [Victonime](https://victonime.vercel.app).

> ⚠️ **Disclaimer:**  
> The code is provided *as is*. The owner assumes no responsibility.  
> This bot is intended for internal use only.

---

## 🧩 Prerequisites

Before running the bot, ensure the following setup is complete:

### 1. `.env` File

##### PASSWORD
Used for creating all the neccessary account

##### EMAIL
Only the part before @gmail.com \
Will be used to register some accounts

##### GENRESJSON 
Link to genres that should return smth like \
```json
{
    "1": "Экшен",
    "2": "Приключения",
    "3": "Комедия"
}
```
_Note: this is only an example_

##### TELEGRAMTOKEN
A telegram bot token that is usualy generated with BotFather \
Used to sent notifications for manual stuff

##### IMAGEKITPUBLIC
As the name says its the public key for ImageKit

##### IMAGEKITPRIVATE
As the name says its the private key for ImageKit

##### IMAGEKITURL
Thats the url enpoint for ImageKit \
_Note: All entries with `IMAGEKIT` are used for uploading posters for anime_

##### ANILIRBIAUSERNAME
Username to login into Anilibria (to avoid ads)

##### ANILIRBRIAPASSWORD
Passowrd to login into Anilibria