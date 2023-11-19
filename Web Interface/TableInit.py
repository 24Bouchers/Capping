# python -m pip install flask
# pip3 install pymysql
# pip install mysql-connector-python
# mysql -u root -p 

#: Login for consol
from flask import Flask
import pymysql

app = Flask(__name__)

#####################
# CONNECTION TOGGLE #
#####################
# Maybe for website purposes have username and password be the same as website login
# This could be easy access for credentials of who can manipulate the DB

#Toggle to run locally or on the vm
LOCAL = True

if(LOCAL):
	conn = pymysql.connect(host='localhost', user='root', password='ArchFiber23', db='radius_netelastic')
else: 
    conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='radius_netelastic')
    
cur = conn.cursor()

#########################
# CREATE/SETUP DATABASE #
#########################

#Drop Database for testing purposes 
cur.execute("DROP DATABASE IF EXISTS radius_netelastic")
cur.execute("CREATE DATABASE radius_netelastic; ")
cur.execute("USE radius_netelastic;")

#Declaratives

# This statement saves the current value of the CHARACTER_SET_CLIENT session variable into a user-defined variable for later restoration.
cur.execute("/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;")
# Similar to the previous statement, this one saves the value of the CHARACTER_SET_RESULTS session variable.
cur.execute("/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;")
# This statement saves the value of the COLLATION_CONNECTION session variable.
cur.execute("/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;")
#This sets the character set and collation for the current connection to use UTF-8 (specifically, utf8mb4),
# which is often used to support a wide range of characters, including emoji.
cur.execute("/*!40101 SET NAMES utf8mb4 */;")
# This saves the current time zone setting into a user-defined variable.
cur.execute("/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;")
# This sets the time zone for the current connection to UTC (Universal Time) by setting the TIME_ZONE session variable to +00:00.
cur.execute("/*!40103 SET TIME_ZONE='+00:00' */;")
#This statement saves the current value of the UNIQUE_CHECKS system variable into a user-defined variable,
# then sets UNIQUE_CHECKS to 0, effectively disabling unique constraint checks temporarily.
cur.execute("/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;")
# Similar to the previous statement, it saves the current value of the FOREIGN_KEY_CHECKS system variable ,
# disables foreign key constraint checks temporarily by setting FOREIGN_KEY_CHECKS to 0.
cur.execute("/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;")
# This statement saves the current value of the SQL_MODE system variable into a user-defined variable,
# sets the SQL_MODE to 'NO_AUTO_VALUE_ON_ZERO',
# which disables automatic generation of values for columns with the AUTO_INCREMENT attribute.
cur.execute("/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;")
# This statement saves the current value of the SQL_NOTES system variable and sets it to 0, which suppresses generation of information notes from the server.
cur.execute("/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;")

# Preserving the value of character_set_client in the variable @saved_cs_client
# in a way that is compatible with MySQL 4.01.01 and later.
cur.execute("/*!40101 SET @saved_cs_client     = @@character_set_client */;")

# Sets the MySQL session variable character_set_client to use the UTF-8 character set.
cur.execute("/*!40101 SET character_set_client = utf8 */;")

#################
# CREATE TABLES #
#################

#Check Radact.png for an easy display of information
# nasportid (Port ID),
# acctstarttime (for uptime calculation)
# acctupdatetime (Date/Time in device table)
# acctstoptime (Time for stop entry)
# callingstationid (MAC Address)
# acctterminatecause (Termination Reason)
# framedipaddress (IPv4 Address)
# framedipv6address (IPv6 Address)

#Create Gtel Table radacct. 

cur.execute('''CREATE TABLE radacct (
  `radacctid` bigint(21) NOT NULL AUTO_INCREMENT,
  `acctsessionid` varchar(64) NOT NULL DEFAULT '',
  `acctuniqueid` varchar(32) NOT NULL DEFAULT '',
  `username` varchar(64) NOT NULL DEFAULT '',
  `realm` varchar(64) DEFAULT '',
  `nasipaddress` varchar(15) NOT NULL DEFAULT '',
  `nasportid` varchar(128) DEFAULT NULL,
  `nasporttype` varchar(32) DEFAULT NULL,
  `acctstarttime` datetime DEFAULT NULL,
  `acctupdatetime` datetime DEFAULT NULL,
  `acctstoptime` datetime DEFAULT NULL,
  `acctinterval` int(12) DEFAULT NULL,
  `acctsessiontime` int(12) unsigned DEFAULT NULL,
  `acctauthentic` varchar(32) DEFAULT NULL,
  `connectinfo_start` varchar(128) DEFAULT NULL,
  `connectinfo_stop` varchar(128) DEFAULT NULL,
  `acctinputoctets` bigint(20) DEFAULT NULL,
  `acctoutputoctets` bigint(20) DEFAULT NULL,
  `calledstationid` varchar(50) NOT NULL DEFAULT '',
  `callingstationid` varchar(50) NOT NULL DEFAULT '',
  `acctterminatecause` varchar(32) NOT NULL DEFAULT '',
  `servicetype` varchar(32) DEFAULT NULL,
  `framedprotocol` varchar(32) DEFAULT NULL,
  `framedipaddress` varchar(15) NOT NULL DEFAULT '',
  `framedipv6address` varchar(45) NOT NULL DEFAULT '',
  `framedipv6prefix` varchar(45) NOT NULL DEFAULT '',
  `framedinterfaceid` varchar(44) NOT NULL DEFAULT '',
  `delegatedipv6prefix` varchar(45) NOT NULL DEFAULT '',
  `class` varchar(64) DEFAULT NULL,
  `netelasticacctipv6inputoctets` bigint(20) unsigned DEFAULT 0,
  `netelasticacctipv6outputoctets` bigint(20) unsigned DEFAULT 0,
  `netelasticacctipv6outputpackets` bigint(20) unsigned DEFAULT 0,
  `netelasticdomainname` varchar(64) DEFAULT '',
  `netelasticnatstartport` int(11) DEFAULT NULL,
  `netelasticnatendport` int(11) DEFAULT NULL,
  `netelasticusermac` varchar(17) DEFAULT '',
  `netelasticacctipv6inputpackets` bigint(20) unsigned DEFAULT 0,
  `netelasticnatpublicaddress` varchar(15) DEFAULT '',
  `netelasticframedipv6address` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`radacctid`),
  UNIQUE KEY `acctuniqueid` (`acctuniqueid`),
  KEY `username` (`username`),
  KEY `framedipaddress` (`framedipaddress`),
  KEY `framedipv6address` (`framedipv6address`),
  KEY `framedipv6prefix` (`framedipv6prefix`),
  KEY `framedinterfaceid` (`framedinterfaceid`),
  KEY `delegatedipv6prefix` (`delegatedipv6prefix`),
  KEY `acctsessionid` (`acctsessionid`),
  KEY `acctsessiontime` (`acctsessiontime`),
  KEY `acctstarttime` (`acctstarttime`),
  KEY `acctinterval` (`acctinterval`),
  KEY `acctstoptime` (`acctstoptime`),
  KEY `nasipaddress` (`nasipaddress`),
  KEY `class` (`class`)
) ENGINE=InnoDB AUTO_INCREMENT=144 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;''')

# Create Gtel Table radius_netelastic.radreply
cur.execute('''CREATE TABLE `radreply` (
    `username` varchar(64) NOT NULL DEFAULT '',
    `attribute` varchar(64) NOT NULL DEFAULT '',
    `op` varchar(64) NOT NULL DEFAULT '',
    `value` varchar(64) NOT NULL DEFAULT ''
)''')


# Create Gtel Table radius_netelastic.radcheck
cur.execute('''CREATE TABLE `radcheck` (
    `username` varchar(64) NOT NULL DEFAULT '',
    `attribute` varchar(64) NOT NULL DEFAULT '',
    `op` varchar(64) NOT NULL DEFAULT '',
    `value` varchar(64) NOT NULL DEFAULT ''
)''')

# Create Table Logs
cur.execute('''CREATE TABLE `logs` (
    logId INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL DEFAULT 'Gtel',
    reason VARCHAR(10),
    time TIMESTAMP
)''')

########################
# INSERT CONSTANT DATA #
########################


