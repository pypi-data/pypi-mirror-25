# auto_flash

自动化升级网关image，基于python3

## Example

```shell
ruff_auto_flash.py -p /dev/ttyUSB0 -l 192.168.31.254 -s 192.168.31.11
```

## Installation

1. 安装python3

   **OSX** : `brew install python3`

   **Linux** : 具体请参照各发行版的包管理器

   **Windows** : 至https://www.python.org/下载安装python3，安装过程中注意勾选`Add Python 3.x to PATH`

2. 安装ruff_auto_flash，代码已打包上传至pypi，可直接在线安装：

   ```shell
   pip install ruff_auto_flash
   ```


## Usage

```shell
Usage: ruff_auto_flash.py [OPTIONS]

Options:
  -p, --port TEXT       serial port name, default is "/dev/ttyUSB0"
  --baudrate INTEGER    serial port baudrate, default is "115200"
  --bytesize INTEGER    serial port bytesize, default is "8"
  --parity [N|E|O|M|S]  serial port parity, default is "N"
  --stopbits INTEGER    serial port stopbits, default is "1"
  -l, --localip TEXT    local ip address
  -s, --serverip TEXT   tftp server ip address
  -u, --uimage TEXT     uboot image filename, default is "uImage"
  -r, --ruffimage TEXT  ruff image filename, default is "ubi.img"
  --help                Show this message and exit.
```

