# usb linux maker aka ulmaker ver. (yes... i won't reconize windows, but exists)

### How to ("comofas") it's a joke... ok
Right... but... how i run this thing? ("comofas... yes again")
```
python ulmaker.py <distro>
```

### If i made a mess...
If no distro or unsupported distro is entered as an argument, a help message will be displayed.

please... python 3, if the script won't run on your terminal, check your python version
```
python --version
```

### Pleaseeeeeee... listen...
If you don't trust on this script (don't run or "X-cute" him), read the code, disconnect all another usb (drives and key)... and run to the hills... no... but keep in mind... human errors occur, put only the drive you are going to use ("there's a selector for drive/key, but human mind sometimes is a S###... taking a breath... it's a fact"), don't blame me if you loss important information, you have been warned.

Remember one more time, make a bootable usb, **will erase** all data on disk.

### No modules installed...
simple... :)
```
pip install -r requirements.txt
```

I hope this help you.

really.


If you like or find any|more bugs/errors/stupid loops/anything, fell free to contact, fork, purge...

Micro$oft... this is not piracy of your software and i don't support this... the script download an official iso from your repositories.


# TODO:
1. remove temp files if manual stop script under download isos. DONE!
1. add more distros support.
1. always get the latest versions of all distros, at moment only ubuntu and archlinux get the latest. (Automatically I mean)
1. add option to keep or not iso file on system.
1. may windows (cof... cof...) support... because i use **dd** system call to record iso on usb device. (but in linux system, this software is copied to device, but maybe won't work as you wish on any motherboard booting)
