from roku import Roku
import time
from plexapi.myplex import MyPlexAccount

import secrets


PLEX_ID = 13535
PLEXLOAD_SECS = 12
BUFFER_SECS = 10

ROKU_IPS = {
    # 'Window': '192.168.1.202',
    'Lower': '192.168.1.200',
    'Upper': '192.168.1.201',
    'Porch': '192.168.1.203',
}

def roku_sleep(roku, secs):
    responded = False
    while not responded:
        try:
            roku.device_info
            responded = True
        except ConnectionError:
            pass
        time.sleep(secs)


def retry(command):
    responded = False
    while not responded:
        try:
            command()
            responded = True
        except Exception as e:
            print( '    Exception: ' + str( e ) )
        time.sleep(0.5)

def play_sequence(sequence):
    for item in sequence:
        play(item[0])
        print(f'\nWaiting {item[1]} seconds to start next video\n')
        time.sleep(item[1])
        print(f'  Wait complete!')
    print(f'\nAll videos complete\n')


def play(video):

    rokus = {}

    print(f'\nDetecting Connected Rokus\n')
    for location, ip in ROKU_IPS.items():
        try:
            print(f'  Searching for {location} Roku at {ip}:')
            roku = Roku(ip)
            info = f'{roku.device_info}'.replace(
                '<DeviceInfo: ', '').replace('>', '')
            print(f'    {info} found!')
            rokus[location] = roku
        except:
            print(f'    Not found!')
            pass

    plex_loading = False

    print(f'\nLaunching Plex\n')
    for location, roku in rokus.items():
        rokus[location].plex = roku[PLEX_ID]
        rokus[location].plex.launch()
        plex_loading = True
        print(f'  Plex launched for {location} Roku')

    print(f'\nConnecting to Plex Server\n')
    account = MyPlexAccount(secrets.PLEX_USERNAME, secrets.PLEX_PASSWORD)
    plex = account.resource(secrets.PLEX_SERVER).connect()
    print(f'  Connected to server {secrets.PLEX_SERVER}')

    print(f'\nWaiting {PLEXLOAD_SECS} seconds for Plex load\n')
    if plex_loading:
        time.sleep(PLEXLOAD_SECS)
    print(f'  Wait complete!')

    print(f'\nConnecting to Plex Clients\n')
    for location, roku in rokus.items():
        print(f'  Connecting to Plex on {location} Roku at {ROKU_IPS[location]}:')
        for client in plex.clients():
            if ROKU_IPS[location] in client._baseurl:
                rokus[location].client = client
                #rokus[location].client.connect()
                print(f'    Connected to {rokus[location].client}')

    print(f'\nPreloading Videos\n')
    for location, roku in rokus.items():
        print(f'  Preloading {location}')
        video_name = f'{video}_{location}'
        movies = plex.library.section('Videos').search(video_name)
        if len( movies ) > 0:
            movie = movies[0]
            movie.markUnwatched()
            rokus[location].client.playMedia(movie)
            while not rokus[location].client.isPlayingMedia():
                time.sleep(0.001)
            retry(roku.play)
            print(f'    Buffering "{video_name}" for {BUFFER_SECS} secs')
            time.sleep(BUFFER_SECS)

    print(f'\nStarting Playback\n')
    for location, roku in rokus.items():
        rokus[location].client.play()
        print(f'    Playing "{video}_{location}"')


if __name__ == "__main__":

    play_sequence([
        ['2021XMAS', 5220],
        ['2021XMAS', 5220],
        ['2021XMAS', 5220],
        ['2021XMAS', 5220],
    ])

    # play_sequence([
    #     ['2021TEST', 600],
    #     ['2021TEST', 600],
    #     ['2021TEST', 600],
    #     ['2021TEST', 600],
    # ])


    # Test
    # roku = Roku('192.168.1.201')
    # roku_plex = roku[13535].launch()
    # account = MyPlexAccount(secrets.PLEX_USERNAME, secrets.PLEX_PASSWORD)
    # plex = account.resource(secrets.PLEX_SERVER).connect()
    # time.sleep(10)
    # for client in plex.clients():
    #     if '192.168.1.201' in client._baseurl:
    #         client.connect()
    #         movies = plex.library.section('Videos').search("2020HALLOWEEN_Upper")
    #         client.playMedia( movies[0])
    #         client.seekTo(0)
    #         client.pause()
    #         print( 'PAUSE')
    #         time.sleep(4)
    #         client.play()
    #         print( 'PLAY')