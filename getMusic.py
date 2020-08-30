#Class with functionality to generate a random month and year and extract a random song from that
#https://developer.spotify.com/dashboard/
#Imports
import random
import requests
from bs4 import BeautifulSoup


#Code
class Music(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}


    def randDate(self):
        randomMonth = random.randint(1,12)
        randomYear = random.randint(1960,2020)
        if randomMonth == 1:
            randomMonth = "january-01"
        if randomMonth == 2:
            randomMonth = "february-02"
        if randomMonth == 3:
            randomMonth = "march-03"
        if randomMonth == 4:
            randomMonth = "april-04"
        if randomMonth == 5:
            randomMonth = "may-05"
        if randomMonth == 6:
            randomMonth = "june-06"
        if randomMonth == 7:
            randomMonth = "july-07"
        if randomMonth == 8:
            randomMonth = "august-08"
        if randomMonth == 9:
            randomMonth = "september-09"
        if randomMonth == 10:
            randomMonth = "october-10"
        if randomMonth == 11:
            randomMonth = "november-11"
        if randomMonth == 12:
            randomMonth = "december-12"
        return str(randomMonth), str(randomYear)


    def getRandomAlbum(self):
        #Generates the date that the songs will be from
        randomMonth, randomYear = self.randDate()
        #print(randomMonth, randomYear)
        #Extracts the page as html soup
        self.albumLinks = "https://www.albumoftheyear.org/" + randomYear + "/releases/" + randomMonth + ".php"
        self.albumPage = requests.get(self.albumLinks, headers=self.headers)
        self.albumPageSoup = BeautifulSoup(self.albumPage.content, "lxml")

        #Sorts through the soup to find all the albums
        self.albumList = self.albumPageSoup.find_all("div", attrs={"class":"albumBlock five"})

        #Randomly chooses an album
        self.randomAlbumNum = random.randint(0,len(self.albumList))
        self.selectedAlbum = self.albumList[self.randomAlbumNum]
        #print(self.albumList[self.randomAlbumNum])
        #Gets the spotify link of the chosen album
        self.randAlbumLink = self.getAlbumLink(self.selectedAlbum)
        #self.randSongName, self.randSongArtist = self.getRandSong(self.randAlbumLink)
        self.randSongName, self.randArtistName, self.randSongID = self.getRandSong(self.randAlbumLink)
        """
        print("Song:", self.randSongName, "by", self.randArtistName)
        print("ID:", self.randSongID)"""
        return self.randSongName, self.randArtistName, self.randSongID


    def getAlbumLink(self, album):
        #Finds all the links in this part of the soup to find the one which links to the album page
        for item in album.find_all("a"):
            if item.get("href")[1:6] == "album":
                self.albumLink = item.get("href")

        self.albumInfoPage = requests.get("https://www.albumoftheyear.org" + self.albumLink, headers=self.headers)
        #self.albumInfoPage = requests.get("https://www.albumoftheyear.org/album/21182-fischerspooner-odyssey.php", headers=self.headers)
        self.albumInfoPageSoup = BeautifulSoup(self.albumInfoPage.content, "lxml")

        #Gets the spotify link of the randomly selected album
        self.buttons = self.albumInfoPageSoup.find("div", attrs={"class":"thirdPartyLinks"})
        self.buttonsLinks = self.buttons.find_all("a")
        for item in self.buttonsLinks:
            if item.get("href")[7:23] == "open.spotify.com":
                return item.get("href")


    def getRandSong(self, albumLink):
        #This gets the randomly generated spotify album link and passes it to beatifulSoup
        self.spotifyAlbumPage = requests.get(albumLink, headers=self.headers)
        self.spotifyAlbumPageSoup = BeautifulSoup(self.spotifyAlbumPage.content, "lxml")

        #Finds a list of all songs in the album
        self.songList = self.spotifyAlbumPageSoup.find("ol", attrs={"class":"tracklist"})

        #Randomly Chooses a song
        self.randNum = random.randint(0,len(self.songList))

        #self.chosenSong = list(self.songList)[0]
        self.chosenSong = list(self.songList)[self.randNum]


        #Finds all the links in the page and extracts the text of the artist
        self.songArtistData = self.spotifyAlbumPageSoup.find_all("a")
        self.songArtistName = list(self.songArtistData)[5].string

        #Finds the song id where its located in the meta tags
        self.songIDList = self.spotifyAlbumPageSoup.find_all("meta", attrs={"property":"music:song"})
        self.songID = list(self.songIDList)[self.randNum]
        #self.songID = list(self.songIDList)[0]

        #Returns the song name, song artist and song track id
        return list(self.chosenSong.children)[1].string, self.songArtistName, self.songID["content"]



"""
#Using the class
try:
    randSong = Music()
    data = randSong.getRandomAlbum()
except:
    randSong = Music()
    data = randSong.getRandomAlbum()

print(data)
"""
