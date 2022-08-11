import requests
import json
import time

defi_names = ('Algofi', 'Tinyman', 'HumbleSwap', 'Folks')


def pretty(dict):

    pretty = json.dumps(dict, indent=4, sort_keys=True)
    print(pretty)


def get_defi_app_ids():
    global defi_mapping

    # save time getting list of app_ids from the algoexplorer application tab, as of today 4 pages
    # (https://algoexplorer.io/applications)

    def _get_verified_applications():

        try:
            response = requests.get(
                'https://indexer.algoexplorerapi.io/rl/v1/applications?limit=40' +
                page,
                timeout=5)
            response.raise_for_status()
            return json.loads(response.content)
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    cursors = [
        '',
        '&cursor=GUYDUNZXGYYTOOJVGU4Q====',
        '&cursor=GUYDUNZYGUYDSOJXGU2Q====',
        '&cursor=GEYDAORUGY2TQMJYGI3DA===']

    defi_mapping = {}

    for page in cursors:

        time.sleep(0.1)
        raw_verified_applications = _get_verified_applications()
        applications = raw_verified_applications.get('applications')

        for app in applications:
            # verified? avoiding scams
            if app["verification"]["score"] >= 50:
                # getting only defis
                app_name = app["verification"]["name"]
                if app_name.startswith(defi_names):
                    app_name = app_name.split()[0]
                    # settings application_ids as keys for faster lookup per
                    # iteration
                    defi_mapping[app["application-id"]] = app_name

    # edge case for HumbleSwap protocol:
    defi_mapping["784340682"] = 'HumbleSwap'


get_defi_app_ids()
