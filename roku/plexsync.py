from roku import Roku
import time


def sleep(roku, secs):
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
        except Exception:
            print( '    Exception' )
        time.sleep(0.5)


def play(video):

    PLEX_ID = 13535
    PLEXLOAD_SECS = 10
    BUFFER_SECS = 15

    roku_ips = {
        'Window': '192.168.1.202',
        'Lower': '192.168.1.200',
        'Upper': '192.168.1.201',
        'Porch': '192.168.1.203',
    }

    rokus = {}

    print(f'\nDetecting Connected Rokus\n')
    for location, ip in roku_ips.items():
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

    print(f'\nPausing if Plex Open\n')
    for location, roku in rokus.items():
        print(f'  Checking if plex running on {location} Roku')
        if roku.active_app.id != 'None':
            active = int(roku.active_app.id)
            if active == PLEX_ID:
                rokus[location].plex = roku[PLEX_ID]
                retry(roku.back)
                retry(roku.back)
                retry(roku.back)
                print(f'   Plex running, returning to main.')
            else:
                rokus[location].plex = roku[PLEX_ID]
                rokus[location].plex.launch()
                print(f'  Plex launched for {location} Roku')
        else:
            rokus[location].plex = roku[PLEX_ID]
            rokus[location].plex.launch()
            print(f'  Plex launched for {location} Roku')

    # print(f'\nLaunching Plex\n')
    # for location, roku in rokus.items():
    #     rokus[location].plex = roku[PLEX_ID]
    #     rokus[location].plex.launch()
    #     print(f'  Plex launched for {location} Roku')

    print(f'\nWaiting {PLEXLOAD_SECS} seconds for Plex load\n')
    time.sleep(PLEXLOAD_SECS)
    print(f'  Wait complete!')

    print(f'\nPreloading Videos\n')
    for location, roku in rokus.items():
        print(f'  Preloading {location} Roku')
        print(f'    Playing "{video}_{location}"')
        retry(roku.right)
        retry(roku.up)
        retry(roku.select)
        roku.literal(f'{video}_{location}')
        retry(roku.up)
        retry(roku.up)
        retry(roku.right)
        sleep(roku, 2)
        retry(roku.down)
        retry(roku.play)
        sleep(roku, 2)
        retry(roku.down)
        retry(roku.select)
        # Roku is playing video from beginning or paused near beginning at this point.
        # Fast forward and play to cause buffering.
        retry(roku.forward)
        sleep(roku, 1)
        retry(roku.play)
        # Reverse then play and pause to ensure paused at start.
        retry(roku.reverse)
        sleep(roku, 4)
        retry(roku.play)
        sleep(roku, 0.01)
        retry(roku.play)
        # roku.reverse()
        # sleep(roku, 3)
        # roku.play()
        # sleep(roku, 0.01)
        # roku.play()
        print(f'    Video "{video}_{location}" paused')
        print(f'    Waiting {BUFFER_SECS} seconds for video buffering')
        time.sleep(BUFFER_SECS)
        print(f'    Wait complete!')

    print(f'\nStarting Playback\n')
    for location, roku in rokus.items():
        roku.play()
    print(f'  Playback started!')


def play_sequence(sequence):
    for item in sequence:
        play(item[0])
        print(f'\nWaiting {item[1]} seconds to start next video\n')
        time.sleep(item[1])
        print(f'  Wait complete!')
    print(f'\nAll videos complete\n')


if __name__ == "__main__":

    # play_sequence([
    #     ['2020INSP', 3480],
    #     ['2020INSP', 3480],
    #     ['2020INSP', 3480],
    #     ['2020INSP', 3480]
    # ])

    # play_sequence([
    #     ['2020HAUNT', 125],
    #     ['2020BONE', 125],
    #     ['2020HAUNT', 125],
    #     ['2020BONE', 125],
    #     ['2020HAUNT', 125],
    #     ['2020BONE', 125]
    # ])

    play_sequence([
        ['2020HALLOWEEN', 4385],
        ['2020HALLOWEEN', 4385],
        ['2020HALLOWEEN', 4385],
        ['2020HALLOWEEN', 4385],
    ])
