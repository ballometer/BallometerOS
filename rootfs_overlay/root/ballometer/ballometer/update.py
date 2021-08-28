import requests
import json
import subprocess
import time


request_timeout = 30
github_user_repo = 'ballometer/BallometerOS'


class UpdateError(Exception):
    pass


def get_installed_release():
    '''
    Reads the version from ```/root/release.json``` and returns it as a string.

    Result example: ```'v1.1.21'```
    '''

    try:
        with open('/root/release.json') as f:
            return json.load(f)
    except FileNotFoundError:
        raise UpdateError('FileNotFoundError')
    except json.JSONDecodeError:
        raise UpdateError('JSONDecodeError')


def get_available_releases():
    '''
    Connects to GitHub and searches for all available releases. 
    The result is a list of releases ordered such that the newest release comes first.

    Example result: ```['v1.1.21', 'v1.1.19', 'v1.1.18-rc.1']```
    '''

    result = []

    url = f'https://api.github.com/repos/{github_user_repo}/releases'
    try:
        r = requests.get(url, timeout=request_timeout)
    except requests.exceptions.Timeout:
        raise UpdateError('Timout')
    except requests.exceptions.ConnectionError:
        raise UpdateError('ConnectionError')
    if r.status_code != 200:
        raise UpdateError('Non 200 status code')

    try:
        releases = json.loads(r.text)
    except json.JSONDecodeError:
        raise UpdateError('JSONDecodeError')

    for release in releases:
        if 'tag_name' not in release:
            raise UpdateError('tag_name not in releases')
        result.append(release['tag_name'])

    return result


def install(release='v1.0.0', update_callback=lambda text: ()):
    '''
    Downloads ```boot.tar.xz``` and ```rootfs.ext2.xz``` from the assets of the GitHub release, extracts the contents and flashes it to the SD card, and makes sha256 checksums of the compressed files and compare them against the values specified in sha256_checksums.json that is also a release asset.
    If no errors occure and the checksums match, the flag in ```/boot/select.txt``` gets updated to the passive partition which now contains the new files. 
    '''
    passive_partition = _get_passive_partition()
    total_size = _get_total_size(release)

    def progress_callback(percentage):
        text = 'ROOTFS ' + str(percentage) + ' %'
        update_callback(text)

    checksums = {}

    checksums['rootfs.ext2.xz'] = _download_rootfs(
        release=release,
        passive_partition=passive_partition,
        progress_callback=progress_callback,
        total_size=total_size,
    )

    update_callback('DOWNLOAD BOOT')

    checksums['boot.tar.xz'] = _download_boot(
        release=release, 
        passive_partition=passive_partition,
    )

    checksums_github = _download_checksums(release=release)

    if 'rootfs.ext2.xz' not in checksums_github:
        raise UpdateError('GitHub checksum file misses rootfs.ext2.xz')

    if 'boot.tar.xz' not in checksums_github:
        raise UpdateError('GitHub checksum file misses boot.tar.xz')

    if checksums['rootfs.ext2.xz'] != checksums_github['rootfs.ext2.xz']:
        raise UpdateError('Checksum rootfs.ext2.xz is wrong')

    if checksums['boot.tar.xz'] != checksums_github['boot.tar.xz']:
        raise UpdateError('Checksum boot.tar.xz is wrong')

    update_callback('CHECKSUMS OK')

    time.sleep(1)

    _flash_boot_select(passive_partition=passive_partition)


def _run(command='ls -lah'):
    try:
        return subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT).decode().strip()
    except subprocess.CalledProcessError:
        raise UpdateError('CalledProcessError')


def _get_passive_partition():
    cmdline = _run('cat /proc/cmdline')
    p2 = '/dev/mmcblk0p2'
    p3 = '/dev/mmcblk0p3'

    if p2 in cmdline:
        return p3
    elif p3 in cmdline:
        return p2
    else:
        raise UpdateError('Passive partition not found')


def _get_total_size(release='v1.0.0'):
    url = f'https://github.com/{github_user_repo}/releases/download/{release}/rootfs.ext2.xz'
    try:
        r = requests.get(url, stream=True, timeout=request_timeout)
    except requests.exceptions.Timeout:
        raise UpdateError('Timout')
    except requests.exceptions.ConnectionError:
        raise UpdateError('ConnectionError')

    try:
        return float(r.headers['Content-Length'])
    except KeyError:
        raise UpdateError('Content-Length not in headers')


def _download_checksums(release='v1.0.0'):
    url = f'https://github.com/{github_user_repo}/releases/download/{release}/sha256_checksums.json'
    try:
        r = requests.get(url, timeout=request_timeout)
    except requests.exceptions.Timeout:
        raise UpdateError('Timout')
    except requests.exceptions.ConnectionError:
        raise UpdateError('ConnectionError')
    if r.status_code != 200:
        raise UpdateError('Non 200 status code')

    try:
        return json.loads(r.text)
    except json.JSONDecodeError:
        raise UpdateError('JSONDecodeError')


