# bbb-monitor-zabbix

hosts= ip or hostname of Bigbluebutton server
ZBX_HOSTNAME= ip or hostname of zabbix server

you can get these two bellow parameters with bbb-conf --secret command
BBB_URL= Bigbluebutton url  ## example https://example.com/bigbluebutton/api/
BBB_SECRET= Bigbluebutton secret


- ansible-playbook -ve "hosts=" -e "ZBX_HOSTNAME=" -e "ZBX_SERVER=" -e "BBB_URL=" -e "BBB_SECRET"  pb.yml

- add zbx_export_templates.xml template to zabbix server
 
