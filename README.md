# Getting Started
Create a network
```
virsh net-define files/networks/lab1.xml
virsh net-autostart lab1
virsh net-start lab1
```

Create a base image as in [scripts/base_image](scripts/base_image).

Create a few nodes, e.g.:
```
base=debian9
net=lab1
for node in node1 node2 node3; do
  ./bin/new-node debian9 $net $node
  virsh start --domain $node.$net
done
```

Set up DNS (see [below](#DNS)).

Wait a few seconds, et voilà:
```
for node in node1 node2 node3; do
  ssh root@$node.$net -c 'echo $HOSTNAME'
done
```


# Directory Structure
```
├── bin
├── docs
├── dumps  # xmls from `virsh dump`
└── files  # manually edited XMLs used for `virsh define`
```


# This is a Toy
Real alternatives:

- https://www.linux-kvm.org/page/Management_Tools
- https://www.proxmox.com/en/proxmox-ve

# Getting Started
Check out [LOG.md](LOG.md)


# "Design" :>
Nodes are friends. They won't imitate each other. If on says it is "node1"
(in `/etc/hostname`) then other nodes won't claim to be "node1" too. See
`./bin/new-node`.


# Setting static IP addresses
```
virsh net-dhcp-leases --network lab1
virsh net-update lab1 add ip-dhcp-host "<host name='node1' ip='10.12.1.55' />" --live --config
virsh reboot --domain node1.lab1
watch -n1 virsh net-dhcp-leases --network lab1

virsh net-update lab1 delete ip-dhcp-host "<host name='node1' />" --live --config
virsh net-update lab1 add ip-dhcp-host "<host name='node1' ip='10.12.1.123' />" --live --config
watch -n1 virsh net-dhcp-leases --network lab1
```


# DNS
Set up local DNS to point to libvirt's DNS.

For NetworkManager with dnsmasq:
```
cat <<'EOF' > /etc/NetworkManager/dnsmasq.d/libvirt-dns.conf
server=/lab1/10.12.1.1
EOF
```

To work around `resolved` on Ubuntu 18.04 see https://github.com/felixhummel/devdns#ubuntu-1804

