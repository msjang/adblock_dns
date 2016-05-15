cat *.txt > tmp.lst
./get_dns_ad_cache.py BIND8 /etc/zone/master/null.zone.file tmp.lst > ad-blocker.db
rm tmp.lst
echo "bind8 configuration file created; ad-blocker.db"
