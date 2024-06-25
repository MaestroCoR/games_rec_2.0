import requests
import json


def get_steam_apps():
    response = requests.get(
        'http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json')
    if response.status_code == 200:
        return response.json()['applist']['apps']
    else:
        return None


apps_list = get_steam_apps()
if apps_list:
    with open('steam_apps_list.json', 'w', encoding='utf-8') as file:
        json.dump(apps_list, file, ensure_ascii=False, indent=4)
    print(f'Записано {len(apps_list)} додатків у файл "steam_apps_list.json".')
else:
    print('Не вдалося отримати список додатків з Steam.')
