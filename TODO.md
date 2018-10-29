- move DNS to .254 to make room for:
  - node1 --> 10.12.1.1
  - node2 --> 10.12.1.2
- sane MAC addressing scheme for static IPs in networks, because networks are
  harder to change than VMs
- regenerate host SSH keys after clone
  https://blog.digitalocean.com/avoid-duplicate-ssh-host-keys/
- container that operates on LVM devices; `echo foo > $target/etc/hosts` should
  **never** result in `echo foo > /etc/hosts`
- check container on vm1 DNS looup for vm2: correct (internal) IP address?
- reverse DNS
  - working: ip=$(dig felixhummel.de +short); dig -x $ip +short
