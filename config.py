from pathlib import Path
import yaml

_config = None

def config():
    global _config
    if _config: return _config
    with open("config.yaml", "r") as file:
        _config = yaml.safe_load(file)
    return _config

def write():
    with open("config.yaml", "w") as file:
        yaml.dump(config(), file, sort_keys=False)

def getWasabiAccountsCount():
    return config()['wasabi']['accounts']

def addWasabiAccount(id, email, access, secret):
    config()['wasabi']['logins'].append({
        "email": email,
        "access": access,
        "secret": secret,
        "bucket": id
    })
    write()

def getWasabiOldAccounts():
    return config()['wasabi']['oldLogins']

def getWasabiCurrentAccounts():
    return config()['wasabi']['logins']

def getWasabiLatestAccount():
    return config()['wasabi']['logins'][-1]

def getCouchdropAccount():
    return config()['couchdrop']['id'], config()['couchdrop']['email']

def setCouchdropAccount(id, email):
    config()['couchdrop'] = {
        "email": email,
        "id": id
    }
    write()

def getBunnyAccount():
    return config()['bunny']['login']['email']

def getBunnyOldAccount():
    return config()['bunny']['oldLogin']['email']

def setBunnyAccount(email):
    config()['bunny']['oldLogin'] = config()['bunny']['login']
    config()['bunny']['login'] = {
        "email": email
    }
    write()

def setWasabiCurrentLoginsAsOld():
    config()['wasabi']['oldLogins'] = []
    for login in config()['wasabi']['logins'].copy():
        config()['wasabi']['oldLogins'].append(login.copy())
    write()

def getWhereToUpload():
    return len(getWasabiCurrentAccounts()) - 1

def generateRcloneConfig():
    text = ""
    for login in config()['wasabi']['logins'].copy():
            text += f"""
[{login['bucket']}]
type = s3
provider = Wasabi
access_key_id = {login['access']}
secret_access_key = {login['secret']}
region = eu-central-2
endpoint = s3.eu-central-2.wasabisys.com
acl = private
            """
    config_dir = Path.home() / ".config" / "rclone"
    config_dir.mkdir(parents=True, exist_ok=True)

    config_file = config_dir / "rclone.conf"
    with config_file.open("w", encoding="utf-8") as file:
        file.write(text)