query_1 ='''
INSERT INTO radius_netelastic.radacct (acctsessionid,acctuniqueid,username,realm,nasipaddress,nasportid,nasporttype,acctstarttime,acctupdatetime,acctstoptime,acctinterval,acctsessiontime,acctauthentic,connectinfo_start,connectinfo_stop,acctinputoctets,acctoutputoctets,calledstationid,callingstationid,acctterminatecause,servicetype,framedprotocol,framedipaddress,framedipv6address,framedipv6prefix,framedinterfaceid,delegatedipv6prefix,class,netelasticacctipv6inputoctets,netelasticacctipv6outputoctets,netelasticacctipv6outputpackets,netelasticdomainname,netelasticnatstartport,netelasticnatendport,netelasticusermac,netelasticacctipv6inputpackets,netelasticnatpublicaddress,netelasticframedipv6address) VALUES
	 ('16987801657485840cc6618ed4b10','f8cb040c5b3dd0e437c6947352e32a7f','cc-66-18-ed-4b-10','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 19:22:45','2023-11-01 18:02:45','2023-11-01 18:07:12',600,81867,'RADIUS','','',2350276705,2366940514,'','cc:66:18:ed:4b:10','Admin-Reset','Login-User','','100.64.128.24','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988414810987720002427090b82','bc38e0f20744aaae5115b3579e6ef16b','00-24-27-09-0b-82','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 12:24:40','2023-11-01 13:54:40','2023-11-01 14:00:22',600,5742,'RADIUS','','',41921717348,30689591739,'','00:24:27:09:0b:82','User-Request','Login-User','','100.64.128.28','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987804956888950cc6618ed4f50','6c0ddd6aab84397cf02f4985b02c39fa','cc-66-18-ed-4f-50','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 19:28:15','2023-11-01 17:58:15','2023-11-01 18:07:12',600,81537,'RADIUS','','',557908,1113485,'','cc:66:18:ed:4f:50','Admin-Reset','Login-User','','100.64.128.25','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987800203485080cc6618eae420','c8ec337f07eb37e30c653a2c7257d48d','cc-66-18-ea-e4-20','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-10-31 19:20:20','2023-11-01 18:00:20','2023-11-01 18:07:12',600,82012,'RADIUS','','',4264778141,5269414569,'','cc:66:18:ea:e4:20','Admin-Reset','Login-User','','100.64.128.9','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987800202585400cc6618e73c50','509040b04430d583ff51074b3ff64cc5','cc-66-18-e7-3c-50','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 19:20:20','2023-11-01 18:00:20','2023-11-01 18:07:12',600,82012,'RADIUS','','',2087225196,3110908164,'','cc:66:18:e7:3c:50','Admin-Reset','Login-User','','100.64.128.8','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987800253686130cc6618ebe220','2a6a54bc9f323c5c0c96c768dea460ad','cc-66-18-eb-e2-20','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1002=3D3Bvlanid2=3D3D302','Ethernet','2023-10-31 19:20:25','2023-11-01 18:00:25','2023-11-01 18:07:12',600,82007,'RADIUS','','',2638640346,2018849939,'','cc:66:18:eb:e2:20','Admin-Reset','Login-User','','100.64.128.10','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987800343885840cc6618e73ae0','69a6a34758c5fdc060644791ab607e23','cc-66-18-e7-3a-e0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 19:20:34','2023-11-01 18:00:34','2023-11-01 18:07:12',600,81998,'RADIUS','','',2280901934,2484666150,'','cc:66:18:e7:3a:e0','Admin-Reset','Login-User','','100.64.128.2','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987890408086960cc6618ed4ef0','ad294f1574924cbdb24080c885f747e3','cc-66-18-ed-4e-f0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 21:50:40','2023-11-01 18:00:40','2023-11-01 18:07:12',600,72992,'RADIUS','','',12320648599,15368645849,'','cc:66:18:ed:4e:f0','Admin-Reset','Login-User','','100.64.128.27','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987800473285100cc6618ed5250','a9ce292ada71bbc871acd0c87802e5fc','cc-66-18-ed-52-50','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 19:20:47','2023-11-01 18:00:47','2023-11-01 18:07:12',600,81985,'RADIUS','','',2405287746,2983424108,'','cc:66:18:ed:52:50','Admin-Reset','Login-User','','100.64.128.3','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987800540884490cc6618ef5500','20e676b19d8acf8dc518382745672dbc','cc-66-18-ef-55-00','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1004=3D3Bvlanid2=3D3D304','Ethernet','2023-10-31 19:20:54','2023-11-01 18:00:54','2023-11-01 18:07:12',600,81978,'RADIUS','','',2309806815,2889343651,'','cc:66:18:ef:55:00','Admin-Reset','Login-User','','100.64.128.15','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL);
'''
query_2 = '''
INSERT INTO radius_netelastic.radacct (acctsessionid,acctuniqueid,username,realm,nasipaddress,nasportid,nasporttype,acctstarttime,acctupdatetime,acctstoptime,acctinterval,acctsessiontime,acctauthentic,connectinfo_start,connectinfo_stop,acctinputoctets,acctoutputoctets,calledstationid,callingstationid,acctterminatecause,servicetype,framedprotocol,framedipaddress,framedipv6address,framedipv6prefix,framedinterfaceid,delegatedipv6prefix,class,netelasticacctipv6inputoctets,netelasticacctipv6outputoctets,netelasticacctipv6outputpackets,netelasticdomainname,netelasticnatstartport,netelasticnatendport,netelasticusermac,netelasticacctipv6inputpackets,netelasticnatpublicaddress,netelasticframedipv6address) VALUES
	 ('1698780056558576078c57d1be6e4','c18188df4ec998f24b793bdfb0d7b83b','78-c5-7d-1b-e6-e4','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 19:20:56','2023-11-01 18:00:56','2023-11-01 18:07:12',600,81976,'RADIUS','','',21374226859,26534784712,'','78:c5:7d:1b:e6:e4','Admin-Reset','Login-User','','100.64.128.4','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987800766985480cc6618ed47d0','fdaf999c58021774425624a1149fc5a7','cc-66-18-ed-47-d0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-10-31 19:21:16','2023-11-01 18:01:16','2023-11-01 18:07:12',600,81956,'RADIUS','','',4667058593,6383253643,'','cc:66:18:ed:47:d0','Admin-Reset','Login-User','','100.64.128.11','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987800839985360cc6618ed4830','c5654dc4b296d34cf4283aca39879f32','cc-66-18-ed-48-30','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-10-31 19:21:24','2023-11-01 18:01:24','2023-11-01 18:07:12',600,81948,'RADIUS','','',391648423,632636624,'','cc:66:18:ed:48:30','Admin-Reset','Login-User','','100.64.128.19','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987800864986540cc6618ed4870','a864508ad9e15c3e848f08efed6a890d','cc-66-18-ed-48-70','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-10-31 19:21:26','2023-11-01 18:01:26','2023-11-01 18:07:12',600,81946,'RADIUS','','',2960978909,4855078113,'','cc:66:18:ed:48:70','Admin-Reset','Login-User','','100.64.128.5','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987800971485760cc6618ef54a0','cc762c7cf42a64e80ee38f2ab0247064','cc-66-18-ef-54-a0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 19:21:37','2023-11-01 18:01:37','2023-11-01 18:07:12',600,81935,'RADIUS','','',2151823912,3071932259,'','cc:66:18:ef:54:a0','Admin-Reset','Login-User','','100.64.128.6','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987800997286190cc6618e73f00','2f66926c2c81ecc810ab19992405bb4c','cc-66-18-e7-3f-00','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 19:21:39','2023-11-01 18:01:39','2023-11-01 18:07:12',600,81933,'RADIUS','','',2552578366,2261079783,'','cc:66:18:e7:3f:00','Admin-Reset','Login-User','','100.64.128.7','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987801011585660cc6618ed47c0','275458ffe0fefccdce81bb9bbdcd9e4d','cc-66-18-ed-47-c0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-10-31 19:21:41','2023-11-01 18:01:41','2023-11-01 18:07:12',600,81931,'RADIUS','','',705759798,1326444065,'','cc:66:18:ed:47:c0','Admin-Reset','Login-User','','100.64.128.12','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987801044185550cc66185c3fd0','9601f94b3b72b2f28e8038bb5496482b','cc-66-18-5c-3f-d0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-10-31 19:21:44','2023-11-01 18:01:44','2023-11-01 18:07:12',600,81928,'RADIUS','','',12829549079,16449704631,'','cc:66:18:5c:3f:d0','Admin-Reset','Login-User','','100.64.128.13','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987855051486990cc6618ef5090','b1a79e60c99086131f1355d8aa97f41e','cc-66-18-ef-50-90','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 20:51:45','2023-11-01 18:01:45','2023-11-01 18:07:12',600,76527,'RADIUS','','',2269830178,2893276887,'','cc:66:18:ef:50:90','Admin-Reset','Login-User','','100.64.128.26','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987801081085890cc6618ef5880','1b6e8e2c6b0c83d68a5e4dc00dd88299','cc-66-18-ef-58-80','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 19:21:48','2023-11-01 18:01:48','2023-11-01 18:07:12',600,81924,'RADIUS','','',2299391365,3091232703,'','cc:66:18:ef:58:80','Admin-Reset','Login-User','','100.64.128.14','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL);
'''
query_3 = '''
INSERT INTO radius_netelastic.radacct (acctsessionid,acctuniqueid,username,realm,nasipaddress,nasportid,nasporttype,acctstarttime,acctupdatetime,acctstoptime,acctinterval,acctsessiontime,acctauthentic,connectinfo_start,connectinfo_stop,acctinputoctets,acctoutputoctets,calledstationid,callingstationid,acctterminatecause,servicetype,framedprotocol,framedipaddress,framedipv6address,framedipv6prefix,framedinterfaceid,delegatedipv6prefix,class,netelasticacctipv6inputoctets,netelasticacctipv6outputoctets,netelasticacctipv6outputpackets,netelasticdomainname,netelasticnatstartport,netelasticnatendport,netelasticusermac,netelasticacctipv6inputpackets,netelasticnatpublicaddress,netelasticframedipv6address) VALUES
	 ('16987801114885740cc6618ec69d0','981416904961b3f1a70d60dced4911f1','cc-66-18-ec-69-d0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-10-31 19:21:51','2023-11-01 18:01:51','2023-11-01 18:07:12',600,81921,'RADIUS','','',712378987,1451552302,'','cc:66:18:ec:69:d0','Admin-Reset','Login-User','','100.64.128.16','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987801137684900cc6618ed5180','b30e6911f5d383b0079deaf950560dca','cc-66-18-ed-51-80','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 19:21:53','2023-11-01 18:01:53','2023-11-01 18:07:12',600,81919,'RADIUS','','',2232709372,3043548580,'','cc:66:18:ed:51:80','Admin-Reset','Login-User','','100.64.128.17','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('1698780115538562078c57d1be774','9c9ad1b54cb96215859c2260180b8478','78-c5-7d-1b-e7-74','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 19:21:55','2023-11-01 18:01:55','2023-11-01 18:07:12',600,81917,'RADIUS','','',41139903203,81079743915,'','78:c5:7d:1b:e7:74','Admin-Reset','Login-User','','100.64.128.18','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987801211685720cc6618ef5570','cacd51d2d74f8880f48bc6aa1b41ee1d','cc-66-18-ef-55-70','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 19:22:01','2023-11-01 18:02:01','2023-11-01 18:07:12',600,81911,'RADIUS','','',2497346454,2731580060,'','cc:66:18:ef:55:70','Admin-Reset','Login-User','','100.64.128.20','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987801256285860cc6618ebe160','296c54a70656e324b3336ae4cd41e23d','cc-66-18-eb-e1-60','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1003=3D3Bvlanid2=3D3D303','Ethernet','2023-10-31 19:22:05','2023-11-01 18:02:05','2023-11-01 18:07:12',600,81907,'RADIUS','','',2424888977,2915582634,'','cc:66:18:eb:e1:60','Admin-Reset','Login-User','','100.64.128.21','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987801271685810cc6618e73af0','55a1fe94c757220627d3f547b9d11c1c','cc-66-18-e7-3a-f0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 19:22:07','2023-11-01 18:02:07','2023-11-01 18:07:12',600,81905,'RADIUS','','',2412815341,2907690813,'','cc:66:18:e7:3a:f0','Admin-Reset','Login-User','','100.64.128.22','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16987801280085860cc6618e73ee0','2140756074efc8c02faddd271b5b012c','cc-66-18-e7-3e-e0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-10-31 19:22:08','2023-11-01 18:02:08','2023-11-01 18:07:12',600,81904,'RADIUS','','',6893003670,7560066161,'','cc:66:18:e7:3e:e0','Admin-Reset','Login-User','','100.64.128.23','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988472228785800002427090b82','a392942161645031604bf50b089f8e55','00-24-27-09-0b-82','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 14:00:22','2023-11-01 18:00:22','2023-11-01 18:07:12',600,14810,'RADIUS','','',284791649074,113578250680,'','00:24:27:09:0b:82','Admin-Reset','Login-User','','100.64.128.28','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('1698862059578633078c57d1be774','ce1d3c4a555f24ab5ee32b3cb5ef3519','78-c5-7d-1b-e7-74','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 18:07:39','2023-11-01 18:57:39','2023-11-01 19:02:04',600,3265,'RADIUS','','',12748133236,19263189868,'','78:c5:7d:1b:e7:74','Admin-Reset','Login-User','','100.64.128.2','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988621723485540cc6618ec69d0','04c845b51978396c922ca6676e124189','cc-66-18-ec-69-d0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-01 18:09:32','2023-11-01 18:39:32','2023-11-01 18:42:37',600,1984,'RADIUS','','',693284,295312,'','cc:66:18:ec:69:d0','Admin-Reset','Login-User','','100.64.128.3','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL);
'''

