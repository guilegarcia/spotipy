import sys
import spotipy

''' shows the albums and tracks for a given artist.
'''

def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def show_album_tracks(album):
    """
    Show tracks of album
    """
    tracks = []
    results = sp.album_tracks(album['id'])
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    for track in tracks:
        print(track['track_number'], track['name'], milliseconds_to_hms(track['duration_ms']))


def milliseconds_to_hms(milliseconds):
    """
    Takes a number of milliseconds and return it into string of hours, minutes and seconds
    """
    seconds, _ = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    duration = (hours, minutes, seconds)
    duration_str = '{:02d}:{:02d}:{:02d}'.format(*duration)

    return duration_str
    

def show_artist_albums(id):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    print('Total albums:', len(albums))
    unique = set()  # skip duplicate albums
    for album in albums:
        name = album['name']
        if not name in unique:  
            print(name)
            unique.add(name)
            show_album_tracks(album)

def show_artist(artist):
    print('====', artist['name'], '====')
    print('Popularity: ', artist['popularity'])
    if len(artist['genres']) > 0:
        print('Genres: ', ','.join(artist['genres']))

if __name__ == '__main__':
    sp = spotipy.Spotify()
    sp.trace = False

    if len(sys.argv) < 2:
        print(('Usage: {0} artist name'.format(sys.argv[0])))
    else:
        name = ' '.join(sys.argv[1:])
        artist = get_artist(name)
        show_artist(artist)
        show_artist_albums(artist)
