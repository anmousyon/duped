from qbittorrent import Client


class Bittorrent:
    def __init__(self):
        self.bittorrent = Client('http://localhost:8080/')
        self.bittorrent.login('pavo', 'buffalo12')
    
    def download(self, movie):
        filename = str(movie.metadata.title) + ' (' + str(movie.metadata.year) + ')'
        self.bittorrent.download_from_link(movie.metadata.magnet_link, savepath=filename)