query_4 = '''
INSERT INTO radius_netelastic.radacct (acctsessionid,acctuniqueid,username,realm,nasipaddress,nasportid,nasporttype,acctstarttime,acctupdatetime,acctstoptime,acctinterval,acctsessiontime,acctauthentic,connectinfo_start,connectinfo_stop,acctinputoctets,acctoutputoctets,calledstationid,callingstationid,acctterminatecause,servicetype,framedprotocol,framedipaddress,framedipv6address,framedipv6prefix,framedinterfaceid,delegatedipv6prefix,class,netelasticacctipv6inputoctets,netelasticacctipv6outputoctets,netelasticacctipv6outputpackets,netelasticdomainname,netelasticnatstartport,netelasticnatendport,netelasticusermac,netelasticacctipv6inputpackets,netelasticnatpublicaddress,netelasticframedipv6address) VALUES
	 ('16988622360486330cc6618e73af0','89fbba187b48c93ff9c0fefc6c1cbe12','cc-66-18-e7-3a-f0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 18:10:36','2023-11-01 19:00:35','2023-11-01 19:02:04',600,3089,'RADIUS','','',657723,286019,'','cc:66:18:e7:3a:f0','Admin-Reset','Login-User','','100.64.128.4','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622388785970cc6618e73c50','6d0ed3ec6fe63a0367735252f422aaf1','cc-66-18-e7-3c-50','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 18:10:38','2023-11-01 19:00:38','2023-11-01 19:02:04',600,3086,'RADIUS','','',644348,283916,'','cc:66:18:e7:3c:50','Admin-Reset','Login-User','','100.64.128.5','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622518885840cc6618ef5880','e38f3321200a95c93a9f3e853f781916','cc-66-18-ef-58-80','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 18:10:51','2023-11-01 19:00:51','2023-11-01 19:02:04',600,3073,'RADIUS','','',653460,295428,'','cc:66:18:ef:58:80','Admin-Reset','Login-User','','100.64.128.6','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622519485580cc6618ef5500','95240002989d97b1ec96138566582f8c','cc-66-18-ef-55-00','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1004=3D3Bvlanid2=3D3D304','Ethernet','2023-11-01 18:10:51','2023-11-01 19:00:51','2023-11-01 19:02:04',600,3073,'RADIUS','','',574201,297256,'','cc:66:18:ef:55:00','Admin-Reset','Login-User','','100.64.128.7','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622537085350cc6618ef54a0','5bb7e7dcd3dfee069f2523e2f8f45eff','cc-66-18-ef-54-a0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 18:10:53','2023-11-01 19:00:53','2023-11-01 19:02:04',600,3071,'RADIUS','','',604410,282413,'','cc:66:18:ef:54:a0','Admin-Reset','Login-User','','100.64.128.8','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622546685260cc6618ed4830','ac7cb3fc67c4f485e259cee091322b67','cc-66-18-ed-48-30','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-01 18:10:54','2023-11-01 19:00:54','2023-11-01 19:02:04',600,3070,'RADIUS','','',573345,260082,'','cc:66:18:ed:48:30','Admin-Reset','Login-User','','100.64.128.9','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622552985680cc6618e73ae0','d0db7062ec2752a25bd47d506f95ebd7','cc-66-18-e7-3a-e0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 18:10:55','2023-11-01 19:00:54','2023-11-01 19:02:04',600,3070,'RADIUS','','',606378,280479,'','cc:66:18:e7:3a:e0','Admin-Reset','Login-User','','100.64.128.10','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622555785260cc6618ed5180','2192a8046fdb75c27d475a9a296c5afb','cc-66-18-ed-51-80','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 18:10:55','2023-11-01 19:00:55','2023-11-01 19:02:04',600,3069,'RADIUS','','',668324,292312,'','cc:66:18:ed:51:80','Admin-Reset','Login-User','','100.64.128.11','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622567084260cc6618e73f00','2bc2cdbdd85a6c64a373433c1fc0bc39','cc-66-18-e7-3f-00','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 18:10:56','2023-11-01 19:00:56','2023-11-01 19:02:04',600,3068,'RADIUS','','',594395,264552,'','cc:66:18:e7:3f:00','Admin-Reset','Login-User','','100.64.128.12','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622570285470cc6618ef5090','2d72fbd4bd860759bdd961e4214de41a','cc-66-18-ef-50-90','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 18:10:57','2023-11-01 19:00:56','2023-11-01 19:02:04',600,3068,'RADIUS','','',600802,277023,'','cc:66:18:ef:50:90','Admin-Reset','Login-User','','100.64.128.13','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL);
'''
query_5 = '''INSERT INTO radius_netelastic.radacct (acctsessionid,acctuniqueid,username,realm,nasipaddress,nasportid,nasporttype,acctstarttime,acctupdatetime,acctstoptime,acctinterval,acctsessiontime,acctauthentic,connectinfo_start,connectinfo_stop,acctinputoctets,acctoutputoctets,calledstationid,callingstationid,acctterminatecause,servicetype,framedprotocol,framedipaddress,framedipv6address,framedipv6prefix,framedinterfaceid,delegatedipv6prefix,class,netelasticacctipv6inputoctets,netelasticacctipv6outputoctets,netelasticacctipv6outputpackets,netelasticdomainname,netelasticnatstartport,netelasticnatendport,netelasticusermac,netelasticacctipv6inputpackets,netelasticnatpublicaddress,netelasticframedipv6address) VALUES
	 ('16988622583685160cc6618ed5250','698c7dc91e9fb622ac1b4d5564c651f3','cc-66-18-ed-52-50','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 18:10:58','2023-11-01 19:00:58','2023-11-01 19:02:04',600,3066,'RADIUS','','',591910,269391,'','cc:66:18:ed:52:50','Admin-Reset','Login-User','','100.64.128.14','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622607485550cc6618e73ee0','d7b7898b26f95619b5b07a224b764785','cc-66-18-e7-3e-e0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 18:11:00','2023-11-01 19:01:00','2023-11-01 19:02:04',600,3064,'RADIUS','','',682533,308040,'','cc:66:18:e7:3e:e0','Admin-Reset','Login-User','','100.64.128.15','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622609984670cc6618ef5570','620603cb3007a4c942aae6c41d8de4ad','cc-66-18-ef-55-70','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 18:11:00','2023-11-01 19:01:00','2023-11-01 19:02:04',600,3064,'RADIUS','','',570571,251148,'','cc:66:18:ef:55:70','Admin-Reset','Login-User','','100.64.128.16','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622665285980cc6618ed47c0','2b14f2dfe8b0c1e55042d4b28acda0fa','cc-66-18-ed-47-c0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-01 18:11:06','2023-11-01 19:01:06','2023-11-01 19:02:04',600,3058,'RADIUS','','',607186,282932,'','cc:66:18:ed:47:c0','Admin-Reset','Login-User','','100.64.128.17','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622687485430cc6618ed4b10','d7db70282ff3e34f6fed2a0d35692f8c','cc-66-18-ed-4b-10','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 18:11:08','2023-11-01 19:01:08','2023-11-01 19:02:04',600,3056,'RADIUS','','',587247,264583,'','cc:66:18:ed:4b:10','Admin-Reset','Login-User','','100.64.128.18','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622753585750cc6618eae420','3b37ead059e371c925d7f4fea1ecdba7','cc-66-18-ea-e4-20','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-01 18:11:15','2023-11-01 19:01:15','2023-11-01 19:02:04',600,3049,'RADIUS','','',12099662,74546007,'','cc:66:18:ea:e4:20','Admin-Reset','Login-User','','100.64.128.19','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622804985790cc6618ebe220','ff1e38bee3554f0a885d8745729a0134','cc-66-18-eb-e2-20','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1002=3D3Bvlanid2=3D3D302','Ethernet','2023-11-01 18:11:20','2023-11-01 19:01:20','2023-11-01 19:02:04',600,3044,'RADIUS','','',505463,266084,'','cc:66:18:eb:e2:20','Admin-Reset','Login-User','','100.64.128.20','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622807285140cc6618ebe160','d8dfdf72c347992ccb322e9dd06dec36','cc-66-18-eb-e1-60','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1003=3D3Bvlanid2=3D3D303','Ethernet','2023-11-01 18:11:20','2023-11-01 19:01:20','2023-11-01 19:02:04',600,3044,'RADIUS','','',487242,245496,'','cc:66:18:eb:e1:60','Admin-Reset','Login-User','','100.64.128.21','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622893985720cc6618ed4ef0','b6fb4efef5a9bc821f60859933ea3be0','cc-66-18-ed-4e-f0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 18:11:29','2023-11-01 19:01:29','2023-11-01 19:02:04',600,3035,'RADIUS','','',599160,272248,'','cc:66:18:ed:4e:f0','Admin-Reset','Login-User','','100.64.128.22','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988622911185010cc66185c3fd0','268bf75f7661a855e9380eacadc0d13f','cc-66-18-5c-3f-d0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-01 18:11:31','2023-11-01 19:01:30','2023-11-01 19:02:04',600,3034,'RADIUS','','',2237595,1267355,'','cc:66:18:5c:3f:d0','Admin-Reset','Login-User','','100.64.128.23','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL);
'''
query_6 = '''INSERT INTO radius_netelastic.radacct (acctsessionid,acctuniqueid,username,realm,nasipaddress,nasportid,nasporttype,acctstarttime,acctupdatetime,acctstoptime,acctinterval,acctsessiontime,acctauthentic,connectinfo_start,connectinfo_stop,acctinputoctets,acctoutputoctets,calledstationid,callingstationid,acctterminatecause,servicetype,framedprotocol,framedipaddress,framedipv6address,framedipv6prefix,framedinterfaceid,delegatedipv6prefix,class,netelasticacctipv6inputoctets,netelasticacctipv6outputoctets,netelasticacctipv6outputpackets,netelasticdomainname,netelasticnatstartport,netelasticnatendport,netelasticusermac,netelasticacctipv6inputpackets,netelasticnatpublicaddress,netelasticframedipv6address) VALUES
	 ('16988636645587910002427090b82','3e6ded43494e717d16358ed88b8cca8a','00-24-27-09-0b-82','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 18:34:24','2023-11-01 18:54:24','2023-11-01 19:02:04',600,1660,'RADIUS','','',135117755373,95736350342,'','00:24:27:09:0b:82','Admin-Reset','Login-User','','100.64.128.28','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988643690386280cc6618ec69d0','f478f50ee568277c01f1f48acf41fd40','cc-66-18-ec-69-d0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-01 18:46:09','2023-11-01 18:56:08','2023-11-01 19:02:04',599,956,'RADIUS','','',480068,10372,'','cc:66:18:ec:69:d0','Admin-Reset','Login-User','','204.11.161.130','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('1698865407038610078c57d1be774','d50b662f490f28e6b3fa6fa97222ef0c','78-c5-7d-1b-e7-74','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 19:03:27','2023-11-03 17:53:27','2023-11-03 18:08:13',600,169486,'RADIUS','','',65855698745,115389832305,'','78:c5:7d:1b:e7:74','NAS-Reboot','Login-User','','100.64.128.2','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655059685800002427090b82','8a32462e2cae9b05edc5e26fa7556829','00-24-27-09-0b-82','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 19:05:05','2023-11-02 14:35:05','2023-11-02 14:40:36',600,70530,'RADIUS','','',121056338260,86986523065,'','00:24:27:09:0b:82','User-Request','Login-User','','100.64.128.28','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655272086250cc6618e73af0','8abf2311e1a2c486aaf0687ae79729cf','cc-66-18-e7-3a-f0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 19:05:27','2023-11-03 17:55:27','2023-11-03 18:08:13',600,169366,'RADIUS','','',1787223459,2406415408,'','cc:66:18:e7:3a:f0','NAS-Reboot','Login-User','','100.64.128.3','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655273685150cc66185c3fd0','0b8da4a2382f607fccfc7dac9c4bec71','cc-66-18-5c-3f-d0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-01 19:05:27','2023-11-03 17:55:28','2023-11-03 18:08:13',600,169366,'RADIUS','','',9919137458,55891011403,'','cc:66:18:5c:3f:d0','NAS-Reboot','Login-User','','100.64.128.4','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655295885660cc6618eae420','ae3a79cf34c35b8e5a3a4f12b91ce051','cc-66-18-ea-e4-20','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-01 19:05:29','2023-11-03 17:55:30','2023-11-03 18:08:13',600,169364,'RADIUS','','',11215060006,15630594164,'','cc:66:18:ea:e4:20','NAS-Reboot','Login-User','','100.64.128.5','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655297385190cc6618ef5570','d99bdd106f267ba561185475a858ec88','cc-66-18-ef-55-70','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 19:05:29','2023-11-03 17:55:30','2023-11-03 18:08:13',600,169364,'RADIUS','','',1945625639,2352181809,'','cc:66:18:ef:55:70','NAS-Reboot','Login-User','','100.64.128.6','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655303685880cc6618ed47c0','7628173b16a243710d99ba95cf20fc7b','cc-66-18-ed-47-c0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-01 19:05:30','2023-11-03 17:55:31','2023-11-03 18:08:13',600,169363,'RADIUS','','',1634733774,2486140332,'','cc:66:18:ed:47:c0','NAS-Reboot','Login-User','','100.64.128.7','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655336586120cc6618ef5500','d9d3fb065f77a8b4be795597264fcb6a','cc-66-18-ef-55-00','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1004=3D3Bvlanid2=3D3D304','Ethernet','2023-11-01 19:05:33','2023-11-03 17:55:34','2023-11-03 18:08:13',600,169360,'RADIUS','','',9045852265,11547622091,'','cc:66:18:ef:55:00','NAS-Reboot','Login-User','','100.64.128.8','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL);
'''
query_7 = '''INSERT INTO radius_netelastic.radacct (acctsessionid,acctuniqueid,username,realm,nasipaddress,nasportid,nasporttype,acctstarttime,acctupdatetime,acctstoptime,acctinterval,acctsessiontime,acctauthentic,connectinfo_start,connectinfo_stop,acctinputoctets,acctoutputoctets,calledstationid,callingstationid,acctterminatecause,servicetype,framedprotocol,framedipaddress,framedipv6address,framedipv6prefix,framedinterfaceid,delegatedipv6prefix,class,netelasticacctipv6inputoctets,netelasticacctipv6outputoctets,netelasticacctipv6outputpackets,netelasticdomainname,netelasticnatstartport,netelasticnatendport,netelasticusermac,netelasticacctipv6inputpackets,netelasticnatpublicaddress,netelasticframedipv6address) VALUES
	 ('16988655429485620cc6618e73c50','df119b7ad0dadcb389162710d64d2ed5','cc-66-18-e7-3c-50','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 19:05:42','2023-11-03 17:55:43','2023-11-03 18:08:13',600,169351,'RADIUS','','',3246734108,3204889094,'','cc:66:18:e7:3c:50','NAS-Reboot','Login-User','','100.64.128.9','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655432385190cc6618ef5880','904676b8a63f53926814b989f3b1def8','cc-66-18-ef-58-80','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 19:05:43','2023-11-03 17:55:43','2023-11-03 18:08:13',600,169350,'RADIUS','','',9389533817,9738648813,'','cc:66:18:ef:58:80','NAS-Reboot','Login-User','','100.64.128.10','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655465685720cc6618e73ee0','b2c0d47ed9af5bf3247a0db17984c635','cc-66-18-e7-3e-e0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 19:05:46','2023-11-03 17:55:47','2023-11-03 18:08:13',600,169347,'RADIUS','','',9810725581,9602833760,'','cc:66:18:e7:3e:e0','NAS-Reboot','Login-User','','100.64.128.11','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655468987190cc6618ebe220','ff100eed015d8917233d7319911e7368','cc-66-18-eb-e2-20','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1002=3D3Bvlanid2=3D3D302','Ethernet','2023-11-01 19:05:46','2023-11-03 17:55:47','2023-11-03 18:08:13',600,169347,'RADIUS','','',8130843063,10428082499,'','cc:66:18:eb:e2:20','NAS-Reboot','Login-User','','100.64.128.13','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655468996430cc6618ed5180','71953246533d4244a02294d86ccd1936','cc-66-18-ed-51-80','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 19:05:46','2023-11-03 17:55:47','2023-11-03 18:08:13',600,169347,'RADIUS','','',2044036309,2344316315,'','cc:66:18:ed:51:80','NAS-Reboot','Login-User','','100.64.128.12','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655475385220cc6618ed4b10','3deb581affbd2a9bb7032e59548c3e64','cc-66-18-ed-4b-10','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 19:05:47','2023-11-03 17:55:48','2023-11-03 18:08:13',600,169346,'RADIUS','','',1733691486,2355039327,'','cc:66:18:ed:4b:10','NAS-Reboot','Login-User','','100.64.128.14','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655478685790cc6618ef54a0','75e39502ea15e19fb6cfcecf1481569a','cc-66-18-ef-54-a0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 19:05:47','2023-11-03 17:55:48','2023-11-03 18:08:13',600,169346,'RADIUS','','',8443849144,10887440097,'','cc:66:18:ef:54:a0','NAS-Reboot','Login-User','','100.64.128.15','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655481885800cc6618e73f00','f3eba857fbd5fcda51c2541c5899a76f','cc-66-18-e7-3f-00','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 19:05:48','2023-11-03 17:55:48','2023-11-03 18:08:13',600,169345,'RADIUS','','',2311587558,2399608659,'','cc:66:18:e7:3f:00','NAS-Reboot','Login-User','','100.64.128.16','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655483285570cc6618ef5090','d3dfef52b41aad627a3079fe321f0651','cc-66-18-ef-50-90','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 19:05:48','2023-11-03 17:55:49','2023-11-03 18:08:13',600,169345,'RADIUS','','',1821584157,2379049279,'','cc:66:18:ef:50:90','NAS-Reboot','Login-User','','100.64.128.17','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655494585580cc6618ed5250','abc929db738ea87d266bd6e502326b62','cc-66-18-ed-52-50','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 19:05:49','2023-11-03 17:55:50','2023-11-03 18:08:13',600,169344,'RADIUS','','',2190253593,2411069424,'','cc:66:18:ed:52:50','NAS-Reboot','Login-User','','100.64.128.18','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL);
'''
query_8 = '''INSERT INTO radius_netelastic.radacct (acctsessionid,acctuniqueid,username,realm,nasipaddress,nasportid,nasporttype,acctstarttime,acctupdatetime,acctstoptime,acctinterval,acctsessiontime,acctauthentic,connectinfo_start,connectinfo_stop,acctinputoctets,acctoutputoctets,calledstationid,callingstationid,acctterminatecause,servicetype,framedprotocol,framedipaddress,framedipv6address,framedipv6prefix,framedinterfaceid,delegatedipv6prefix,class,netelasticacctipv6inputoctets,netelasticacctipv6outputoctets,netelasticacctipv6outputpackets,netelasticdomainname,netelasticnatstartport,netelasticnatendport,netelasticusermac,netelasticacctipv6inputpackets,netelasticnatpublicaddress,netelasticframedipv6address) VALUES
	 ('16988655495685560cc6618e73ae0','ffbc58fedd672ea5d8c886506737c604','cc-66-18-e7-3a-e0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 19:05:49','2023-11-03 17:55:50','2023-11-03 18:08:13',600,169344,'RADIUS','','',1906967105,2342471933,'','cc:66:18:e7:3a:e0','NAS-Reboot','Login-User','','100.64.128.19','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655502685440cc6618ebe160','b6847e539257ae19b724a540cf37706c','cc-66-18-eb-e1-60','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1003=3D3Bvlanid2=3D3D303','Ethernet','2023-11-01 19:05:50','2023-11-03 17:55:50','2023-11-03 18:08:13',600,169343,'RADIUS','','',8420460496,11265627618,'','cc:66:18:eb:e1:60','NAS-Reboot','Login-User','','100.64.128.20','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655535485760cc6618ed4830','52c868f44c3792e6e8a84e27d25ee7a0','cc-66-18-ed-48-30','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-01 19:05:53','2023-11-03 11:35:54','2023-11-03 11:36:57',600,145863,'RADIUS','','',1000406425,1196985633,'','cc:66:18:ed:48:30','User-Request','Login-User','','100.64.128.21','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988655536285350cc6618ed4ef0','4e2eb3ab042dc344444cf19bb48caa48','cc-66-18-ed-4e-f0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-01 19:05:53','2023-11-03 17:55:54','2023-11-03 18:08:13',600,169340,'RADIUS','','',9272425222,10502881941,'','cc:66:18:ed:4e:f0','NAS-Reboot','Login-User','','100.64.128.22','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16988656995486370cc6618ec69d0','3e3e6b906b8ae6ed95bb027f85af041e','cc-66-18-ec-69-d0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-01 19:08:19','2023-11-03 11:28:20','2023-11-03 11:36:57',600,145717,'RADIUS','','',1758589971,2980780735,'','cc:66:18:ec:69:d0','User-Request','Login-User','','204.11.161.194','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('1698931845648787078c57d1be6e4','fa266acf3eeb85ebb7578b14c5a5aab0','78-c5-7d-1b-e6-e4','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-02 13:30:45','2023-11-03 17:50:46','2023-11-03 18:08:13',600,103048,'RADIUS','','',323632083153,544007699751,'','78:c5:7d:1b:e6:e4','NAS-Reboot','Login-User','','100.64.128.23','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16989360395986060002427090b82','b71e9daf3c0e9cf4f6d4ee1231e3515c','00-24-27-09-0b-82','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-02 14:40:39','2023-11-02 14:40:39','2023-11-02 14:49:40',NULL,542,'RADIUS','','',26564294620,59338174155,'','00:24:27:09:0b:82','User-Request','Login-User','','100.64.128.24','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16989365811085440002427090b82','596faabb9b632b45909b51ce59525f29','00-24-27-09-0b-82','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-02 14:49:41','2023-11-02 15:39:40','2023-11-02 15:42:56',600,3195,'RADIUS','','',15995595537,44486011814,'','00:24:27:09:0b:82','User-Request','Login-User','','100.64.128.28','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16989397769086000002427090b82','9e5e52c9edbfdd6ce033a649c2308fff','00-24-27-09-0b-82','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-02 15:42:56','2023-11-02 18:02:57','2023-11-02 18:10:57',601,8881,'RADIUS','','',38801375624,62751783774,'','00:24:27:09:0b:82','Admin-Reset','Login-User','','100.64.128.24','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16989486756485530002427090b82','6b776125af44aa2ca3d23545e08e5d43','00-24-27-09-0b-82','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-02 18:11:15','2023-11-03 14:41:15','2023-11-03 14:48:18',600,74222,'RADIUS','','',9667668206,51308600086,'','00:24:27:09:0b:82','Admin-Reset','Login-User','','100.64.128.24','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL);
'''
query_9 = '''INSERT INTO radius_netelastic.radacct (acctsessionid,acctuniqueid,username,realm,nasipaddress,nasportid,nasporttype,acctstarttime,acctupdatetime,acctstoptime,acctinterval,acctsessiontime,acctauthentic,connectinfo_start,connectinfo_stop,acctinputoctets,acctoutputoctets,calledstationid,callingstationid,acctterminatecause,servicetype,framedprotocol,framedipaddress,framedipv6address,framedipv6prefix,framedinterfaceid,delegatedipv6prefix,class,netelasticacctipv6inputoctets,netelasticacctipv6outputoctets,netelasticacctipv6outputpackets,netelasticdomainname,netelasticnatstartport,netelasticnatendport,netelasticusermac,netelasticacctipv6inputpackets,netelasticnatpublicaddress,netelasticframedipv6address) VALUES
	 ('16989525636586020cc6618ed4870','f98ce360ca3455dd5ceefabf3624e1d9','cc-66-18-ed-48-70','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-02 19:16:03','2023-11-03 17:56:03','2023-11-03 18:08:13',600,82330,'RADIUS','','',3436896,1083978,'','cc:66:18:ed:48:70','NAS-Reboot','Login-User','','100.64.128.25','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16989537165286140cc6618ed47d0','154b870a29e90f5af665ad789aa8e4ec','cc-66-18-ed-47-d0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-02 19:35:16','2023-11-03 17:55:16','2023-11-03 18:08:13',600,81177,'RADIUS','','',807270,324495,'','cc:66:18:ed:47:d0','NAS-Reboot','Login-User','','100.64.128.26','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16989550341186800002427090b75','2336e28e12c3dcbaf9004f7450ad20dd','00-24-27-09-0b-75','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-02 19:57:14','2023-11-03 14:37:14','2023-11-03 14:46:27',600,67753,'RADIUS','','',30661267197,41547262870,'','00:24:27:09:0b:75','User-Request','Login-User','','100.64.128.27','','','','',NULL,0,0,0,'',NULL,NULL,'',0,'',NULL),
	 ('16989623902187680cc6618eeb890','e62323155f6d4791a45fc1294113f12d','cc-66-18-ee-b8-90','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-02 21:59:50','2023-11-03 17:59:50','2023-11-03 18:08:13',600,72503,'RADIUS','','',1380935381,2032635133,'','cc:66:18:ee:b8:90','NAS-Reboot','Login-User','','100.64.128.28','','','','',NULL,0,0,0,'my_domain',33500,33999,'cc:66:18:ee:b8:90',0,'',NULL),
	 ('16989631207486940cc66185c3cc0','bd96291a400cdfe5ca4ea79e11a7fe77','cc-66-18-5c-3c-c0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-02 22:12:00','2023-11-03 17:52:00','2023-11-03 18:08:13',600,71773,'RADIUS','','',3954807,40799736,'','cc:66:18:5c:3c:c0','NAS-Reboot','Login-User','','100.64.128.29','','','','',NULL,0,0,0,'my_domain',34000,34499,'cc:66:18:5c:3c:c0',0,'',NULL),
	 ('16990227876386130002427090b75','1ffa16b5c66711e7b1fa6f47abc2bad2','00-24-27-09-0b-75','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 14:46:27','2023-11-03 17:56:27','2023-11-03 18:08:13',600,12106,'RADIUS','','',7517625800,8143286084,'','00:24:27:09:0b:75','NAS-Reboot','Login-User','','100.64.128.21','','','','',NULL,0,0,0,'my_domain',34500,34999,'00:24:27:09:0b:75',0,'',NULL),
	 ('16990229101286540002427090b82','2fa5a651535098f0c30d29a7e2896f70','00-24-27-09-0b-82','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 14:48:30','2023-11-03 17:58:30','2023-11-03 18:08:13',600,11983,'RADIUS','','',14590399806,21544428424,'','00:24:27:09:0b:82','NAS-Reboot','Login-User','','100.64.128.24','','','','',NULL,0,0,0,'my_domain',35000,35499,'00:24:27:09:0b:82',0,'',NULL),
	 ('16990362469056790cc66185c3fd0','bf51b48840e36802263be6194bee83e8','cc-66-18-5c-3f-d0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-03 18:30:46','2023-11-08 13:00:48','2023-11-08 13:02:06',600,412278,'RADIUS','','',251905209365,80684842039,'','cc:66:18:5c:3f:d0','User-Request','Login-User','','100.64.128.4','','','','',NULL,0,0,0,'hwkg_internet_domain',17000,17499,'cc:66:18:5c:3f:d0',0,'',NULL),
	 ('16990362497956270cc6618ed4ef0','bec989a13b8cc32ee463d1b4433ff5b0','cc-66-18-ed-4e-f0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 18:30:49','2023-11-08 13:00:51','2023-11-08 13:02:06',600,412275,'RADIUS','','',20429981430,26546244088,'','cc:66:18:ed:4e:f0','User-Request','Login-User','','100.64.128.5','','','','',NULL,0,0,0,'hwkg_internet_domain',17500,17999,'cc:66:18:ed:4e:f0',0,'',NULL),
	 ('16990362602656510cc6618ef5570','b66fbfd3849ed3bc295a71a9465277df','cc-66-18-ef-55-70','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 18:31:00','2023-11-08 13:01:02','2023-11-08 13:02:06',600,412264,'RADIUS','','',3086676937,4089222447,'','cc:66:18:ef:55:70','User-Request','Login-User','','100.64.128.7','','','','',NULL,0,0,0,'hwkg_internet_domain',18500,18999,'cc:66:18:ef:55:70',0,'',NULL);
'''
query_10 = '''INSERT INTO radius_netelastic.radacct (acctsessionid,acctuniqueid,username,realm,nasipaddress,nasportid,nasporttype,acctstarttime,acctupdatetime,acctstoptime,acctinterval,acctsessiontime,acctauthentic,connectinfo_start,connectinfo_stop,acctinputoctets,acctoutputoctets,calledstationid,callingstationid,acctterminatecause,servicetype,framedprotocol,framedipaddress,framedipv6address,framedipv6prefix,framedinterfaceid,delegatedipv6prefix,class,netelasticacctipv6inputoctets,netelasticacctipv6outputoctets,netelasticacctipv6outputpackets,netelasticdomainname,netelasticnatstartport,netelasticnatendport,netelasticusermac,netelasticacctipv6inputpackets,netelasticnatpublicaddress,netelasticframedipv6address) VALUES
	 ('16990362601455990cc6618ef5090','4988f4da2bb3faecaf9e72751e0be6b3','cc-66-18-ef-50-90','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 18:31:00','2023-11-08 13:01:02','2023-11-08 13:02:06',600,412264,'RADIUS','','',3109679022,4087060288,'','cc:66:18:ef:50:90','User-Request','Login-User','','100.64.128.6','','','','',NULL,0,0,0,'hwkg_internet_domain',18000,18499,'cc:66:18:ef:50:90',0,'',NULL),
	 ('16990362620556490cc6618e73f00','fc4dea839a7b175f1df259a720bff032','cc-66-18-e7-3f-00','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 18:31:01','2023-11-08 13:01:03','2023-11-08 13:02:06',600,412263,'RADIUS','','',3678321688,3746169913,'','cc:66:18:e7:3f:00','User-Request','Login-User','','100.64.128.12','','','','',NULL,0,0,0,'hwkg_internet_domain',21000,21499,'cc:66:18:e7:3f:00',0,'',NULL),
	 ('16990362617356470cc6618ed4b10','c2e8608743b486ffef66e9e2df653820','cc-66-18-ed-4b-10','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 18:31:01','2023-11-08 13:01:03','2023-11-08 13:02:06',600,412263,'RADIUS','','',4294440050,5030328203,'','cc:66:18:ed:4b:10','User-Request','Login-User','','100.64.128.11','','','','',NULL,0,0,0,'hwkg_internet_domain',20500,20999,'cc:66:18:ed:4b:10',0,'',NULL),
	 ('16990362614157770cc6618ebe160','18e00832d384fe344f0c667bfa540699','cc-66-18-eb-e1-60','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1003=3D3Bvlanid2=3D3D303','Ethernet','2023-11-03 18:31:01','2023-11-08 13:01:03','2023-11-08 13:02:06',600,412263,'RADIUS','','',17740925390,21605237718,'','cc:66:18:eb:e1:60','User-Request','Login-User','','100.64.128.10','','','','',NULL,0,0,0,'hwkg_internet_domain',20000,20499,'cc:66:18:eb:e1:60',0,'',NULL),
	 ('16990362612467690cc6618ebe220','06f6c0e5ebb8dbded84880ac947e2c2e','cc-66-18-eb-e2-20','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1002=3D3Bvlanid2=3D3D302','Ethernet','2023-11-03 18:31:01','2023-11-08 13:01:03','2023-11-08 13:02:06',600,412263,'RADIUS','','',19280932130,22159589756,'','cc:66:18:eb:e2:20','User-Request','Login-User','','100.64.128.9','','','','',NULL,0,0,0,'hwkg_internet_domain',19500,19999,'cc:66:18:eb:e2:20',0,'',NULL),
	 ('16990362612458290cc6618e73af0','1a19ae8b48df92f68dce739bbb8ab764','cc-66-18-e7-3a-f0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 18:31:01','2023-11-08 13:01:03','2023-11-08 13:02:06',600,412263,'RADIUS','','',3103669750,4043242082,'','cc:66:18:e7:3a:f0','User-Request','Login-User','','100.64.128.8','','','','',NULL,0,0,0,'hwkg_internet_domain',19000,19499,'cc:66:18:e7:3a:f0',0,'',NULL),
	 ('16990362627956510cc6618eeb890','7ae369e2d0159ea21491b9edcba80897','cc-66-18-ee-b8-90','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-03 18:31:02','2023-11-08 11:41:04','2023-11-08 11:48:25',600,407841,'RADIUS','','',1219814219,1947007086,'','cc:66:18:ee:b8:90','User-Request','Login-User','','100.64.128.15','','','','',NULL,0,0,0,'hwkg_internet_domain',22500,22999,'cc:66:18:ee:b8:90',0,'',NULL),
	 ('16990362624056630cc6618ef5880','82c965e6cce78c26a2f1cd1387bf209f','cc-66-18-ef-58-80','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 18:31:02','2023-11-08 13:01:04','2023-11-08 13:02:06',600,412262,'RADIUS','','',17003227422,20292969640,'','cc:66:18:ef:58:80','User-Request','Login-User','','100.64.128.14','','','','',NULL,0,0,0,'hwkg_internet_domain',22000,22499,'cc:66:18:ef:58:80',0,'',NULL),
	 ('16990362621856550cc6618ed5180','48442bfd8942b7eaecd65534206f3195','cc-66-18-ed-51-80','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 18:31:02','2023-11-08 13:01:04','2023-11-08 13:02:06',600,412262,'RADIUS','','',3546788561,4015682485,'','cc:66:18:ed:51:80','User-Request','Login-User','','100.64.128.13','','','','',NULL,0,0,0,'hwkg_internet_domain',21500,21999,'cc:66:18:ed:51:80',0,'',NULL),
	 ('16990362632556750cc6618ef5500','5ccf196af1f7cc2e7d3b18892baac802','cc-66-18-ef-55-00','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1004=3D3Bvlanid2=3D3D304','Ethernet','2023-11-03 18:31:03','2023-11-08 13:01:05','2023-11-08 13:02:06',600,412261,'RADIUS','','',19681641690,24285801166,'','cc:66:18:ef:55:00','User-Request','Login-User','','100.64.128.16','','','','',NULL,0,0,0,'hwkg_internet_domain',23000,23499,'cc:66:18:ef:55:00',0,'',NULL);
'''
query_11 = '''INSERT INTO radius_netelastic.radacct (acctsessionid,acctuniqueid,username,realm,nasipaddress,nasportid,nasporttype,acctstarttime,acctupdatetime,acctstoptime,acctinterval,acctsessiontime,acctauthentic,connectinfo_start,connectinfo_stop,acctinputoctets,acctoutputoctets,calledstationid,callingstationid,acctterminatecause,servicetype,framedprotocol,framedipaddress,framedipv6address,framedipv6prefix,framedinterfaceid,delegatedipv6prefix,class,netelasticacctipv6inputoctets,netelasticacctipv6outputoctets,netelasticacctipv6outputpackets,netelasticdomainname,netelasticnatstartport,netelasticnatendport,netelasticusermac,netelasticacctipv6inputpackets,netelasticnatpublicaddress,netelasticframedipv6address) VALUES
	 ('16990362645356240cc6618eae420','c44e89a79c9685618e7351fbe0d9dfc8','cc-66-18-ea-e4-20','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-03 18:31:04','2023-11-08 13:01:06','2023-11-08 13:02:06',600,412260,'RADIUS','','',25128620436,27372101928,'','cc:66:18:ea:e4:20','User-Request','Login-User','','100.64.128.18','','','','',NULL,0,0,0,'hwkg_internet_domain',24000,24499,'cc:66:18:ea:e4:20',0,'',NULL),
	 ('16990362641556750cc6618ef54a0','6dea8dc16fc4077be4dc2c693f907d72','cc-66-18-ef-54-a0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 18:31:04','2023-11-08 13:01:06','2023-11-08 13:02:06',600,412260,'RADIUS','','',16151984876,17252084172,'','cc:66:18:ef:54:a0','User-Request','Login-User','','100.64.128.17','','','','',NULL,0,0,0,'hwkg_internet_domain',23500,23999,'cc:66:18:ef:54:a0',0,'',NULL),
	 ('16990362655956810cc6618ed5250','5422d5f1a4ec43121c74e2102004258b','cc-66-18-ed-52-50','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 18:31:05','2023-11-08 13:01:07','2023-11-08 13:02:06',600,412259,'RADIUS','','',3835530666,4063418711,'','cc:66:18:ed:52:50','User-Request','Login-User','','100.64.128.20','','','','',NULL,0,0,0,'hwkg_internet_domain',25000,25499,'cc:66:18:ed:52:50',0,'',NULL),
	 ('16990362655056600cc6618e73ae0','af9478da6f36e5aefa4bdef4434c3976','cc-66-18-e7-3a-e0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 18:31:05','2023-11-08 13:01:07','2023-11-08 13:02:06',600,412259,'RADIUS','','',3079046868,4091799682,'','cc:66:18:e7:3a:e0','User-Request','Login-User','','100.64.128.19','','','','',NULL,0,0,0,'hwkg_internet_domain',24500,24999,'cc:66:18:e7:3a:e0',0,'',NULL),
	 ('16990362680856560cc6618e73c50','2be5509cf9334f3d076fb68a406db078','cc-66-18-e7-3c-50','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 18:31:07','2023-11-08 13:01:09','2023-11-08 13:02:06',600,412257,'RADIUS','','',4275606691,4380829488,'','cc:66:18:e7:3c:50','User-Request','Login-User','','100.64.128.21','','','','',NULL,0,0,0,'hwkg_internet_domain',25500,25999,'cc:66:18:e7:3c:50',0,'',NULL),
	 ('16990384978458230cc6618ed4870','80d151dfc709ce2fa2a33d28a4435661','cc-66-18-ed-48-70','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-03 19:08:18','2023-11-07 07:08:19','2023-11-07 07:11:33',600,302595,'RADIUS','','',11859039350,15982259690,'','cc:66:18:ed:48:70','User-Request','Login-User','','100.64.128.22','','','','',NULL,0,0,0,'hwkg_internet_domain',26500,26999,'cc:66:18:ed:48:70',0,'204.11.161.1',NULL),
	 ('1699036722985850078c57d1be774','5b54da91f6fdf5405ec4bdbf2af6e07e','78-c5-7d-1b-e7-74','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 18:38:43','2023-11-08 12:58:44','2023-11-08 13:02:06',600,411802,'RADIUS','','',95476778823,147331983168,'','78:c5:7d:1b:e7:74','User-Request','Login-User','','100.64.128.2','','','','',NULL,0,0,0,'hwkg_internet_domain',26000,26499,'78:c5:7d:1b:e7:74',0,'204.11.161.1',NULL),
	 ('1699036143565655078c57d1be6e4','8275355a0d6ef6b2990687c30e98594d','78-c5-7d-1b-e6-e4','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-03 18:29:04','2023-11-07 15:09:05','2023-11-07 15:10:32',600,333687,'RADIUS','','',67958581263,174813808119,'','78:c5:7d:1b:e6:e4','Admin-Reset','Login-User','','100.64.128.3','','','','',NULL,0,0,0,'hwkg_internet_domain',16500,16999,'78:c5:7d:1b:e6:e4',0,'204.11.161.1',NULL),
	 ('16992845829157620cc6618e73ee0','458db420eab6a1268bf40c8ed47b7624','cc-66-18-e7-3e-e0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-06 15:29:42','2023-11-08 12:59:43','2023-11-08 13:02:06',600,163943,'RADIUS','','',6031349873,4781248455,'','cc:66:18:e7:3e:e0','User-Request','Login-User','','100.64.128.23','','','','2607:2040:300:8001::/64',NULL,99210,0,0,'hwkg_internet_domain',27500,27999,'cc:66:18:e7:3e:e0',124,'204.11.161.1',NULL),
	 ('16993648093358460002427090b75','ad590a97c5c25699034470d28b14fc98','00-24-27-09-0b-75','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-07 13:46:49','2023-11-08 12:56:49','2023-11-08 13:02:06',600,83717,'RADIUS','','',90703452236,149772469779,'','00:24:27:09:0b:75','User-Request','Login-User','','100.64.128.22','','','','',NULL,0,0,0,'hwkg_internet_domain',28000,28499,'00:24:27:09:0b:75',34,'204.11.161.1',NULL);
'''
query_12 = '''INSERT INTO radius_netelastic.radacct (acctsessionid,acctuniqueid,username,realm,nasipaddress,nasportid,nasporttype,acctstarttime,acctupdatetime,acctstoptime,acctinterval,acctsessiontime,acctauthentic,connectinfo_start,connectinfo_stop,acctinputoctets,acctoutputoctets,calledstationid,callingstationid,acctterminatecause,servicetype,framedprotocol,framedipaddress,framedipv6address,framedipv6prefix,framedinterfaceid,delegatedipv6prefix,class,netelasticacctipv6inputoctets,netelasticacctipv6outputoctets,netelasticacctipv6outputpackets,netelasticdomainname,netelasticnatstartport,netelasticnatendport,netelasticusermac,netelasticacctipv6inputpackets,netelasticnatpublicaddress,netelasticframedipv6address) VALUES
	 ('1699369851115783078c57d1be6e4','682287084b46e74061b24e94bf962b23','78-c5-7d-1b-e6-e4','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-07 15:10:51','2023-11-08 13:00:51','2023-11-08 13:02:06',600,78675,'RADIUS','','',33832526279,60678190525,'','78:c5:7d:1b:e6:e4','User-Request','Login-User','','100.64.128.3','','','','',NULL,683150,0,0,'hwkg_internet_domain',28500,28999,'78:c5:7d:1b:e6:e4',114,'204.11.161.1',NULL),
	 ('16993709670557310cc6618ed4870','37434d320184c1575c2d89a5c7f8f6b1','cc-66-18-ed-48-70','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-07 15:29:27','2023-11-08 12:59:27','2023-11-08 13:02:06',600,77559,'RADIUS','','',844729,370431,'','cc:66:18:ed:48:70','User-Request','Login-User','','100.64.128.24','','','','',NULL,0,0,0,'hwkg_internet_domain',29000,29499,'cc:66:18:ed:48:70',195,'204.11.161.1','2607:2040:300::5'),
	 ('16993959302158760cc6618e73f50','f062aa43cd713c003d60f8c746830cea','cc-66-18-e7-3f-50','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-07 22:25:30','2023-11-08 12:55:30','2023-11-08 13:02:06',600,52596,'RADIUS','','',3665486,4616159,'','cc:66:18:e7:3f:50','User-Request','Login-User','','100.64.128.25','','','','2607:2040:300:8000::/64',NULL,166480,0,0,'hwkg_internet_domain',30000,30499,'cc:66:18:e7:3f:50',70,'204.11.161.1','2607:2040:300::3'),
	 ('16993963329957920cc6618e73fe1','eb9440063c7e21401d4bdb564e160171','cc-66-18-e7-3f-e1','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-07 22:32:13','2023-11-08 12:52:13','2023-11-08 13:02:06',600,52193,'RADIUS','','',17284668,15310156,'','cc:66:18:e7:3f:e1','User-Request','Login-User','','100.64.128.26','','','','2607:2040:300:8002::/64',NULL,1105422,0,0,'hwkg_internet_domain',30500,30999,'cc:66:18:e7:3f:e1',162,'204.11.161.1','2607:2040:300::5'),
	 ('1699448644425610078c57d1be6e4','619acd5306fe27d5c996825d67ad4a36','78-c5-7d-1b-e6-e4','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-08 13:04:04','2023-11-09 16:04:05','2023-11-09 16:13:05',600,97740,'RADIUS','','',18155360694,26007858381,'','78:c5:7d:1b:e6:e4','Admin-Reset','Login-User','','100.64.128.4','','','','',NULL,0,0,0,'hwkg_internet_domain',32000,32499,'78:c5:7d:1b:e6:e4',0,'204.11.161.1',''),
	 ('16994485455257320cc6618e73fe1','db76c0a5f7afb267d54f7f5787a916a3','cc-66-18-e7-3f-e1','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-08 13:02:25','2023-11-09 16:12:26','2023-11-09 16:13:05',600,97840,'RADIUS','','',8480653,5832201,'','cc:66:18:e7:3f:e1','Admin-Reset','Login-User','','100.64.128.2','','','','2607:2040:300:8000::/64',NULL,3145628971,3568842096,0,'hwkg_internet_domain',31000,31499,'cc:66:18:e7:3f:e1',167,'204.11.161.1','2607:2040:300::2'),
	 ('1699448628885758078c57d1be774','ff7f9eca0ed0a191457c2611a6c2c3ad','78-c5-7d-1b-e7-74','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-08 13:03:48','2023-11-08 18:03:48','2023-11-08 18:10:18',600,18390,'RADIUS','','',1979545997,1138196828,'','78:c5:7d:1b:e7:74','Admin-Reset','Login-User','','100.64.128.3','','','','2607:2040:300:8006::/64',NULL,61226,11375,0,'hwkg_internet_domain',31500,31999,'78:c5:7d:1b:e7:74',0,'204.11.161.1',''),
	 ('16994487309257010cc6618e73f50','bc3e2185b9d363a52ea86df67712f6e8','cc-66-18-e7-3f-50','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-08 13:05:30','2023-11-09 16:05:31','2023-11-09 16:13:05',600,97654,'RADIUS','','',13862864,19550272,'','cc:66:18:e7:3f:50','Admin-Reset','Login-User','','100.64.128.5','','','','2607:2040:300:8001::/64',NULL,11636751963,13209402121,0,'hwkg_internet_domain',32500,32999,'cc:66:18:e7:3f:50',26,'204.11.161.1','2607:2040:300::4'),
	 ('16994487334457540cc6618eae420','8ae533943141e5e80569678502e63650','cc-66-18-ea-e4-20','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-08 13:05:33','2023-11-09 16:05:34','2023-11-09 16:13:05',600,97652,'RADIUS','','',5824422163,7972636957,'','cc:66:18:ea:e4:20','Admin-Reset','Login-User','','100.64.128.6','','','','2607:2040:300:8004::/64',NULL,16778113366,18804608306,0,'hwkg_internet_domain',33000,33499,'cc:66:18:ea:e4:20',0,'204.11.161.1',''),
	 ('16994487404756390cc66185c3fd0','37c2fccdc2273a717aeea0948234381b','cc-66-18-5c-3f-d0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-08 13:05:40','2023-11-09 16:05:41','2023-11-09 16:13:05',600,97644,'RADIUS','','',194486380403,32385330707,'','cc:66:18:5c:3f:d0','Admin-Reset','Login-User','','100.64.128.8','','','','',NULL,0,0,0,'hwkg_internet_domain',34000,34499,'cc:66:18:5c:3f:d0',0,'204.11.161.1','');
'''
query_13 = '''INSERT INTO radius_netelastic.radacct (acctsessionid,acctuniqueid,username,realm,nasipaddress,nasportid,nasporttype,acctstarttime,acctupdatetime,acctstoptime,acctinterval,acctsessiontime,acctauthentic,connectinfo_start,connectinfo_stop,acctinputoctets,acctoutputoctets,calledstationid,callingstationid,acctterminatecause,servicetype,framedprotocol,framedipaddress,framedipv6address,framedipv6prefix,framedinterfaceid,delegatedipv6prefix,class,netelasticacctipv6inputoctets,netelasticacctipv6outputoctets,netelasticacctipv6outputpackets,netelasticdomainname,netelasticnatstartport,netelasticnatendport,netelasticusermac,netelasticacctipv6inputpackets,netelasticnatpublicaddress,netelasticframedipv6address) VALUES
	 ('16994487403956820cc6618ef5500','6538be110da349b6fcecad6e5f9a88df','cc-66-18-ef-55-00','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1004=3D3Bvlanid2=3D3D304','Ethernet','2023-11-08 13:05:40','2023-11-09 12:55:41','2023-11-09 13:05:40',600,86400,'RADIUS','','',595160,290736,'','cc:66:18:ef:55:00','User-Request','Login-User','','100.64.128.7','','','','',NULL,0,0,0,'hwkg_internet_domain',33500,33999,'cc:66:18:ef:55:00',0,'204.11.161.1',''),
	 ('16994487457738320cc6618ebe220','b380fdb5062f8bafc930e19ab7629b95','cc-66-18-eb-e2-20','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1002=3D3Bvlanid2=3D3D302','Ethernet','2023-11-08 13:05:45','2023-11-09 16:05:46','2023-11-09 16:13:05',600,97639,'RADIUS','','',4546205416,4575756253,'','cc:66:18:eb:e2:20','Admin-Reset','Login-User','','100.64.128.9','','','','2607:2040:300:8007::/64',NULL,3561626372,4092241448,0,'hwkg_internet_domain',34500,34999,'cc:66:18:eb:e2:20',0,'204.11.161.1',''),
	 ('16994487559356680cc6618ebe160','3d8b19cf2379eb73605b8be06a3e2e20','cc-66-18-eb-e1-60','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1003=3D3Bvlanid2=3D3D303','Ethernet','2023-11-08 13:05:55','2023-11-09 12:55:56','2023-11-09 13:05:55',600,86400,'RADIUS','','',591376,267231,'','cc:66:18:eb:e1:60','User-Request','Login-User','','100.64.128.10','','','','',NULL,0,0,0,'hwkg_internet_domain',35000,35499,'cc:66:18:eb:e1:60',0,'204.11.161.1',''),
	 ('16994487717856860cc6618ed4ef0','e3505b569ea57053949bd57d6723cc61','cc-66-18-ed-4e-f0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-08 13:06:11','2023-11-09 16:06:12','2023-11-09 16:13:05',600,97613,'RADIUS','','',1879871019,2573158437,'','cc:66:18:ed:4e:f0','Admin-Reset','Login-User','','100.64.128.11','','','','2607:2040:300:8005::/64',NULL,1197928808,1255883613,0,'hwkg_internet_domain',35500,35999,'cc:66:18:ed:4e:f0',0,'204.11.161.1',''),
	 ('16994493520957340cc6618e73ee0','136de11c609bf0ed1ce89bf3a80c0b98','cc-66-18-e7-3e-e0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-08 13:15:51','2023-11-09 16:05:52','2023-11-09 16:13:05',600,97033,'RADIUS','','',5449571,2112798,'','cc:66:18:e7:3e:e0','Admin-Reset','Login-User','','100.64.128.12','','','','2607:2040:300:8002::/64',NULL,2503470999,2540464973,0,'hwkg_internet_domain',36000,36499,'cc:66:18:e7:3e:e0',100,'204.11.161.1','2607:2040:300::5'),
	 ('16994558818156470cc6618ebe110','03a558ecdba7491738a2815fb64ef2c8','cc-66-18-eb-e1-10','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-08 15:04:41','2023-11-09 16:04:42','2023-11-09 16:13:05',600,90503,'RADIUS','','',1501918,705723,'','cc:66:18:eb:e1:10','Admin-Reset','Login-User','','100.64.128.13','','','','',NULL,0,0,0,'hwkg_internet_domain',36500,36999,'cc:66:18:eb:e1:10',89,'204.11.161.1','2607:2040:300::6'),
	 ('16994605674157240d41ad1fa462c','a7f52021f94fd64a8f9f2c62e05f5c17','d4-1a-d1-fa-46-2c','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1004=3D3Bvlanid2=3D3D304','Ethernet','2023-11-08 16:22:47','2023-11-09 16:12:48','2023-11-09 16:13:05',600,85817,'RADIUS','','',2358,3311,'','d4:1a:d1:fa:46:2c','Admin-Reset','Login-User','','100.64.128.14','','','','',NULL,0,0,0,'hwkg_internet_domain',37000,37499,'d4:1a:d1:fa:46:2c',0,'204.11.161.1','2607:2040:300::a'),
	 ('1699467020325688078c57d1be774','1235a0f7c7dc82c44fe7fb0922d1e339','78-c5-7d-1b-e7-74','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1004=3D3Bvlanid2=3D3D304','Ethernet','2023-11-08 18:10:20','2023-11-09 16:10:21','2023-11-09 16:13:05',600,79364,'RADIUS','','',5155865216,9605297834,'','78:c5:7d:1b:e7:74','Admin-Reset','Login-User','','100.64.128.3','','','','',NULL,57971051405,27833371392,2914171,'hwkg_internet_domain',37500,37999,'78:c5:7d:1b:e7:74',5019159,'204.11.161.1','2607:2040:300::9'),
	 ('16994759444058490cc6618eeb890','29f1038d0b93a1730a40eb34527dac09','cc-66-18-ee-b8-90','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-08 20:39:04','2023-11-09 16:09:05','2023-11-09 16:13:05',145,70441,'RADIUS','','',570056,406021,'','cc:66:18:ee:b8:90','Admin-Reset','Login-User','','100.64.128.15','','','','2607:2040:300:8003::/64',NULL,1076295,433915,378,'hwkg_internet_domain',38000,38499,'cc:66:18:ee:b8:90',446,'204.11.161.1','2607:2040:300::6'),
	 ('16994784067958370002427090b75','2a540659d31fb9f512e98a2ada4cbf79','00-24-27-09-0b-75','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-08 21:20:06','2023-11-08 22:50:06','2023-11-08 22:51:15',600,5469,'RADIUS','','',5759208,537211238,'','00:24:27:09:0b:75','User-Request','Login-User','','100.64.144.25','','','','',NULL,0,0,2054390,'hwkg_internet_domain',38500,38999,'00:24:27:09:0b:75',1744617,'204.11.161.1','2607:2040:300::b');
'''
query_14 = '''INSERT INTO radius_netelastic.radacct (acctsessionid,acctuniqueid,username,realm,nasipaddress,nasportid,nasporttype,acctstarttime,acctupdatetime,acctstoptime,acctinterval,acctsessiontime,acctauthentic,connectinfo_start,connectinfo_stop,acctinputoctets,acctoutputoctets,calledstationid,callingstationid,acctterminatecause,servicetype,framedprotocol,framedipaddress,framedipv6address,framedipv6prefix,framedinterfaceid,delegatedipv6prefix,class,netelasticacctipv6inputoctets,netelasticacctipv6outputoctets,netelasticacctipv6outputpackets,netelasticdomainname,netelasticnatstartport,netelasticnatendport,netelasticusermac,netelasticacctipv6inputpackets,netelasticnatpublicaddress,netelasticframedipv6address) VALUES
	 ('16994838760756280002427090b75','68b31cdd17462a954f765b0c3e010039','00-24-27-09-0b-75','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-08 22:51:15','2023-11-09 16:11:16','2023-11-09 16:13:05',600,62509,'RADIUS','','',359510,469889,'','00:24:27:09:0b:75','Admin-Reset','Login-User','','100.64.128.16','','','','',NULL,0,0,1401883,'hwkg_internet_domain',39000,39499,'00:24:27:09:0b:75',727367,'204.11.161.1','2607:2040:300::9'),
	 ('16995394062157420cc6618e73f00','5bb4e4177cbb4c1e455775087cbe1fdb','cc-66-18-e7-3f-00','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-09 14:16:46','2023-11-09 15:46:46','2023-11-09 15:51:11',600,5666,'RADIUS','','',393357,302154,'','cc:66:18:e7:3f:00','Admin-Reset','Login-User','','100.64.128.7','','','','2607:2040:300:8003::/64',NULL,972909,406757,778,'hwkg_internet_domain',39500,39999,'cc:66:18:e7:3f:00',955,'204.11.161.1','2607:2040:300::9'),
	 ('16995452539557420cc6618e73f00','f8f98ea4344aaa2b1762c364eff11d8c','cc-66-18-e7-3f-00','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-09 15:54:14','2023-11-09 16:04:14','2023-11-09 16:13:05',NULL,1132,'RADIUS','','',243701125,253528715,'','cc:66:18:e7:3f:00','Admin-Reset','Login-User','','204.11.161.199','','','','',NULL,0,0,0,'hwkg_internet_domain',40000,40499,'cc:66:18:e7:3f:00',0,'204.11.161.1',''),
	 ('1699546724905824078c57d1be774','6c4dc44a9757cdea9b94f5b1e205a5a5','78-c5-7d-1b-e7-74','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1004=3D3Bvlanid2=3D3D304','Ethernet','2023-11-09 16:18:44','2023-11-09 16:48:45',NULL,600,1800,'RADIUS','','',554869,144305,'','78:c5:7d:1b:e7:74','','Login-User','','100.64.128.2','','','','',NULL,16872,11322,0,'hwkg_internet_domain',42000,42499,'78:c5:7d:1b:e7:74',0,'204.11.161.1','2607:2040:300::2'),
	 ('16995472473458670cc6618e73fe1','d3f1e0cdcbd208ea238480ae507e0599','cc-66-18-e7-3f-e1','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-09 16:27:27','2023-11-09 16:47:27',NULL,600,1200,'RADIUS','','',122530,128169,'','cc:66:18:e7:3f:e1','','Login-User','','100.64.128.7','','','','2607:2040:300:8003::/64',NULL,555333,236013,0,'hwkg_internet_domain',45000,45499,'cc:66:18:e7:3f:e1',0,'204.11.161.1','2607:2040:300::6'),
	 ('16995467772156460cc6618e73f00','d8cf431f051f1fc392f27d500a3257f6','cc-66-18-e7-3f-00','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-09 16:19:37','2023-11-09 16:49:37',NULL,600,1800,'RADIUS','','',264780,99720,'','cc:66:18:e7:3f:00','','Login-User','','204.11.161.199','','','','',NULL,0,0,0,'hwkg_internet_domain',43000,43499,'cc:66:18:e7:3f:00',0,'204.11.161.1',''),
	 ('16995467767356900cc66185c3fd0','7f5fa0208cc40b0f49b5feaeabee7804','cc-66-18-5c-3f-d0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-09 16:19:37','2023-11-09 16:49:37',NULL,600,1800,'RADIUS','','',1889592483,1412223452,'','cc:66:18:5c:3f:d0','','Login-User','','100.64.128.3','','','','',NULL,0,0,0,'hwkg_internet_domain',42500,42999,'cc:66:18:5c:3f:d0',0,'204.11.161.1',''),
	 ('16995472413157130cc6618eeb890','b218fe09712e9f69de82a4f7212c6235','cc-66-18-ee-b8-90','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-09 16:27:21','2023-11-09 16:47:21',NULL,600,1200,'RADIUS','','',129024,127977,'','cc:66:18:ee:b8:90','','Login-User','','100.64.128.4','','','','2607:2040:300:8000::/64',NULL,3848925757,4533045960,3195427,'hwkg_internet_domain',43500,43999,'cc:66:18:ee:b8:90',2677757,'204.11.161.1','2607:2040:300::3'),
	 ('16995472431456380cc6618e73ee0','00bd37be94209e5b17ce831a779668a9','cc-66-18-e7-3e-e0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-09 16:27:23','2023-11-09 16:47:23',NULL,600,1200,'RADIUS','','',86010,81871,'','cc:66:18:e7:3e:e0','','Login-User','','100.64.128.5','','','','2607:2040:300:8001::/64',NULL,400788,177507,563,'hwkg_internet_domain',44000,44499,'cc:66:18:e7:3e:e0',713,'204.11.161.1','2607:2040:300::4'),
	 ('16995472452656170cc6618ed4ef0','0e595a152defe5d2be7e89b4f75ae39a','cc-66-18-ed-4e-f0','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-09 16:27:25','2023-11-09 16:47:25',NULL,600,1200,'RADIUS','','',211901,192016,'','cc:66:18:ed:4e:f0','','Login-User','','100.64.128.6','','','','2607:2040:300:8002::/64',NULL,1406380,485524,1894,'hwkg_internet_domain',44500,44999,'cc:66:18:ed:4e:f0',2218,'204.11.161.1','2607:2040:300::5');
'''
query_15 = '''INSERT INTO radius_netelastic.radacct (acctsessionid,acctuniqueid,username,realm,nasipaddress,nasportid,nasporttype,acctstarttime,acctupdatetime,acctstoptime,acctinterval,acctsessiontime,acctauthentic,connectinfo_start,connectinfo_stop,acctinputoctets,acctoutputoctets,calledstationid,callingstationid,acctterminatecause,servicetype,framedprotocol,framedipaddress,framedipv6address,framedipv6prefix,framedinterfaceid,delegatedipv6prefix,class,netelasticacctipv6inputoctets,netelasticacctipv6outputoctets,netelasticacctipv6outputpackets,netelasticdomainname,netelasticnatstartport,netelasticnatendport,netelasticusermac,netelasticacctipv6inputpackets,netelasticnatpublicaddress,netelasticframedipv6address) VALUES
	 ('16995472496156380cc6618e73f50','cce13e8457870585f685e11db77f3145','cc-66-18-e7-3f-50','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1005=3D3Bvlanid2=3D3D305','Ethernet','2023-11-09 16:27:30','2023-11-09 16:47:30',NULL,600,1200,'RADIUS','','',95715,97586,'','cc:66:18:e7:3f:50','','Login-User','','100.64.128.8','','','','2607:2040:300:8004::/64',NULL,390355,172525,564,'hwkg_internet_domain',45500,45999,'cc:66:18:e7:3f:50',664,'204.11.161.1','2607:2040:300::7'),
	 ('16995472512458290cc6618ebe220','45bdd817b1bc028f19633354bc00d44e','cc-66-18-eb-e2-20','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1002=3D3Bvlanid2=3D3D302','Ethernet','2023-11-09 16:27:31','2023-11-09 16:47:31',NULL,600,1200,'RADIUS','','',71571,79321,'','cc:66:18:eb:e2:20','','Login-User','','100.64.128.9','','','','2607:2040:300:8005::/64',NULL,391570,162704,553,'hwkg_internet_domain',46000,46499,'cc:66:18:eb:e2:20',668,'204.11.161.1','2607:2040:300::8'),
	 ('16995472831056720cc6618eae420','f4bc195e01be94b48118f44a941cc334','cc-66-18-ea-e4-20','','10.255.0.103','slot=3D3D0=3D3Bsubslot=3D3D0=3D3Bport=3D3D1=3D3Bvlanid=3D3D1011=3D3Bvlanid2=3D3D301','Ethernet','2023-11-09 16:28:03','2023-11-09 16:48:03',NULL,600,1200,'RADIUS','','',553107,630310,'','cc:66:18:ea:e4:20','','Login-User','','100.64.128.10','','','','2607:2040:300:8006::/64',NULL,3029844,1993857,4102,'hwkg_internet_domain',46500,46999,'cc:66:18:ea:e4:20',4524,'204.11.161.1','2607:2040:300::9');
'''
cur.execute(query_1)
cur.execute(query_2)
cur.execute(query_3)
cur.execute(query_4)
cur.execute(query_5)
cur.execute(query_6)
cur.execute(query_7)
cur.execute(query_8)
cur.execute(query_9)
cur.execute(query_10)
cur.execute(query_11)
cur.execute(query_12)
cur.execute(query_13)
cur.execute(query_14)
cur.execute(query_15)

