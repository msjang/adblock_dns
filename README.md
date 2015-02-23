# get_dnsmasq_conf
create dnsmasq.conf from domain list to block advertisement

## how to use
1. Prepare ad_domain_list.txt
```
ad.about.co.kr
ad4980.kr
ad4989.co.kr
ad9.kr
advs.hankyung.com
adcrm.co.kr
adtechus.com
atdmt.com
...
```
2. run the following command
```
usage:   ./get_dnsmasq_conf.py <IP> <ad_domain_list>
example: ./get_dnsmasq_conf 192.168.0.8 ad_domain_list.txt
```
3. then, you will get the content of dnsmasq.conf to block advertisement
```
address=/.ad.about.co.kr/192.168.0.8    #about
address=/.img.ad-indicator.com/192.168.0.8  #ad-indicator
address=/.tag.ad-indicator.com/192.168.0.8  #ad-indicator
address=/.ad134m.com/192.168.0.8    #ad134m
address=/.ad4980.kr/192.168.0.8 #ad4980
address=/.ad4989.co.kr/192.168.0.8  #ad4989
address=/.ad9.kr/192.168.0.8    #ad9
...
```
