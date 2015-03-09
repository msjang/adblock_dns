# ADBlock DNS
create own adblock dns using rasberrypi and dnsmasq

## how to use
1. install dnsmasq
```
~ $ sudo apt-get install dnsmasq
```

2. clone this project on rasberrypi
```
~ $ git clone https://github.com/shuggiejang/get_dnsmasq_conf.git
```

3. get adblock filters and custom custom_ad_domains
```
~ $ cd get_dnsmasq_conf/
~/get_dnsmasq_conf $ ./update_adblock_filter.sh
~/get_dnsmasq_conf $ vi custom_ad_domains.txt
```

4. run the following command
```
~/get_dnsmasq_conf $ ./update_dns.sh
```

5. update DNS on your router
```
~ $ ifconfig eth0
eth0      Link encap:Ethernet  HWaddr b8:27:eb:72:9a:d3
          inet addr:192.168.0.8  Bcast:192.168.0.255  Mask:255.255.255.0
...
```
[DNS configuration on ipTime router](dns_config_on_iptime_router.png)