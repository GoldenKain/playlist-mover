import sys
from os import path, rename
from glob import glob, escape
from urllib.parse import unquote, urlparse

if len(sys.argv) < 2:
    print('Error. Missing playlist files to process in arguments.')
    exit()

for playlistFile in sys.argv[1:]:
    if not path.exists(playlistFile):
        print('Error. {playlistFile} doesn\'t exist.')
        continue

    if not playlistFile.lower().endswith('.m3u'):
        print('Error. {playlistFile} is not a valid playlist file (.m3u).')
        continue

    with open(playlistFile, 'rt') as file:
        with open(file.name + '_new', 'wt') as newfile:
            for l in file.readlines():
                if l.startswith('#'):
                    newfile.write(l)
                    continue

                # This function call gets rid of trailing whitespaces. I have to manually add a line break from this point on.
                l = unquote(urlparse(l).path, errors='replace')

                if path.exists(l):
                    newfile.write(l + '\n')
                    continue

                globStr = path.join(path.expanduser('~'), 'Music', '**', escape(path.splitext(path.basename(l))[0]))

                results = glob(globStr + '.mp3', recursive=True) + glob(globStr + '.flac', recursive=True)

                if len(results) < 1:
                    newfile.write('#' + l + '\n')
                    continue

                for r in results:
                    if r.endswith('.flac'):
                        newfile.write(r + '\n')
                        break
                else:
                    newfile.write(results[0] + '\n')

    rename(playlistFile, playlistFile + '_old')
    rename(playlistFile + '_new', playlistFile)