cur.execute('''INSERT INTO radius_netelastic.radreply (username,`attribute`,op,value) VALUES
	 ('cc-66-18-ec-69-d0','Framed-IP-Address','=','204.11.161.194'),
	 ('CC-66-18-E7-3f-00','Framed-IP-Address','=','204.11.161.199'),
	 ('CC-66-18-E7-3f-00','Framed-IPv6-Prefix','=','2607:2040:300:800A::1/64'),
	 ('CC-66-18-E7-3f-00','Framed-IPv6-Address','=','2607:2040:300:800A::1/64');''')
 
cur.execute('''INSERT INTO radius_netelastic.radcheck (username,`attribute`,op,value) VALUES
	 ('aa-bb-cc-dd-ee-ff','Cleartext-Password',':=',' aa-bb-cc-dd-ee-ff'),
	 ('cc-66-18-ec-69-d0','Cleartext-Password','=','cc-66-18-ec-69-d0'),
	 ('ben','Cleartext-Password',':=','ben'),
	 ('tim','Cleartext-Password',':=','tim'),
	 ('CC-66-18-E7-3f-00','Cleartext-Password',':=','CC-66-18-E7-3f-00');''')


cur.execute(''' INSERT INTO radius_netelastic.logs(username, reason, time)
            	VALUES ('Steve B', 'Added', NOW())''')
