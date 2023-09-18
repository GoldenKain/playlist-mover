import sys
from os import path, rename
from glob import glob, escape
from urllib.parse import unquote, urlparse

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

            l = unquote(urlparse(l).path, errors='replace')

            if path.exists(l):
                newfile.write(l)
                continue

            globStr = path.join(path.expanduser('~'), 'Music', '**', escape(path.splitext(path.basename(l.strip()))[0]))

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

rename(playlistFile, playlistFile + '_old')
rename(playlistFile + '_new', playlistFile)