def _download_rootfs(
        release='v1.0.0',
        passive_partition='/dev/mmcblk0p3',
        progress_callback=lambda percentage: (),
        total_size=1.0):
    '''
    Downloads the compressed ```rootfs.ext2.xz``` from GitHub and flashes the content to the passive partition.
    At the same time the sha256 sum of ```rootfs.ext2.xz``` is computed and returned at the end.

    Return example: ```'b2561992faf0f4540b5bf761a7d147bbd8b344cb9f3040b5266842dfccb77de1'```
    '''

    sha_value = None
    try:
        url = f'https://github.com/{github_user_repo}/releases/download/{release}/rootfs.ext2.xz'
        r = requests.get(url, stream=True, timeout=request_timeout)

        r.raise_for_status()
        chunk_i = 0
        last_percentage = 0
        progress_callback(last_percentage)

        sha_command = ['sha256sum']
        sha_pipe = subprocess.Popen(
            sha_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        xz_command = ['xz', '-d']
        xz_pipe = subprocess.Popen(
            xz_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        dd_command = ['dd', f'of={passive_partition}', 'bs=1M']
        dd_pipe = subprocess.Popen(dd_command, stdin=xz_pipe.stdout)

        chunk_size = 8192
        for chunk in r.iter_content(chunk_size):
            xz_pipe.stdin.write(chunk)
            sha_pipe.stdin.write(chunk)
            chunk_i += 1
            percentage = min(int(100 * chunk_i * chunk_size / total_size), 100)
            if percentage > last_percentage:
                last_percentage = percentage
                progress_callback(percentage)

        xz_pipe.stdin.close()
        xz_pipe.wait()
        dd_pipe.wait()

        sha_pipe.stdin.close()
        sha_value = sha_pipe.stdout.readline().decode().strip().split(' ')[0]
        sha_pipe.wait()

    except requests.exceptions.Timeout:
        raise UpdateError('Timout')
    except requests.exceptions.ConnectionError:
        raise UpdateError('ConnectionError')

    return sha_value

def _download_boot(release='v1.0.0', passive_partition='/dev/mmcblk0p3'):
    '''
    Downloads the compressed ```boot.tar.xz``` from GitHub and extracts the files to parts of the boot partition.
    At the same time the sha256 sum of ```boot.tar.xz``` is computed and returned at the end.

    Return example: ```'79dbca32e4f743a63b984e6b2b94495f1622343d1a3a6580733e5485b63fe706'```
    '''

    sha_value = None

    _run('mount -t vfat /dev/mmcblk0p1 /boot')
    folder = '/boot/os-p2'
    if passive_partition == '/dev/mmcblk0p3':
        folder = '/boot/os-p3'

    _run('rm -rf ' + folder)
    _run('mkdir ' + folder)

    try:
        url = f'https://github.com/{github_user_repo}/releases/download/{release}/boot.tar.xz'
        r = requests.get(url, stream=True, timeout=request_timeout)

        r.raise_for_status()

        sha_command = ['sha256sum']
        sha_pipe = subprocess.Popen(
            sha_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        xz_command = ['xz', '-d']
        xz_pipe = subprocess.Popen(
            xz_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        tar_command = ['tar', 'x', '-C', folder]
        tar_pipe = subprocess.Popen(tar_command, stdin=xz_pipe.stdout)

        chunk_size = 8192
        for chunk in r.iter_content(chunk_size):
            xz_pipe.stdin.write(chunk)
            sha_pipe.stdin.write(chunk)

        xz_pipe.stdin.close()
        xz_pipe.wait()
        tar_pipe.wait()

        sha_pipe.stdin.close()
        sha_value = sha_pipe.stdout.readline().decode().strip().split(' ')[0]
        sha_pipe.wait()

    except requests.exceptions.Timeout:
        raise UpdateError('Timout')
    except requests.exceptions.ConnectionError:
        raise UpdateError('ConnectionError')

    _run('umount /boot')

    return sha_value


def _flash_boot_select(passive_partition='/dev/mmcblk0p3'):
    _run('mount -t vfat /dev/mmcblk0p1 /boot')

    if passive_partition == '/dev/mmcblk0p2':
        _run('echo "cmdline=cmdline-p2.txt\r\n' +
             'os_prefix=os-p2/" > /boot/select.txt')
    elif passive_partition == '/dev/mmcblk0p3':
        _run('echo "cmdline=cmdline-p3.txt\r\n' +
             'os_prefix=os-p3/" > /boot/select.txt')
    else:
        _run('umount /boot')
        raise UpdateError('Passive partition not matched')

    _run('umount /boot')