cur.execute(''' INSERT INTO radius_netelastic.logs(username, reason, time)
            	VALUES ('Liam', 'Added', NOW())''')
cur.execute(''' INSERT INTO radius_netelastic.logs(username, reason, time)
            	VALUES ('Easton', 'Deleted', NOW())''')
cur.execute(''' INSERT INTO radius_netelastic.logs(username, reason, time)
            	VALUES ('Nick', 'Edit', NOW())''')
cur.execute(''' INSERT INTO radius_netelastic.logs(username, reason, time)
            	VALUES ('Christian', 'Deleted', NOW())''')
cur.execute(''' INSERT INTO radius_netelastic.logs(username, reason, time)
            	VALUES ('Algozzine', 'Edit', NOW())''')
cur.execute(''' INSERT INTO radius_netelastic.logs(username, reason, time)
            	VALUES ('Devon', 'Edit', NOW())''')
cur.execute(''' INSERT INTO radius_netelastic.logs(username, reason, time)
            	VALUES ('Eagle', 'Edit', NOW())''')
cur.execute(''' INSERT INTO radius_netelastic.logs(username, reason, time)
            	VALUES ('Appy.py', 'Edit', NOW())''')
cur.execute(''' INSERT INTO radius_netelastic.logs(username, reason, time)
            	VALUES ('Appy.py', 'Deleted', NOW())''')
