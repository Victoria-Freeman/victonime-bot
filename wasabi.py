import os
from time import sleep
import click
from faker import Faker
import config as Config
import rclone as Rclone
import helper as Helper
import gmail as Gmail

def _login(page, email):
    page.goto("https://console.wasabisys.com/login")
    page.fill("#signInAcctName", email)
    sleep(.5)
    page.fill("#signInPass", os.getenv("PASSWORD"))
    sleep(.5)
    page.click("#signInBtn")
    sleep(10)

@click.command()
def setup():
    fake = Faker()

    Config.setWasabiCurrentLoginsAsOld()
    for _ in range(Config.getWasabiAccountsCount()):
        id, email = Helper.getRandomEmail()
        with Helper.openBrowser() as page:
            page.goto("https://wasabi.com/try-free")
            page.fill("#firstName", fake.first_name())
            page.fill("#lastName", fake.last_name())
            page.fill("#phone", fake.phone_number())
            page.fill("#companyName", Helper.getRandomString(15))
            page.fill("#email", email)
            page.select_option("#country", "Germany")
            page.select_option("#storage", "Less than 25 TB")
            page.select_option("#source", "Other")
            page.check("#resell")
            page.check("#consentToShare")
            page.click("#main-content > div.MuiBox-root.css-0 > div > div > div > div > div > div:nth-child(2) > div > div > form > div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-3.MuiGrid-spacing-lg-4.css-l26694 > div:nth-child(12) > button")
            confirmationLink = Gmail.getWasabiConfirmationLink(email)
            page.goto(confirmationLink)
            sleep(.5)
            page.type("#page\:fm\:password", os.getenv("PASSWORD"), delay=25)
            sleep(.5)
            page.type("#page\:fm\:confirmPassword", os.getenv("PASSWORD"), delay=25)
            sleep(.5)
            page.click("#page\:fm\:login")
            page.click("input[name='page:fm:btnTrial2']")
            sleep(2)
            _login(page, email)
            page.goto("https://console.wasabisys.com/file_manager")
            page.evaluate("document.head.insertAdjacentHTML('beforeend','<style>.appcues{display:none!important;}</style>')")
            sleep(5)
            page.click("#createBucketBtn")
            sleep(.5)
            page.type("input[name='Bucket']", id, delay=25)
            page.evaluate("const btn=document.querySelector('#mui-component-select-Region');btn.focus();const ev=new KeyboardEvent('keydown',{key:'Enter',code:'Enter',bubbles:true,cancelable:true,});btn.dispatchEvent(ev);")
            page.click("#menu-Region > div.MuiPaper-root.MuiMenu-paper.MuiPopover-paper.MuiPaper-elevation8.MuiPaper-rounded > ul > li:nth-child(10)")
            for _ in range(5):
                page.click("#bucketWizNext")
                
            page.click("button[data-testid='createBucket']")
            sleep(10)
            page.goto("https://console.wasabisys.com/access_keys")
            page.click("#createAccessKey")
            sleep(.5)
            page.click("#createKeysModal")
            access = page.locator("#accessKeyValue-label").text_content()
            page.click("#showSecretKey")
            secret = page.locator("#secretKeyValue-label").text_content()
            print(access)
            print(secret)
            Config.addWasabiAccount(id, email, access, secret)
    Rclone.setup()

@click.command()
def upload():
    newestWasabiAccount = Config.getWasabiLatestAccount()
    os.system(f"rclone copy ~/tmpfs {newestWasabiAccount['bucket']}:{newestWasabiAccount['bucket']}/anime/ --progress")
    os.system("rm -rf ~/tmpfs/*")

@click.command()
def cleanup():
    for account in Config.getWasabiOldAccounts():
        with Helper.openBrowser() as page:
            _login(page, account['email'])
            page.goto("https://console.wasabisys.com/profile")
            accountId = page.text_content("#acctId")
            page.click("#vertical-tab-12")
            page.click("#deleteAcctBtn")
            page.type("#delete-account-form-deleteAcctIdField", accountId, delay=50)
            page.type("#delete-account-form-deleteAcctPassField", os.getenv("PASSWORD"))
            page.evaluate("const btn=document.querySelector('#delete-account-form-deleteAcctReasonField');btn.focus();const ev=new KeyboardEvent('keydown',{key:'Enter',code:'Enter',bubbles:true,cancelable:true,});btn.dispatchEvent(ev);")
            page.click("div.MuiPaper-root:nth-child(3) > ul:nth-child(1) > li:nth-child(8)")
            page.click("#delete-account-form-container > :nth-child(6) > label > span:nth-child(1) > span > input")
            page.click("#delete-account-form-container > :nth-child(7) > button")
            sleep(5)
