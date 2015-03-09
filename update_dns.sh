wget -O easylist.txt https://easylist-downloads.adblockplus.org/easylist.txt
cat *.txt > tmp.lst
./get_dnsmasq_conf.py 127.0.0.1 tmp.lst > dnsmasq.adlist.conf