cur.execute(''' INSERT INTO radius_netelastic.logs(username, reason, time)
            	VALUES ('Appy.py', 'Added', NOW())''')
cur.execute(''' INSERT INTO radius_netelastic.logs(username, reason, time)
            	VALUES ('Appy.py', 'Deleted', NOW())''')
cur.execute(''' INSERT INTO radius_netelastic.logs(username, reason, time)
            	VALUES ('Appy.py', 'Added', NOW())''')
conn.commit()

##################
# CRUD FUNCTIONS # 
##################
#Add or Update Radcheck and Radreply based on username IPV4,IPv6Prefix
cur.execute('''CREATE DEFINER=`root`@`localhost` PROCEDURE `radius_netelastic`.`PROC_InsUpRadiusUser`(
    p_userName VARCHAR(64),
    p_ipv4 VARCHAR(15),
    p_ipv6Prefix VARCHAR(45),
    p_ipv6 VARCHAR(45)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;

        GET DIAGNOSTICS CONDITION 1 @p1 = MYSQL_ERRNO, @p2 = MESSAGE_TEXT;

        SIGNAL SQLSTATE '45000' SET MYSQL_ERRNO = @p1, MESSAGE_TEXT = @p2;
    END;

    START TRANSACTION;

    /*
     * Insert the user if it does not exist
     */
    INSERT INTO radius_netelastic.radcheck (username, `attribute`, op, value)
    SELECT p_userName, 'Cleartext-Password', ':=', p_userName
    WHERE NOT EXISTS (
        SELECT *
        FROM radius_netelastic.radcheck
        WHERE username = p_userName
    );

    /* Update the ipv4 if it exists */
    UPDATE radius_netelastic.radreply
    SET value = p_ipv4
    WHERE `attribute` = 'Framed-IP-Address' AND username = p_userName;

    /* Update the prefix ipv6 if it exists */
    UPDATE radius_netelastic.radreply
    SET value = p_ipv6Prefix
    WHERE `attribute` = 'Framed-IPv6-Prefix' AND username = p_userName;

    /* Update the ipv6 if it exists */
    UPDATE radius_netelastic.radreply
    SET value = p_ipv6
    WHERE `attribute` = 'Framed-IPv6-Address' AND username = p_userName;

    /* Add the ipv4 if it does not exist */
    INSERT INTO radius_netelastic.radreply (username, `attribute`, op, value)
    SELECT p_userName, 'Framed-IP-Address', '=', p_ipv4
    WHERE NOT EXISTS (
        SELECT *
        FROM radius_netelastic.radreply
        WHERE username = p_userName AND `attribute` = 'Framed-IP-Address'
    );

    /* Add the ipv6 prefix if it does not exist */
    INSERT INTO radius_netelastic.radreply (username, `attribute`, op, value)
    SELECT p_userName, 'Framed-IPv6-Prefix', '=', p_ipv6Prefix
    WHERE NOT EXISTS (
        SELECT *
        FROM radius_netelastic.radreply
        WHERE username = p_userName AND `attribute` = 'Framed-IPv6-Prefix'
    );

    /* Add the ipv6 if it does not exist */
    INSERT INTO radius_netelastic.radreply (username, `attribute`, op, value)
    SELECT p_userName, 'Framed-IPv6-Address', '=', p_ipv6
    WHERE NOT EXISTS (
        SELECT *
        FROM radius_netelastic.radreply
        WHERE username = p_userName AND `attribute` = 'Framed-IPv6-Address'
    );

    /* SELECT *
    FROM radius_netelastic.radreply
    WHERE username = p_userName; */

    COMMIT;
END;
''')

