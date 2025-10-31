import os
from time import sleep
import click
import mailtm as MailTm
import helper as Helper
import config as Config
from notifier import Notifier

def _login(page):
    page.goto("https://dash.bunny.net/auth/login")
    page.type("form.ng-untouched > bn-web-ui-input:nth-child(1) > div:nth-child(1) > label:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)", Config.getBunnyAccount(), delay=50)
    page.type("div.mt-3:nth-child(2) > bn-web-ui-input:nth-child(1) > div:nth-child(1) > label:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)", os.getenv("PASSWORD"), delay=50)
    page.click(".bn-button--full-width")
    sleep(5)


@click.command()
def setup():
    mail, account = MailTm.generate_mail()

    with Helper.openBrowser() as page:
        page.goto("https://dash.bunny.net/auth/register")
        page.click("body > bn-dashboard-root > bn-auth-layout > div > bn-auth-register > div > div:nth-child(1) > div > form > bn-web-ui-input > div > label > div.bn-form__container.show-on-hover__trigger > div > input")
        page.type("body > bn-dashboard-root > bn-auth-layout > div > bn-auth-register > div > div:nth-child(1) > div > form > bn-web-ui-input > div > label > div.bn-form__container.show-on-hover__trigger > div > input", account['address'], delay=50)
        page.click("body > bn-dashboard-root > bn-auth-layout > div > bn-auth-register > div > div:nth-child(1) > div > form > div:nth-child(2) > bn-web-ui-input > div > label > div.bn-form__container.show-on-hover__trigger > div > input")
        page.type("body > bn-dashboard-root > bn-auth-layout > div > bn-auth-register > div > div:nth-child(1) > div > form > div:nth-child(2) > bn-web-ui-input > div > label > div.bn-form__container.show-on-hover__trigger > div > input", os.getenv("PASSWORD"), delay=50)
        page.click("body > bn-dashboard-root > bn-auth-layout > div > bn-auth-register > div > div:nth-child(1) > div > form > div.mt-3.row.g-0 > div > bn-web-ui-checkbox > div > label > div.bn-checkbox__checkbox.animate")
        page.click("body > bn-dashboard-root > bn-auth-layout > div > bn-auth-register > div > div:nth-child(1) > div > form > div:nth-child(6) > button")
        confirmationLink = MailTm.getBunnyConfirmationEmail(mail, account)
        sleep(5)
        page.goto(confirmationLink)
        sleep(5)
        Config.setBunnyAccount(account['address'])
    
    
    with Helper.openBrowser() as page:
        _login(page)
        for wasabiCurrentAccount in Config.getWasabiCurrentAccounts():
            page.goto("https://dash.bunny.net/cdn/add")
            page.type(".bn-input--md > label:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(2)", wasabiCurrentAccount['bucket'], delay=50)
            page.type("bn-web-ui-card.mt-4:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2) > bn-web-ui-input:nth-child(1) > div:nth-child(1) > label:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(2)", f"https://s3.eu-central-2.wasabisys.com/{wasabiCurrentAccount['bucket']}", delay=50)
            page.click("bn-web-ui-card.mt-4:nth-child(3) > div:nth-child(1) > div:nth-child(2) > bn-web-ui-radio-tabs:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(2) > label:nth-child(1)")
            page.click(".btn-primary")
            sleep(5)
        page.goto("https://dash.bunny.net/cdn")
        sleep(10)
        count = page.locator(".bn-table--normal > tbody:nth-child(2) > tr").count()
        links = []
        buckets = []
        for i in range(1, count+1):
            entry = page.locator(f"tr.has-context--:nth-child({i}) > td:nth-child(1) > div:nth-child(1) > a")
            links.append(entry.get_attribute("href"))
            buckets.append(entry.inner_text())
        for i in range(len(links)):
            page.goto("https://dash.bunny.net" + links[i] + "/security/s3-authentication")
            page.click(".bn-checkbox__checkbox")
            access, secret = None
            for wasabiCurrentAccount in Config.getWasabiCurrentAccounts():
                if wasabiCurrentAccount['bucket'] != buckets[i]: continue
                access = wasabiCurrentAccount['access']
                secret = wasabiCurrentAccount['secret']
                break
            sleep(2)
            page.type(".bn-s3-auth-form > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > bn-web-ui-input:nth-child(1) > div:nth-child(1) > label:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(2)", access, delay=50)
            page.type(".ps-xl-5 > bn-web-ui-input:nth-child(1) > div:nth-child(1) > label:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(2)", secret, delay=50)
            page.type("input.bn-input__input:nth-child(1)", "eu-central-2", delay=50)
            page.click(".bn-button__item-style--primary")
            sleep(5)
    notifier = Notifier()
    urls = "".join(f"\"https://{login['bucket']}.b-cdn.net/anime\"," for login in Config.getWasabiCurrentAccounts())
    notifier.send_notification("NIGGA UPDATE YOUR URLS")
    notifier.send_notification(f"```\nexport const urls = [\n{urls}\n]```")

# @click.command()
# def cleanup():
#     with Helper.openBrowser() as page:
#         _login(page)
#         page.goto("https://dash.bunny.net/account/settings/close")
