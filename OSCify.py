from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import keyboard
import comtypes
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume



# Get Spotify volume interface
def get_spotify_volume_interface():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name().lower() == "spotify.exe":
            return session._ctl.QueryInterface(ISimpleAudioVolume)
    return None

spotify_volume = get_spotify_volume_interface()


# Parameter Controlled functions
def play_pause():
    print("Play/Pause")
    keyboard.send("play/pause media")

def next_track():
    print("Next Track")
    keyboard.send("next track")

def previous_track():
    print("Previous Track")
    keyboard.send("previous track")

def set_spotify_volume(vol):
    """ vol is 0.0 → 1.0 from radial puppet """
    global spotify_volume

    if spotify_volume is None:
        spotify_volume = get_spotify_volume_interface()
        if spotify_volume is None:
            print("Spotify process not found!")
            return

    spotify_volume.SetMasterVolume(float(vol), None)
    print(f"Volume → {round(vol * 100)}%")


# OSC Handler
def handle_param(address, *args):
    value = args[0]

    if address == "/avatar/parameters/pausePlay" and value == 1:
        play_pause()

    elif address == "/avatar/parameters/skipTrack" and value == 1:
        next_track()

    elif address == "/avatar/parameters/previousTrack" and value == 1:
        previous_track()

    elif address == "/avatar/parameters/spotVolume":
        set_spotify_volume(float(value))

# OSC Server Setup
dispatcher = Dispatcher()
dispatcher.map("/avatar/parameters/*", handle_param)

ip = "127.0.0.1"
port = 9001

print("Listening for VRChat Spotify controls...")
server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()