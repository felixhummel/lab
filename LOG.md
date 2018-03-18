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

- [x] storage pool, volume, FS [scripts/storage_pool](scripts/storage_pool)
- [x] install. either:
  - [ ] iso, volume, FS, installer, kernel extract
  - [x] or [debootstrap](https://blag.felixhummel.de/admin/chroot.html)
- [x] kernel extract [scripts/storage_pool](scripts/storage_pool)
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
