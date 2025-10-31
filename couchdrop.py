import os
from time import sleep
import click
import config as Config
import helper as Helper
import gmail as Gmail

def _login(page):
    _, email = Config.getCouchdropAccount()
    page.goto("https://secure-auth.couchdrop.io/login")
    page.type("input[name='email']", email, delay=50)
    page.click("button")
    page.type("input[name='password']", os.getenv("PASSWORD"), delay=50)
    page.click("button")
    sleep(10)

@click.command()
def automate():
    id, _ = Config.getCouchdropAccount()
    wasabiOldAccounts = Config.getWasabiOldAccounts()
    wasabiCurrentAccounts = Config.getWasabiCurrentAccounts()
    with Helper.openBrowser(humanize=True) as page:
        _login(page)
    
        for i in range(len(wasabiOldAccounts)):
            wasabiOldBucket = wasabiOldAccounts[i]['bucket']
            wasabiOldAccessKey = wasabiOldAccounts[i]['access']
            wasabiOldSecretKey = wasabiOldAccounts[i]['secret']
            wasabiCurrentBucket = wasabiCurrentAccounts[i]['bucket']
            wasabiCurrentAccessKey = wasabiCurrentAccounts[i]['access']
            wasabiCurrentSecretKey = wasabiCurrentAccounts[i]['secret']
            page.goto(f"https://{id}.couchdrop.io/manage/connections")
            page.click("#page > div > div:nth-child(2) > div > div > :nth-child(2) > div")
            page.click("#sidebar-modal > :last-child > div > div > :nth-child(3) > div > :last-child > :nth-child(19) > div")
            page.click("#sidebar-modal > :last-child > div > div > :last-child > :last-child > div")
            page.type("#sidebar-modal > :last-child > div > div > :nth-child(3) > div > :nth-child(1) > :nth-child(2) > :last-child > div > div > input", wasabiOldBucket, delay=50)
            page.type("#sidebar-modal > :last-child > div > div > :nth-child(3) > div > :nth-child(1) > :last-child > :last-child > div > div > input", wasabiOldBucket, delay=50)
            page.click("#sidebar-modal > :last-child > div > div > :nth-child(3) > div > :nth-child(3) > div > div > div > div")
            page.click("#react-select-2-option-5 > div")
            page.type("input[label='Wasabi Bucket']", wasabiOldBucket, delay=50)
            page.type("input[label='Wasabi Access Key']", wasabiOldAccessKey, delay=50)
            page.type("input[label='Wasabi Access Key Secret']", wasabiOldSecretKey, delay=50)
            page.click("#sidebar-modal > :last-child > div > div > :last-child > :last-child > :last-child")
            sleep(5)
            page.goto(f"https://{id}.couchdrop.io/manage/connections")
            page.click("#page > div > div:nth-child(2) > div > div > :nth-child(2) > div")
            page.click("#sidebar-modal > :last-child > div > div > :nth-child(3) > div > :last-child > :nth-child(19) > div")
            page.click("#sidebar-modal > :last-child > div > div > :last-child > :last-child > div")
            page.type("#sidebar-modal > :last-child > div > div > :nth-child(3) > div > :nth-child(1) > :nth-child(2) > :last-child > div > div > input", wasabiCurrentBucket, delay=50)
            page.type("#sidebar-modal > :last-child > div > div > :nth-child(3) > div > :nth-child(1) > :last-child > :last-child > div > div > input", wasabiCurrentBucket, delay=50)
            page.click("#sidebar-modal > :last-child > div > div > :nth-child(3) > div > :nth-child(3) > div > div > div > div")
            page.click("#react-select-2-option-5 > div")
            page.type("input[label='Wasabi Bucket']", wasabiCurrentBucket, delay=50)
            page.type("input[label='Wasabi Access Key']", wasabiCurrentAccessKey, delay=50)
            page.type("input[label='Wasabi Access Key Secret']", wasabiCurrentSecretKey, delay=50)
            page.click("#sidebar-modal > :last-child > div > div > :last-child > :last-child > :last-child")
            sleep(5)
            page.goto(f"https://{id}.couchdrop.io/manage/schedules")
            page.click("#page > div > :first-child > :last-child > :last-child")
            page.click("#page > div > :last-child > div > :last-child > :last-child > div > div > div > div > div > div > :last-child > div > div > div")
            page.click("#sidebar-modal > :last-child > div > div > :nth-child(3) > div > :nth-child(4)")
            page.click("#sidebar-modal > :last-child > div > div > :last-child > :last-child > :last-child")
            page.click("#sidebar-modal > :last-child > div > div > :nth-child(3) > div > :last-child > :nth-child(2) > div > div > div > div")
            page.type("#sidebar-modal > :last-child > div > div > :nth-child(3) > div > div > :last-child > div > div > div > div > div > div > textarea", f"/{wasabiOldBucket}/anime/", delay=50)
            page.click("#sidebar-modal > :last-child > div > div > :last-child > :last-child > :last-child")
            page.click("#page > div > :last-child > div > :last-child > :last-child > div > div > div > div > div > div > :last-child > :last-child > div > div")
            page.click("#sidebar-modal > :last-child > div > div > :last-child > :last-child > :last-child")
            page.click("#sidebar-modal > :last-child > div > div > :nth-child(3) > div > :nth-child(4)")
            page.click("#sidebar-modal > :last-child > div > div > :last-child > :last-child > :last-child")
            page.click("#sidebar-modal > :last-child > div > div > :nth-child(3) > div > :last-child > :nth-child(2) > div > div > div > div")
            page.type("#sidebar-modal > :last-child > div > div > :nth-child(3) > div > :last-child > :nth-child(2) > div > div > div > div > div > div > textarea", f"/{wasabiCurrentBucket}/anime/", delay=50)
            page.click("#sidebar-modal > :last-child > div > div > :last-child > :last-child > :last-child")
            page.click("#page > div > div > div > div > :last-child > div")
            page.click("#couchdrop-body > :last-child > div > :last-child > div > :last-child")
            sleep(5)

@click.command()
def setup():
    id, email = Helper.getRandomEmail()

    with Helper.openBrowser(humanize=True) as page:
        page.goto("https://secure-auth.couchdrop.io/register")
        page.type("#email", email, delay=50)
        page.type("#password", os.getenv("PASSWORD"), delay=50)
        page.click("#accountNextButton")
        page.type("#email_confirm_code", Gmail.getCouchdropCode(), delay=50)
        page.click("#accountNextButton")
        page.type("#organisation_subdomain", id, delay=50)
        page.select_option("#hosted_storage_region", "Europe - Frankfurt")
        page.select_option("#registration_reason", "Other/I am not sure")
        page.select_option("#registration_reason_storage", "Amazon S3")
        page.select_option("#registration_reason_special", "Other")
        print("Solve the CAPTCHA in the browser, then press Enter here to continue...")
        input()
        page.click("#consent_ticked")
        page.click("#termsNextButton")
        sleep(10)
    Config.setCouchdropAccount(id, email)

@click.command()
def cleanup():
    id, _ = Config.getCouchdropAccount()
    with Helper.openBrowser(humanize=True) as page:
        _login(page)
        page.goto(f"https://{id}.couchdrop.io/manage/settings/billing")
        page.click("div.Button-module-button_secondary__M6GSy:nth-child(2)")
        page.type("#page > div > div > div > :nth-child(2) > div > :last-child > :last-child > div > input", "I understand", delay=75)
        page.click("#page > div > div > div > :nth-child(3) > div > :last-child")
        sleep(5)