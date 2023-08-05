#!/usr/bin/env python3

import sys
import re
import click
import serial
import platform

if re.search(r'Windows', platform.platform()):
    def cprint(msg, *args, **kwargs):
        print(msg, **kwargs)
else:
    from termcolor import cprint


DefaultConfig = {
    'port': '/dev/ttyUSB0',
    'baudrate': 115200,
    'bytesize': 8,
    'parity': 'N',
    'stopbits': 1,
    'localip': '192.168.31.178',
    'serverip': '192.168.31.11',
    'uimage': 'uImage',
    'ruffimage': 'ubi.img'
}


class BaseConnection(object):

    def connect(self):
        pass

    def write(self, data):
        pass

    def read_until(self, match):
        pass


class Connection(BaseConnection):

    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits

    def connect(self):
        self.serial = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=self.bytesize,
            parity=self.parity,
            stopbits=self.stopbits)

    def write(self, data):
        cprint('\n>>> {}'.format(data.strip()), 'magenta')
        self.serial.reset_input_buffer()
        self.serial.write(data.encode())

    def read_until(self, match):
        content = ''

        while True:
            try:
                char = self.serial.read().decode()
            except Exception as e:
                continue
            content += char
            sys.stdout.write(char)
            sys.stdout.flush()
            
            if re.search(match, content):
                self.serial.reset_input_buffer()
                break

        return content


class Flash(object):

    def __init__(self, conn, conf):
        self.conf = conf
        self.conn = conn

    def _wait(self, match):
        return self.conn.read_until(match)

    def _intercept(self):
        self._wait('Hit any key to stop autoboot')
        self._write_wait('')

    def _write(self, cmd):
        self.conn.write(cmd.strip() + '\r\n')

    def _write_wait(self, cmd, match='U-Boot#'):
        self._write(cmd)
        self._wait(cmd)
        self._write('\r\n')
        return self._wait(match)

    def _set_ipaddr(self):
        cmd = 'setenv ipaddr {}'.format(self.conf['localip'])
        self._write_wait(cmd)

    def _set_serveraddr(self):
        cmd = 'setenv serverip {}'.format(self.conf['serverip'])
        self._write_wait(cmd)

    def _update_uimage(self):
        self._write_wait('tftp 0x80200000 {}'.format(self.conf['uimage']))
        self._write_wait('nand erase 0x280000 0x500000', r'Erasing at.*100% complete')
        self._write_wait('nand write 0x80200000 0x280000 0x500000', r'\d+ bytes written: OK')
    
    def _update_ruffimage(self):
        content = self._write_wait('tftp 0x80200000 {}'.format(self.conf['ruffimage']))
        size = re.findall(r'Bytes transferred = (\d+)', content)[0];
        self._write_wait('nand erase 0x780000 0xF880000', r'Erasing at.*100% complete')
        self._write_wait('nand write 0x80200000 0x780000 {}'.format(hex(int(size))), r'\d+ bytes written: OK')

    def _reboot(self):
        self._write('reset')

    def _login(self):
        self._wait('login:')
        self._write('root')
        self._wait('Password:')
        self._write('ruff')
        self._wait(r'root@.*#')

    def get_version(self):
        content = self._write_wait('/ruff/sdk/bin/ruff -v', r'root@.*#')
        ver_str = re.findall(r'\d+\.\d+\.\d+', content)[0]
        return ver_str

    def get_macaddr(self):
        content = self._write_wait('ip link | grep eth0 -A 1 | tail -1', r'root@.*#')
        macaddr = re.findall(r'(?:[\da-f]{2}:){5}[\da-f]{2}', content)
        return macaddr[0]

    def get_serial_number(self):
        addr = self.get_macaddr()
        addr = addr.replace(':', '')
        return '110011FF-0000-0001-00FF-{}'.format(addr)

    def get_wlan_macaddr(self):
        content = self._write_wait('ip link | grep wlan0 -A 1 | tail -1', r'root@.*#')
        macaddr = re.findall(r'(?:[\da-f]{2}:){5}[\da-f]{2}', content)
        return macaddr[0]

    def start(self):
        self.conn.connect()

        # update image
        self._intercept()
        self._set_ipaddr()
        self._set_serveraddr()
        self._update_uimage()
        self._update_ruffimage()

        # reboot
        self._reboot()
        self._login()


def verify(config):
    if (config['localip'] == None):
        error('"localip" is required')
    if (config['serverip'] == None):
        error('"serverip" is required')
    if not is_ip(config['localip']):
        error('invalid localip')
    if not is_ip(config['serverip']):
        error('invalid serverip')

def error(msg):
    cprint('ERR: {}'.format(msg), 'red', file=sys.stderr)
    sys.exit(1)

def is_ip(string):
    return bool(re.match(r'^(\d{1,3}\.){3}\d{1,3}$', string))

@click.command()
@click.option('-p', '--port', default=DefaultConfig['port'], help='serial port name, default is "{}"'.format(DefaultConfig['port']))
@click.option('--baudrate', default=DefaultConfig['baudrate'], help='serial port baudrate, default is "{}"'.format(DefaultConfig['baudrate']))
@click.option('--bytesize', default=DefaultConfig['bytesize'], help='serial port bytesize, default is "{}"'.format(DefaultConfig['bytesize']))
@click.option('--parity', default=DefaultConfig['parity'], type=click.Choice(['N', 'E', 'O', 'M', 'S']), help='serial port parity, default is "{}"'.format(DefaultConfig['parity']))
@click.option('--stopbits', default=DefaultConfig['stopbits'], help='serial port stopbits, default is "{}"'.format(DefaultConfig['stopbits']))
@click.option('-l', '--localip', help='local ip address')
@click.option('-s', '--serverip', help='tftp server ip address')
@click.option('-u', '--uimage', default=DefaultConfig['uimage'], help='uboot image filename, default is "{}"'.format(DefaultConfig['uimage']))
@click.option('-r', '--ruffimage', default=DefaultConfig['ruffimage'], help='ruff image filename, default is "{}"'.format(DefaultConfig['ruffimage']))
def main(**kwargs):
    config = kwargs
    verify(config)

    conn = Connection(
        port=config['port'],
        baudrate=config['baudrate'],
        bytesize=config['bytesize'],
        parity=config['parity'],
        stopbits=config['stopbits'])
    flash = Flash(conn, config)

    flash.start()
    ver_str = flash.get_version()
    sn = flash.get_serial_number()
    wlan_addr = flash.get_wlan_macaddr()
    cprint('\r\nUpdate completed, ruff version is "{}", serial number is "{}"'.format(ver_str, sn), 'green')
    cprint('\r\nwlan0 mac address is "{}"'.format(wlan_addr), 'green')


if __name__ == '__main__':
    main()

