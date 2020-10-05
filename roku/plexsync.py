from roku import Roku
import time

def sleep_check( roku, secs ):
    responded = False
    while not responded :
        try:
            roku.device_info
            responded = True
        except ConnectionError:
            pass
        time.sleep( secs )

def play( video ):

    PLEX_ID = 13535
    PLEXLOAD_SECS = 10
    BUFFER_SECS = 30

    roku_ips = {
        'Lower':'192.168.1.200',
        'Upper':'192.168.1.201',
        'Window':'192.168.1.202',
        'Porch':'192.168.1.203',
    }

    rokus = {}

    print( f'\nDetecting Connected Rokus\n')
    for location, ip in roku_ips.items():
        try:
            print( f'  Searching for {location} Roku at {ip}:')
            roku = Roku(ip)
            info = f'{roku.device_info}'.replace('<DeviceInfo: ','').replace('>','')
            print( f'    {info} found!' )
            rokus[location] = roku
        except:
            print( f'    Not found!' )
            pass

    print( f'\nLaunching Plex\n')
    for location, roku in rokus.items():
        rokus[location].plex = roku[PLEX_ID]
        rokus[location].plex.launch()
        print( f'  Plex launched for {location} Roku')

    print( f'\nWaiting {PLEXLOAD_SECS} seconds for Plex load\n')
    time.sleep( PLEXLOAD_SECS )
    print( f'  Wait complete!')

    print( f'\nPreloading Videos\n')
    for location, roku in rokus.items():
        print( f'  Preloading {location} Roku')
        print( f'    Playing "{video}_{location}"')
        roku.right()
        roku.up()
        roku.select()
        roku.literal(f'{video}_{location}')
        roku.up()
        roku.up()
        roku.right()
        sleep_check( roku, 3 )
        roku.down()
        roku.play()
        sleep_check( roku, 3 )
        roku.down()
        roku.select()
        sleep_check( roku, 3 )
        roku.play()
        print( f'    Video "{video}_{location}" paused')

    print( f'\nWaiting {BUFFER_SECS} seconds for video buffering\n')
    time.sleep( BUFFER_SECS )
    print( f'  Wait complete!')

    print( f'\nStarting Playback\n')
    for location, roku in rokus.items():
        roku.play()
    print( f'  Playback started!')


def play_sequence( sequence ):
    for item in sequence:
        play( item[0] )
        print( f'\nWaiting {item[1]} seconds to start next video\n')
        time.sleep( item[1] )
        print( f'  Wait complete!')
    print( f'\nAll videos complete\n')


if __name__ == "__main__":

    play_sequence([
        ['2020INSP', 3500],
        ['2020INSP', 3500],
        ['2020INSP', 3500],
        ['2020INSP', 3500]
    ])