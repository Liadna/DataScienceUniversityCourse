import urllib
import time
import os

userhome = os.path.expanduser('~')
desktop = userhome + '/Desktop/'
fileName = desktop + '/FootballResultsGraph.csv'
fileNameAll = desktop + '/AllFootballResults.csv'
dic = {}
with open(fileName,'w') as fid:
    fid.write("Wins" + ',' + "Loses" + '\n')
with open(fileNameAll,'w') as fid:
    fid.write("HomeTeam" + ',' + "AwayTeam" + ',' + "HomeTeamGoals" + ',' + "AwayTeamGoals" + '\n')
num = 1
while (int(num)<=85):
    print ("Those are the new games after receiving team " + str(num))
    link = "http://api.football-data.org/v1//teams/" + str(num) + "/fixtures/"
    try:
        f = urllib.urlopen(link)
        json = f.read()
    except:
        num = int(num) + 1
    games = str(json).split("_links")
    i = 0
    for game in games:
        if int(i)>1:
            home = game.split('homeTeamName')[1].split('",')[0].replace('":"',"").replace("1. ","")
            away = game.split('awayTeamName')[1].split('",')[0].replace('":"', "").replace("1. ","")
            homeGoles = game.split('goalsHomeTeam')[1].split(',')[0].replace('":', "")
            awayGoles = game.split('goalsAwayTeam')[1].split(',')[0].replace('":', "").replace('}', "")
            with open(fileNameAll, 'a') as fidAll:
                fidAll.write(home + ',' + away + ',' + homeGoles + ',' + awayGoles + '\n')
            if ((not('null' in homeGoles)) and (not('null' in awayGoles))):
                homeGoles = int(homeGoles)
                awayGoles = int(awayGoles)
                if (homeGoles>awayGoles):
                    temp = home + "_" + away
                    if not(temp in dic):
                        dic.update({temp:1})
                        with open(fileName,'a') as fid:
                            fid.write(home + ',' + away + '\n')
                        print temp
                elif (homeGoles<awayGoles):
                    temp = away + "_" + home
                    if not (temp in dic):
                        dic.update({temp: 1})
                        with open(fileName,'a') as fid:
                            fid.write(away + ',' + home + '\n')
                        print temp
        i = int(i) + 1
    num = int(num) + 1
    print ("Team " + str(num) + " is coming soon")
    time.sleep(20)
print "The Crawling finished"