# ADBlock DNS
* create own adblock dns using rasberrypi and dnsmasq
* create own adblock dns using bind8 based dns cache server

## Basics
Advertisements are usually located on ad.download.cnet.com or similar addresses. This program create DNS that maps these addresses to 127.0.0.1.

## Based on DNSMASQ
### How to use
1. Install dnsmasq on rasberrypi.
```
raspberrypi ~ $ sudo apt-get install dnsmasq
```

2. Clone this project on rasberrypi.
```
raspberrypi ~ $ git clone https://github.com/shuggiejang/adblock_dns.git
```

3. Get adblock filters and custom custom_ad_domains.
```
raspberrypi ~ $ cd adblock_dns/
raspberrypi ~/adblock_dns $ ./update_adblock_filter.sh
raspberrypi ~/adblock_dns $ vi custom_ad_domains.txt
```

4. Run the following command.
```
raspberrypi ~/adblock_dns $ ./update_dns.sh
```

5. Update DNS on your router(once needed).
```
raspberrypi ~ $ ifconfig eth0
eth0      Link encap:Ethernet  HWaddr b8:27:eb:72:9a:d3
          inet addr:192.168.0.8  Bcast:192.168.0.255  Mask:255.255.255.0
...
```
![DNS configuration on ipTime router](dns_config_on_iptime_router.png)

## Based on BIND8
### How to
1. Do the following instructions (on Synology NAS)
https://synologytweaks.wordpress.com/2015/08/23/use-synology-as-an-ad-blocker/

2. Check `ad-blocker.db` is created and ad-block dns is working
After enabling SSH port on Synology WebUI, you can check the followings.
```
$ ssh root@192.168.0.XX

DiskStation> cd /volumeX/@appstore/DNSServer/named/etc/zone/data

DiskStation> ls -1
ad-blocker.db
null.zone.file

DiskStation> cat null.zone.file
zone "null.zone.file" {
    type master;
    file "/etc/zone/master/null.zone.file";
    allow-transfer {61.41.153.2;8.8.8.8;};
    allow-query {any;};
};
include "/etc/zone/data/ad-blocker.db";

DiskStation> tail -n 1 ad-blocker.db
zone "zypenetwork.com" { type master; notify no; file "/etc/zone/master/null.zone.file"; };
```

Check that registered domains are connected to the 127.0.0.1
```
$ ping -c 1 zypenetwork.com
PING zypenetwork.com (127.0.0.1): 56 data bytes
64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.047 ms
```
It is needed to update DNS on your router(once needed).
![DNS configuration on ipTime router](dns_config_on_iptime_router.png)

3. Create and apply ad-blocker.db (bind8 based config). And re-launch DNS server.
```
$ ./update_bind8_conf.sh
bind8 configuration file created; ad-blocker.db

$ scp ad-blocker.db root@192.168.0.XX:/volumeX/@appstore/DNSServer/named/etc/zone/data/ad-blocker.new
```

```
DiskStation> mv ad-blocker.db  ad-blocker.bak
DiskStation> mv ad-blocker.new ad-blocker.db

DiskStation> ls -al
-rw-r--r--    1 nobody   nobody      527217 May 15 12:01 ad-blocker.db
-rw-r--r--    1 root     root        448997 May 15 13:38 ad-blocker.bak
-rw-r--r--    1 nobody   nobody         183 May 15 11:47 null.zone.file
```

## Details
1. Remove duplicates and create DNS configuration.
2. Remove subdomains if a higher domain exists.
```
# ad-domains
raspberrypi ~/adblock_dns $ grep -Hrn realclick ./*.txt
./ad_punisher_abp.txt:382:||realclick.co.kr
./custom_ad_domains.txt:74:realclick.co.kr
./custom_ad_domains.txt:112:click.realclick.co.kr
./custom_ad_domains.txt:113:ads.realclick.co.kr
./custom_ad_domains.txt:114:ptimg.realclick.co.kr
./custom_ad_domains.txt:115:rsense-ad.realclick.co.kr
./custom_ad_domains.txt:116:ade.realclick.co.kr
./custom_ad_domains.txt:117:img.realclick.co.kr
./custom_ad_domains.txt:118:adr.realclick.co.kr
./custom_ad_domains.txt:119:hcimg.realclick.co.kr
./custom_ad_domains.txt:120:image3.realclick.co.kr
./custom_ad_domains.txt:121:image13.realclick.co.kr
./custom_ad_domains.txt:122:mdimg.realclick.co.kr
./custom_ad_domains.txt:123:ptimg.realclick.co.kr
./custom_ad_domains.txt:124:scimg.realclick.co.kr
./easylist.txt:24887:||realclick.co.kr^$third-party

# DNS configuration
raspberrypi ~/adblock_dns $ grep -Hrn realclick ./*.conf
./dnsmasq.adlist.conf:3769:address=/.realclick.co.kr/127.0.0.1 #realclick
```
