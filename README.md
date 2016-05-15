# ADBlock DNS
* 라즈베리파이와 dnsmasq를 이용하여 광고방지 DNS를 만듭니다.
* BIND8 기반의 DNS CACHE 서버를 설정하여 광고방지 DNS를 만듭니다.

## 원리
인터넷 상의 광고들은 주로 ads.realclick.co.kr 또는 이와 유사한 주소에 있습니다.
이 프로그램은 이러한 주소를 127.0.0.1 로 연결하는 DNS를 만듭니다.

## DNSMASQ 기반
### 사용법
1. 라즈베리파이에 dnsmasq 를 설치합니다.
```
raspberrypi ~ $ sudo apt-get install dnsmasq
```

2. 이 프로젝트를 라즈베리파이에 clone 합니다.
```
raspberrypi ~ $ git clone https://github.com/shuggiejang/adblock_dns.git
```

3. adblock 필터를 다운로드합니다. 그리고 사용자가 직접 광고 사이트를 추가합니다.
```
raspberrypi ~ $ cd adblock_dns/
raspberrypi ~/adblock_dns $ ./update_adblock_filter.sh
raspberrypi ~/adblock_dns $ vi custom_ad_domains.txt
```

4. 위의 자료를 바탕으로 DNS를 갱신합니다.
```
raspberrypi ~/adblock_dns $ ./update_dnsmasq_conf.sh
```

5. 공유기의 DNS를 라즈베리파이로 설정합니다(1회만 적용).
```
raspberrypi ~ $ ifconfig eth0
eth0      Link encap:Ethernet  HWaddr b8:27:eb:72:9a:d3
          inet addr:192.168.0.8  Bcast:192.168.0.255  Mask:255.255.255.0
...
```
![ipTime 수동 DNS 설정](dns_config_on_iptime_router.png)

## BIND8 기반
### 사용법
1. Synology NAS를 AD-BLOCK DNS로 만드는 아래 예제를 따라 합니다.
https://synologytweaks.wordpress.com/2015/08/23/use-synology-as-an-ad-blocker/

2. `ad-blocker.db` 파일이 생성되고 동작하는 것을 확인합니다.
Synology NAS의 SSH 포트를 활성화 하고 접속하면, 설정파일이 적용된 것을 확인할 수 있습니다.
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

PC에서 ping을 통해 ad-blocker.db 에 등록된 도메인이 127.0.0.1로 연결된 것을 확인할 수 있습니다.
```
$ ping -c 1 zypenetwork.com
PING zypenetwork.com (127.0.0.1): 56 data bytes
64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.047 ms
```

이 때, 공유기의 DNS를 시놀로지로 설정해야 합니다.(1회만 적용).
![ipTime 수동 DNS 설정](dns_config_on_iptime_router.png)

3. ad-blocker.db (bind8 기반의 DNS 설정파일)을 생성하고 적용합니다. 그리고 DNS 서버를 재시작합니다.
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

## 상세
1. 주소 목록에서 중복된 주소를 제거합니다.
2. 상위도메인이 등록된 경우, 서브 도메인을 제거합니다.
```
# 광고사이트 목록
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

# DNS 설정 파일
raspberrypi ~/adblock_dns $ grep -Hrn realclick ./*.conf
./dnsmasq.adlist.conf:3769:address=/.realclick.co.kr/127.0.0.1 #realclick
```
