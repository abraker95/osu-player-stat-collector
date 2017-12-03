import time 
import urllib.request
from bs4 import BeautifulSoup


def getValue(value_str):
    value = []
    for ch in value_str.split(' ')[0]:
        if ch.isdigit() or ch == '.': value.append(ch)

    return float(''.join(value))


def getPlayerIdAtRank(rank):
    with urllib.request.urlopen('https://osu.ppy.sh/p/pp/?m=0&s=3&o=1&f=&page=' + str(int((rank - 1)/50) + 1)) as response:
        rankings_html = response.read()

    root         = BeautifulSoup(rankings_html, "lxml")
    rank_listing = root.find_all(class_=['row1p', 'row2p'])
    player_row   = rank_listing[int(rank%50) - 1]
    user_link    = player_row['onclick']
    user_id      = int(user_link.split('=')[1].replace('"', '').replace('/u/', ''))
    
    return user_id


class PlayerProfile():
    def __init__(self, player_id):
        self.stats = {}

        with urllib.request.urlopen('https://osu.ppy.sh/pages/include/profile-general.php?u=' + str(player_id) + '&m=0') as response:
            player_html = response.read()

        root = BeautifulSoup(player_html, "lxml")
        player_stats = root.find_all(class_='profileStatLine')

        for player_stat in player_stats:
            try:
                key = player_stat.text[: player_stat.text.find(': ')].strip()
                value = getValue(player_stat.text[player_stat.text.find(': ') + 2 :])
                self.stats[key] = value
            except: continue


    def getPerformance(self):            return self.stats['Performance']
    def getRankedScore(self):            return self.stats['Ranked Score']
    def getHitAccuracy(self):            return self.stats['Hit Accuracy']
    def getPlayCount(self):              return self.stats['Play Count']
    def getPlayTime(self):               return self.stats['Play Time']
    def getTotalScore(self):             return self.stats['Total Score']
    def getCurrentLevel(self):           return self.stats['Current Level']
    def getTotalHits(self):              return self.stats['Total Hits']
    def getMaxCombo(self):               return self.stats['Maximum Combo']
    def getTotalKudosuEarned(self):      return self.stats['Total Kudosu Earned']
    def getReplaysWatchedByOthers(self): return self.stats['Replays Watched by Others']



f = open('player_stats.csv', 'w')
f.write('rank,performance,hitcount,playcount,combo,playtime,rankedscore,totalscore\n')

for rank in range(1, 10000):
    try: 
        player = PlayerProfile(getPlayerIdAtRank(rank))
        player_performance = player.getPerformance()
        player_hitcount    = player.getTotalHits()
        player_playcount   = player.getPlayCount()
        player_combo       = player.getMaxCombo()
        player_playime     = player.getPlayTime()
        player_rankedscore = player.getRankedScore()
        player_totalscore  = player.getTotalScore()
        
        f.write(str(rank) + ',' + 
                str(player_performance) + ',' +
                str(player_hitcount) + ',' + 
                str(player_playcount) + ',' + 
                str(player_combo) + ',' + 
                str(player_playime) +  ',' + 
                str(player_rankedscore) +  ',' + 
                str(player_totalscore) +  '\n')
        
        print(str(rank) + ',' + str(player_performance))
        time.sleep(0.5)
    except: continue    

f.close()