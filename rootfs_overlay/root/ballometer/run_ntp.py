import socket
import struct
import subprocess
import time


def set_system_time(unixtime=1601116701):
    subprocess.run(['date', '-s', '@%i' % int(unixtime)],
                   stdout=subprocess.PIPE).stdout.decode('utf-8')


def get_ntp_time():
    t = 0
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(3)
        client.sendto(('\x1b' + 47 * '\0').encode('utf-8'),
                      ('pool.ntp.org', 123))
        msg, _ = client.recvfrom(1024)
        t = struct.unpack('!12I', msg)[10]
        time_1970 = 2208988800
        t -= time_1970
    except socket.timeout:
        t = 0
    except socket.gaierror:
        t = 0
    except struct.error:
        t = 0
    except IndexError:
        t = 0

    return t


time_was_set = False
while not time_was_set:
    t = get_ntp_time()
    if t > 0:
        set_system_time(t)
        time_was_set = True
    else:
        time.sleep(5)
