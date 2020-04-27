**How to run the MVM raspberry pi4 image under qemu-aarch64**

Manual changes that had to be done as of the 'v5' MVM raspberry pi4 image to run it in a virtualised environment:
  * Make sure no direct reference to /dev/mmcblcXX esists (changed /dev/mmcblk0p3 -> /storage mount in /etc/fstab to PARTUUID=738a4d67-03)
  * Change the 'pi' account password in /etc/shadow as it's not the default one.
  * In the 'v5' image the third partition ('/storage') seems not to accessible or is corrupted (used not to be the case) in previous versions. Commented out /storage in /etc/fstab altogether.
kpartx output:
```
    # kpartx -v -a readonly-raspiesp32-v5
    add map loop0p1 (254:0): 0 524288 linear 7:0 8192
    add map loop0p2 (254:1): 0 12294144 linear 7:0 532480
    device-mapper: reload ioctl on loop0p3  failed: Invalid argument
    create/reload failed on loop0p3
```

Notes:
  * The graphical and network devices are virtualised via virtio and a synthetic PCI bus that doesn't exist in the Raspberry PI 4 (Broadcom 2711) hardware. There is currently no 'raspi4' machine type in qemu. The emulated graphical device in the 'raspi3' doesn't get recognised by the 'vc3' video controller driver. This may mature in time - it doesn;t seem feasible for us to contribue to this support in QEMU.

  * vmlinuz is the default kernel that comes from a Vanilla Debian 10 ('buster') installation for ARM64 - the initrd is modified to preload any needed module (list in /initrd-root/conf/mofiles).

The following QEMU configuration is used (vmlinuz-mvm-test and initrd-mvm-test are in this directory):

    qemu-system-aarch64 -M virt -cpu cortex-a72 -m 2048 \
      -kernel vmlinuz-mvm-test -initrd initrd-mvm-test \
      -append "root=PARTUUID=738a4d67-02 rootfstype=ext4 elevator=deadline rootwait noswap ro"
      -drive if=virtio,format=raw,file=/path/to/readonly-raspiesp32-v5 \
      -device virtio-keyboard-pci -device virtio-tablet-pci -device VGA \
      -serial telnet:localhost:18769,server,nowait \
      -serial telnet:localhost:18770,server,nowait \
      -monitor telnet:localhost:18771,server,nowait \
      -net nic,model=virtio -net tap \
      -chardev pipe,path=/tmp/raspusb,id=husbserial \
      -device nec-usb-xhci,id=usb -device usb-serial,chardev=husbserial

Log in and run:
    cd ~/MVMSoftware/gui/gui
    env DISPLAY=:0 ./mvm_gui.py fakeESP32

After starting new 'patient' in the GUI: [resulting screenshot](http://www0.mi.infn.it/~prelz/qemued-mvm.png)

Risky things that may not be needed in the kernel or in the image configuration (not complete - in order of noticing them):

 1. NFS and pipefs
 2. ...
