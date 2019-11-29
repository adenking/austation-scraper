from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import csv
import tqdm

def Download_Data(url):
    request = requests.get("https://stats.austation.net/deaths/" + str(url))
    soup = BeautifulSoup(request.content,'html.parser')
    death_number = soup.find_all('small')[0].get_text()
    username = soup.find_all('small')[1].get_text()
    username = username.strip()
    player_name = soup.find('small').next_sibling.string[:-1]
    player_name = player_name.strip()
    rank = soup.find('h3', {'class': 'card-header'}, text='Rank')
    try:
        rank_tag = rank.parent
        rank = rank_tag.findNext('div').get_text()
        rank = rank.join(mystring.split())
    except:
        rank = 'none'
    cause_of_death = soup.find('h3', {'class': 'card-header'}, text='Cause of Death')
    try:
        cause_of_death_tag = cause_of_death.parent
        cause_of_death = cause_of_death_tag.findNext('div', {'class': 'card-body h4'}).get_text()
        cause_of_death = cause_of_death.strip()
    except:
        cause_of_death = 'none'
    location_of_death = soup.find_all('div', {'class': 'card-body h4'})[3].get_text()
    location_of_death = location_of_death.strip()
    location_of_death = location_of_death[:-27]
    brute_damage = soup.find('span', {'class': 'badge-brute'}).get_text()
    brain_damage = soup.find('span', {'class': 'badge-brain'}).get_text()
    fire_damage = soup.find('span', {'class': 'badge-fire'}).get_text()
    oxy_damage = soup.find('span', {'class': 'badge-oxy'}).get_text()
    tox_damage = soup.find('span', {'class': 'badge-tox'}).get_text()
    clone_damage = soup.find('span', {'class': 'badge-clone'}).get_text()
    stamina_damage = soup.find('span', {'class': 'badge-stamina'}).get_text()
    murder_suspect = soup.find('h3', {'class': 'card-header bg-danger text-white'})
    try:
        murder_tag = murder_suspect.parent
        murder_suspect = murder_tag.findNext('div').get_text()
        murder_suspect = murder_suspect.strip()
    except:
        murder_suspect = 'none'
    lines_data = [death_number, username, player_name, rank, cause_of_death, brute_damage, brain_damage, fire_damage, oxy_damage, tox_damage, clone_damage, stamina_damage, murder_suspect]
    lines = ",".join(lines_data)
    with open('deaths.csv', 'a') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE, quotechar='', escapechar=' ')
        writer.writerow([lines])

if __name__ == '__main__':
    pool = Pool(processes=10)
    for _ in tqdm.tqdm(pool.imap_unordered(Download_Data, range(25915)), total=25915):
        pass
