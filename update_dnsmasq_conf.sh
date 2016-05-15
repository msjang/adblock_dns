cat *.txt > tmp.lst
./get_dnsmasq_conf.py 127.0.0.1 tmp.lst > dnsmasq.adlist.conf
rm tmp.lst
echo "dnsmasq configuration file created"

sudo mv /etc/dnsmasq.d/dnsmasq.adlist.conf /etc/dnsmasq.d/dnsmasq.adlist.conf.bak
sudo mv dnsmasq.adlist.conf /etc/dnsmasq.d/dnsmasq.adlist.conf
echo "dnsmasq configuration file updated"

sudo service dnsmasq restart
echo "dns service restarted"