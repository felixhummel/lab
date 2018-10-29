# ufw and NAT

Real World (TM):
```
internet --[ ips 1-n on real NICs ]-- host --[ virsh net ]-- vms
                               (ufw / iptables)
```

Playground should be similar, but virtualized, i.e.
```
notebook --[ virsh net ]-- guest --[ docker net ]-- containers
                      (ufw / iptables)
```

## checklist

- [x] notebook
- [ ] virsh net
- [ ] guest (debian from scratch, external kernel)
- [ ] docker
- [ ] containers

## virsh net
- name: lab1
- domain: lab1
- IP range: `10.12.1.0/24`
- static IPs: `10.12.1.1` - `10.12.1.127`
- DHCP range: `10.12.1.128` - `10.12.1.254`


## guest
- name: node1.lab1
- static IP: `10.12.1.1`


# Salt Cloud
https://docs.saltstack.com/en/latest/topics/cloud/libvirt.html

```
sudo vi /etc/salt/cloud.providers
salt-run virt.host_info
```


# Creating a base image
On LVM. the logical volume contents should be the raw FS (no partition tables).

Mounted Kernel. Pro: lvresize for raw FS. Con: cannot update kernel *inside* FS.

- [x] storage pool, volume, FS [scripts/base_image](scripts/base_image)
- [x] install. either:
  - [ ] iso, volume, FS, installer, kernel extract
  - [x] or [debootstrap](https://blag.felixhummel.de/admin/chroot.html)
- [x] kernel extract [scripts/base_image](scripts/base_image)
- [x] run and verify

`--include=less,locales-all,vim,sudo,openssh-server` looks nice http://diogogomes.com/2012/07/13/debootstrap-kvm-image/index.html

# ACPI for `virsh shutdown`
`acpi-support`

# ens3
`/etc/network/interfaces` defines `ens3`, because `files/debian9.xml` sets the network interface on `slot='0x03'`.

This is the PCI slot `3`. If you set it to `0x01`, virsh complains:
```
Attempted double use of PCI slot 0000:00:01.0 (may need "multifunction='on'" for device on function 0)
```

To get `ens1`, `ens2` and `ens3`, use higher slot numbers for different controllers.

# And again
With caching and SSH! \o/

FS fail?
```
e2fsck $dev
```

# Multi-Net and DNS \o/
Given two nets `lab1` (`10.12.1.0/24`) and `lab2` (`10.12.2.0/24`),
can a vm in `lab1` talk to a vm in `lab2`?

https://wiki.libvirt.org/page/VirtualNetworking

https://www.redhat.com/archives/libvir-list/2013-December/msg00063.html

I guess setting `//network/forward/nat/port` explicitly is not needed.
Docs are quiet: https://libvirt.org/formatnetwork.html#elementsConnect

Wrong name in `virsh vol-create`? [./bin/lvm-vol-rename](bin/lvm-vol-rename), `service libvirt-bin restart`

Let's have a look at
[drill](https://imdjh.github.io/toolchain/2015/10/07/drill-if-you-can-dig-if-you-have-to.html)
some time...

# New-Node Script
https://www.ovirt.org/ looks interesting

TL;DR
RTFM!

- hackey hack
- abort script while cloning --> `vol-delete` --> `volume 'node3' is still being allocated.`
- how long does this take? is there a progress bar?
- https://www.google.com/search?q=virsh+vol-clone+"progress"
- https://bugzilla.redhat.com/show_bug.cgi?id=829166
- https://linux.die.net/man/1/virt-clone

```
cat <<EOF > .env
pool=lab
EOF

./bin/new-node debian9 lab1 node2
virsh start node2
ssh root@node2.lab1
```

works for lab1 (because debian9) is defined there. see TODOs in [./bin/new-node](./bin/new-node)

`bin/base2xml.py` and `bin/xmlformat.py` are drafts for xml manipulation

[setting static IP addresses](README.md#setting-static-ip-addresses)

kill everything
```
for node in $(virsh list  --all --name|grep ^node); do
  virsh undefine $node
done
for vol in $(virsh vol-list --pool lab | awk '/\s+node/ {print $1 }'); do
  virsh vol-delete --pool lab --vol $vol
done
virsh net-destroy lab1
virsh net-undefine lab1
```

