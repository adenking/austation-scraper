

from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import csv
import tqdm

def Download_Data(url):
    request = requests.get("https://stats.austation.net/deaths/" + str(url))
    soup = BeautifulSoup(request.content,'html.parser')
    try:
        page_status = soup.find('span', {'class': 'badge badge-dam badge-brute'}, text='BRU').get_text()
    except:
        page_status = None
    if page_status == 'BRU':
        pass
    else:
        death_id = url

        username = soup.find('h2')
        username = username.get_text()[10:].strip().split('/')
        username, player_name = username[0], username[1]

        rank = soup.find('h3', {'class': 'card-header'}, text='Rank')
        rank = rank.findNext('div', {'class': 'card-body h4'})
        try:
            traitor = rank.findNext('span').get_text()
            traitor = True
        except:
            traitor = False
        if traitor == True:
            rank = rank.get_text()[:-8].strip()
        else:
            rank = rank.get_text().strip()
        
        cause_of_death = soup.find('h3', {'class': 'card-header'}, text='Cause of Death')
        cause_of_death = cause_of_death.findNext('div', {'class': 'card-body h4'})

        brute_damage = soup.find('span', {'class': 'badge badge-dam badge-brute'})

        brute_damage = soup.find('span', {'class': 'badge badge-dam badge-brain'})

        fire_damage = soup.find('span', {'class': 'badge badge-dam badge-fire'})
 
        oxy_damage = soup.find('span', {'class': 'badge badge-dam badge-oxy'})

        tox_damage = soup.find('span', {'class': 'badge badge-dam badge-tox'})

        clone_damage = soup.find('span', {'class': 'badge badge-dam badge-clone'})

        stamina_damage = soup.find('span', {'class': 'badge badge-dam badge-stamina'})

        try:
            murder_suspect = soup.find('h3', {'class': 'card-header'}, text='Murder Suspect')
            murder_suspect = murder_suspect.findNext('div', {'class': 'card-body h4'}).get_text().strip().split('/')
            murder_suspect_username, murder_suspect_player_name = murder_suspect
        except:
            murder_suspect_username = None
            murder_suspect_player_name = None

        with open('deaths.csv', 'a') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([death_number, username, player_name, rank, cause_of_death, brute_damage, brain_damage, fire_damage, oxy_damage, tox_damage, clone_damage, stamina_damage, murder_suspect_username, murder_suspect_player_name])

if __name__ == '__main__':
    pool = Pool(processes=20)
    for _ in tqdm.tqdm(pool.imap_unordered(Download_Data, range(25915)), total=25915):
        pass
