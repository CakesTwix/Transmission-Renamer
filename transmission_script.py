from transmission_rpc import Client
from transmission_rpc.utils import format_size
from transmission_rpc.error import TransmissionConnectError
import argparse
from time import sleep 

config = {"username": "CakesTwix",
          "password": "Pass",
          "port": 9091,
          "host": "192.168.1.1",
          "protocol": "http",
          "rpc": "/transmission/rpc"
        }

# Instantiate the parser
parser = argparse.ArgumentParser(description='Massive rename torrent files in torrent, lol')

# Required positional argument
parser.add_argument('-f', '--file', type=str, help='Torrent file')
parser.add_argument('name', type=str, help='Name of torrent')
parser.add_argument('-t','--template', type=str, help='Name template for names in torrent. Default - Episode S01E{}.mkv')

args = parser.parse_args()

# Init
try:
    TransmissionClient = Client(host=config["host"], 
        port=config["port"], 
        username=config["username"], 
        password=config["password"],
        path=config["rpc"],
        protocol=config["protocol"]
    )
except TransmissionConnectError:
    print("No connection")
    exit()

# Code
for torrent in TransmissionClient.get_torrents():
    if args.name in torrent.name:
        if args.file:
            TransmissionClient.remove_torrent(torrent.id)
            with open(args.file, 'rb') as f:
                # Download torrent file
                new_torrent = TransmissionClient.get_torrent(TransmissionClient.add_torrent(f).id)

            sleep(5)
        else:
            new_torrent = torrent
            
        i = 1
        for name_id, name in enumerate(new_torrent.files()):
            if args.template:
                new_name = args.template.format(i)
            else:
                # Default
                new_name = "Episode S01E{}.mkv".format(i)
            TransmissionClient.rename_torrent_path(new_torrent.id, name.name, new_name)
            i += 1
    
        TransmissionClient.rename_torrent_path(new_torrent.id, new_torrent.name, args.name)
        TransmissionClient.verify_torrent(new_torrent.id)