#Delete MAC from Radcheck and Radreply
cur.execute('''CREATE PROCEDURE radius_netelastic.PROC_DeleteRadiusUser(p_userName VARCHAR(64))
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        GET DIAGNOSTICS CONDITION 1 @p1 = MYSQL_ERRNO, @p2 = MESSAGE_TEXT;

        SIGNAL SQLSTATE '45000' SET MYSQL_ERRNO = @p1, MESSAGE_TEXT = @p2;
    END;

    START TRANSACTION;
    DELETE FROM radius_netelastic.radcheck WHERE username = p_userName;
    DELETE FROM radius_netelastic.radreply WHERE username = p_userName;
    COMMIT;
END;
''')

conn.commit()



###########
# LOCK UP #
###########

cur.execute("LOCK TABLES radius_netelastic.radacct WRITE;")
cur.execute("/*!40000 ALTER TABLE radius_netelastic.radacct DISABLE KEYS */;")
cur.execute("LOCK TABLES `radreply` WRITE;")
cur.execute("/*!40000 ALTER TABLE `radreply` DISABLE KEYS */;")
cur.execute("LOCK TABLES `radcheck` WRITE;")
cur.execute("/*!40000 ALTER TABLE `radcheck` DISABLE KEYS */;")
cur.execute("LOCK TABLES `logs` WRITE;")
cur.execute("/*!40000 ALTER TABLE `logs` DISABLE KEYS */;")

