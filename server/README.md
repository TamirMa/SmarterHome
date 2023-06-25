
# Smarter Home

The best Python-FastAPI service for controlling your Smart Home using RestAPI. 

Your smart home deserves a FastAPI for controlling it. Something that you won't be able to do when using openHAB or HomeAssistant

## But why?
It all started when I had to control all my devices on Shabbat. I wanted to have a scheduler controlling all my `lights/curtains/oven/dishwasher/..` and HA/openHAB had nothing to offer for that. So I've built this module for controlling all your devices through a FastAPI + Allowing to schedule tasks that will sync with Shabbat times each week.

#### Controlling
* AEG / Electrolux (Ovens - pyelectroluxconnect)
* Home Connect (Dishwasher)
* Tuya devices (lights, sockets, curtains, ACs, ..)
* Shelly devices (lights, sockets)
* BroadLink RF controller (fans, IR, ..)
* Samsung SmartThings (TVs, ..)
* Yeelight (LEDs)

#### Get all items

```http
  POST /devices/{device_id}/state
```

| Parameter   | Type     | Description                |
| :---------- | :------- | :--------------------------------- |
| `device_id` | `string` | **Required**. The device you want to control |
| `light_state` | `string` | **Required**. 'on' / 'off' |

#### Get item

```http
  POST /dishwasher/{device_id}/start
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `device_id`      | `string` | **Required**. The id of the dishwasher |


## Installation

In order to run the service you need to prepare 3-4 files:

* .env
```
TELEGRAM_BOT_TOKEN={YOUR TELEGRAM BOT TOKEN - keep empty for skipping the bot}
TELEGRAM_ALLOWED_LIST={IDS OF YOUR TELEGRAM ACCOUNTS - keep empty for skipping the bot)
CONNECTION_PARAMS_FILE=".connection_params.json"
DEVICES_FILE=".devices.json"
SERVER_PORT=9000
SERVER_IP=127.0.0.1
```

* .connection_params
! If you are missing one of those devices, you can simply remove it from the file !
```
{
    "AEG": {
        "username": "{ACCOUNT_EMAIL}",
        "password": "{ACCOUNT_PASSWORD}"
    },
    "Tuya": {
        "devices_json_path": ".tuya_devices.json"
    },
    "HomeConnect": {
        "clientId": "{YOUR_HOMECONNECT_CLIENT_ID}",
        "clientSecret": "{YOUR_HOMECONNECT_CLIENT_SECRET}",
        "redirectURI": "{YOUR_HOMECONNECT_REDIRECT_URL}"
    },
    "SmartThings": {
        "token": "{SMART_THINGS_TOKEN}"
    }
}
```

* .devices.json
```
[
    {
        "connection": "AEG",
        "name": "AEGOven",
        "type": "Oven",
        "connection_id": "11XXXX32-443XXXXXXXB3"
    }
]
```

* .tuya_devices.json

This is the output file of the command:
`python3 -m tinytuya wizard`

Looks like this:
```
[
    {
        "name": "Kitchen Lights",
        "id": "brt5c1d44GG6cb5ta17y5i9",
        "key": "1dFFFFFFFFFF0aeb",
        "mac": "70:58:e8:f6:60:34",
        "category": "wnykq",
        "product_name": "Smart remote with sensors",
        "ip": "10.0.0.118",
        "version": "3.3"
    },
    {
        ...
    },
    ...
]
```
## Run Locally

Run the command

```
python3 start.py
```

## Authors

- [@tamirma](https://www.github.com/tamirma)

