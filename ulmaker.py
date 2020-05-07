#!/usr/bin/env python
import re
import signal
import sys
from pathlib import Path
from subprocess import DEVNULL, STDOUT, call, check_output
try:
    import wget
    import requests
    from bs4 import BeautifulSoup
except Exception as err:
    sys.exit(f"[!] {err}, please use 'pip install -r requirements.txt'")


URLS = []
HOME = Path.home()
# when user exits with Ctrl-C, don't show error msg and remove wget's temp files
signal.signal(signal.SIGINT, lambda x, y: clean_temp())


def download(dist):
    regex = re.compile(".*iso$")
    if dist == "ubuntu":
        url = "https://releases.ubuntu.com/20.04/"
        regex = re.compile(".*desktop.*.iso$")
    if dist == "archlinux":
        url = "https://mirror.rackspace.com/archlinux/iso/latest/"
    if dist == "fedora":
        url = "https://download.fedoraproject.org/pub/fedora/linux/releases/32/Workstation/x86_64/iso/"
    if dist == "mint":
        url = "https://mirrors.edge.kernel.org/linuxmint/stable/19.3/"
        regex = re.compile(".*cinnamon-64.*iso$")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    for link in soup.find_all("a", attrs={"href": regex}):
        URLS.append(url+link.get("href"))
    iso_file = Path(f"{HOME}/Downloads/{link.get('href')}")
    if iso_file.exists():
        print("[?] ISO file already downloaded.")
        return
    print(f"Downloading {link.get('href')} and saving on {HOME}/Downloads")
    wget.download(URLS[0], f"{HOME}/Downloads/{link.get('href')}")
    print()
    print("Download complete.")


def create_usb(dist):
    dir = f"{HOME}/Downloads"
    try:
        iso = check_output(f"find {dir} -name {dist}*.iso", shell=True, stderr=STDOUT).decode('utf-8').split('\n')[:-1]
        print(f"ISO file {iso[0]} found!")
    except Exception as err:
        print(f"[!] {err}: {dir} is not a valid directory!")
        exit()

    if not len(iso):
        print("You don't have ISO files in this directory!")
        exit()

    # empty line
    print()

    drive_list = check_output("ls -l /dev/disk/by-id/", shell=True).decode("utf-8")
    if "usb" not in drive_list:
        print("You don't have any USB drive connected!")
        exit()

    usb_list = [d for d in drive_list.split("\n")[:-1]
                if not d[-1].isdigit() and "usb" in d]

    print("List of your USB drives:")

    labels = []
    for i, usb in enumerate(usb_list):
        name = " ".join(usb.split("usb-")[1].split("_")[:-1])
        label = usb.split("/")[-1]
        labels.append(label)
        size = int(check_output(f"cat /sys/class/block/{label}/size", shell=True)) / 2 / 1024 / 1024
        print(f"\n  {i} {name} - {size:.2f} GB")

    # drive selection
    drive = input("\nSelect your USB drive! (default: 0) ")

    if drive.isdigit() and int(drive) < len(labels):
        drive = "/dev/" + labels[int(drive)]
    elif drive == "":
        drive = "/dev/" + labels[0]
    else:
        print("[!] This is not a valid number drive.\n")
        exit()

    confirm = True if input(f"\nThis will erease {drive} Are you sure? (y/n) ") == 'y' else False

    if confirm:
        is_mounted = True if call(f"mount | grep {drive}", shell=True, stdout=DEVNULL, stderr=STDOUT) == 0 else False
        if is_mounted:
            mount_part = check_output(f"mount | grep {drive}", shell=True).decode("utf-8").split(" on")[0]
            call(f"umount {mount_part}", shell=True)
            print("drive unmounted!")

        call(f"sudo dd if={iso[0]} of={drive} status=progress bs=4M", shell=True)
        call(f"sync && sudo eject {drive}", shell=True)
        print("\nDone! Now you can remove your USB drive!")
    else:
        exit()


def info():
    print("""
            All systems and software are downloaded in x64 only... sorry.
            Supported distros and software at moment:
            ubuntu    = Ubuntu 20.04 (LTS Always)
            fedora    = Fedora 32
            archlinux = Archlinux (latest)
            mint      = Mint Linux (19.3)
            """)


def clean_temp():
    try:
        temp_files = check_output(
                    f"find {HOME}/Downloads -name *.tmp", shell=True, stderr=STDOUT
                ).decode('utf-8').split('\n')[:-1]
        if temp_files:
            call(f"rm {HOME}/Downloads/*.tmp", shell=True)
        exit()
    except Exception as err:
        print(f"[!] {err}: {dir} is not a valid directory!")
        exit()


def main(argv):
    try:
        if argv:
            download(argv)
            create_usb(argv)
    except Exception:
        info()


if __name__ == "__main__":
    try:
        dist = sys.argv[1].lower()
        main(dist)
    except Exception:
        info()