# This statement is used to restore the MySQL session's time zone to the value it had before the script or tool made any changes. 
# It sets the TIME_ZONE session variable back to its previous value.
cur.execute("/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;")
# It restores the SQL mode of the session to the value it had before any modifications. 
# The SQL_MODE variable controls various aspects of MySQL's SQL behavior.
cur.execute("/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;")
# It sets the FOREIGN_KEY_CHECKS session variable back to its previous value. 
# This variable controls whether foreign key constraints are checked when making changes to the database.
cur.execute("/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;")
# Similar to the previous statement, this restores the UNIQUE_CHECKS variable to its previous value, 
# controlling how unique constraints are enforced.
cur.execute("/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;")
# Restores the character set used by the client connection to its previous setting. It affects how text data is sent and received.
cur.execute("/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;")
# This statement reverts the CHARACTER_SET_RESULTS variable, which specifies the character set in which query results are returned.
cur.execute("/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;")
# Restores the COLLATION_CONNECTION variable to its previous setting. It specifies the collation for the connection.
cur.execute("/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;")
# Restores the SQL_NOTES variable to its previous value. This variable controls the behavior of MySQL regarding comments in SQL statements.
cur.execute("/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;")
conn.commit()

cur.execute('UNLOCK TABLES')

##################
# CRUD FUNCTIONS # 
##################

#Add or Update Radcheck and Radreply based on username IPV4,IPv6Per
cur.execute('''CREATE DEFINER=`root`@`localhost` PROCEDURE `radius_netelastic`.`PROC_InsUpRadiusUser`(
    p_userName VARCHAR(64),
    p_ipv4 VARCHAR(15),
    p_ipv6Perfix VARCHAR(45),
    p_ipv6 VARCHAR(45)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;

        GET DIAGNOSTICS CONDITION 1 @p1 = MYSQL_ERRNO, @p2 = MESSAGE_TEXT;

        SIGNAL SQLSTATE '45000' SET MYSQL_ERRNO = @p1, MESSAGE_TEXT = @p2;
    END;

    START TRANSACTION;

    /*
     * Insert the user if it does not exist
     */
    INSERT INTO radius_netelastic.radcheck (username, `attribute`, op, value)
    SELECT p_userName, 'Cleartext-Password', ':=', p_userName
    WHERE NOT EXISTS (
        SELECT *
        FROM radius_netelastic.radcheck
        WHERE username = p_userName
    );

    /* Update the ipv4 if it exists */
    UPDATE radius_netelastic.radreply
    SET value = p_ipv4
    WHERE `attribute` = 'Framed-IP-Address' AND username = p_userName;

    /* Update the prefix ipv6 if it exists */
    UPDATE radius_netelastic.radreply
    SET value = p_ipv6Perfix
    WHERE `attribute` = 'Framed-IPv6-Prefix' AND username = p_userName;

    /* Update the ipv6 if it exists */
    UPDATE radius_netelastic.radreply
    SET value = p_ipv6
    WHERE `attribute` = 'Framed-IPv6-Address' AND username = p_userName;

    /* Add the ipv4 if it does not exist */
    INSERT INTO radius_netelastic.radreply (username, `attribute`, op, value)
    SELECT p_userName, 'Framed-IP-Address', '=', p_ipv4
    WHERE NOT EXISTS (
        SELECT *
        FROM radius_netelastic.radreply
        WHERE username = p_userName AND `attribute` = 'Framed-IP-Address'
    );

    /* Add the ipv6 prefix if it does not exist */
    INSERT INTO radius_netelastic.radreply (username, `attribute`, op, value)
    SELECT p_userName, 'Framed-IPv6-Prefix', '=', p_ipv6Perfix
    WHERE NOT EXISTS (
        SELECT *
        FROM radius_netelastic.radreply
        WHERE username = p_userName AND `attribute` = 'Framed-IPv6-Prefix'
    );

    /* Add the ipv6 if it does not exist */
    INSERT INTO radius_netelastic.radreply (username, `attribute`, op, value)
    SELECT p_userName, 'Framed-IPv6-Address', '=', p_ipv6
    WHERE NOT EXISTS (
        SELECT *
        FROM radius_netelastic.radreply
        WHERE username = p_userName AND `attribute` = 'Framed-IPv6-Address'
    );

    /* SELECT *
    FROM radius_netelastic.radreply
    WHERE username = p_userName; */

    COMMIT;
END;
''')

#Delete MAC from Radcheck and Radreply
cur.execute('''CREATE PROCEDURE radius_netelastic.PROC_DeleteRadiusUser(p_userName VARCHAR(64))
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        GET DIAGNOSTICS CONDITION 1 @p1 = MYSQL_ERRNO, @p2 = MESSAGE_TEXT;

        SIGNAL SQLSTATE '45000' SET MYSQL_ERRNO = @p1, MESSAGE_TEXT = @p2;
    END;

    START TRANSACTION;
    DELETE FROM radius_netelastic.radcheck WHERE username = p_userName;
    DELETE FROM radius_netelastic.radreply WHERE username = p_userName;
    COMMIT;
END;
''')

conn.commit()

#########
# Flask #
#########

@app.route("/index")
def index():
    return "Connected to database"


if __name__ == "__main__":
    app.run()


















