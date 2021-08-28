import subprocess
import json

def get_sha256_checksum(filename):
    command = f'sha256sum {filename}'
    s = subprocess.check_output(command, shell=True).decode().strip()
    return s.split(' ')[0]

files = [
    'sdcard.img.zip',
    'rootfs.ext2.xz',
    'boot.tar.xz',
]

sha256_checksums = {
    f: get_sha256_checksum(f'output/images/{f}') for f in files
}

with open('output/images/sha256_checksums.json', 'w') as out:
    json.dump(sha256_checksums, out, indent=2)
