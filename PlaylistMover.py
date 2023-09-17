import sys
import os
from os import path
from glob import glob

playlistFile = sys.argv[1]

if not path.exists(playlistFile):
    print('Error. {playlistFile} doesn\'t exist.')
    exit()

if not playlistFile.lower().endswith('.m3u'):
    print('Error. {playlistFile} is not a valid playlist file (.m3u).')
    exit()

with open(playlistFile, 'r') as file:
    with open(file.name + '_new', 'w') as newfile:
        for l in file.readlines():
            if l.startswith('#'):
                newfile.write(l)
                continue

            if path.exists(l):
                newfile.write(l)
                continue

            globStr = path.join(path.expanduser('~'), 'Music', '**', path.splitext(path.basename(l.strip()))[0])

            results = glob(globStr + '.mp3', recursive=True) + glob(globStr + '.flac', recursive=True)

            if len(results) < 1:
                newfile.write('#' + l)
                continue

            for r in results:
                if r.endswith('.flac'):
                    newfile.write(r + '\n')
                    break
            else:
                newfile.write(results[0] + '\n')

os.rename(playlistFile, playlistFile + '_old')
os.rename(playlistFile + '_new', playlistFile)