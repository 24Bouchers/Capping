# python -m pip install flask
# pip3 install pymysql
# pip install mysql-connector-python
# mysql -u root -p : Login for consol
from flask import Flask
import pymysql
import sys

######################
# CONNECT TO MARIADB #
######################

# Attempt to connect with current credentials
# currently set to localhost
# Maybe for website purposes have username and password be the same as website login
# This could be easy access for credentials of who can manipulate the DB

app = Flask(__name__)
#Toggle to run locally or on the vm


conn = pymysql.connect(host='localhost', user='root', password='ArchFiber23', db='radius_netelastic')

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

#Check Raddact.png for an easy display of information
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
cur.execute("LOCK TABLES radius_netelastic.radacct WRITE;")
cur.execute("/*!40000 ALTER TABLE radius_netelastic.radacct DISABLE KEYS */;")
cur.execute("UNLOCK TABLES")

# Create Gtel Table radius_netelastic.radreply
cur.execute('''CREATE TABLE `radreply` (
    `username` varchar(64) NOT NULL DEFAULT '',
    `attribute` varchar(64) NOT NULL DEFAULT '',
    `op` varchar(64) NOT NULL DEFAULT '',
    `value` varchar(64) NOT NULL DEFAULT ''
)''')
cur.execute("LOCK TABLES `radreply` WRITE;")
cur.execute("/*!40000 ALTER TABLE `radreply` DISABLE KEYS */;")
cur.execute("UNLOCK TABLES")

# Create Gtel Table radius_netelastic.radcheck
cur.execute('''CREATE TABLE `radcheck` (
    `username` varchar(64) NOT NULL DEFAULT '',
    `attribute` varchar(64) NOT NULL DEFAULT '',
    `op` varchar(64) NOT NULL DEFAULT '',
    `value` varchar(64) NOT NULL DEFAULT ''
)''')
cur.execute("LOCK TABLES `radcheck` WRITE;")
cur.execute("/*!40000 ALTER TABLE `radcheck` DISABLE KEYS */;")

cur.execute("UNLOCK TABLES")

# Create Table Logs
cur.execute('''CREATE TABLE `logs` (
    logId INT PRIMARY KEY,
    username VARCHAR(64) NOT NULL DEFAULT 'Gtel',
    reason VARCHAR(10),
    time TIMESTAMP
)''')
cur.execute("LOCK TABLES `logs` WRITE;")
cur.execute("/*!40000 ALTER TABLE `logs` DISABLE KEYS */;")

########################
# INSERT CONSTANT DATA #
########################

cur.execute("UNLOCK TABLES")

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


cur.execute(query_1)
cur.execute(query_2)
cur.execute(query_3)
cur.execute(query_4)

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

conn.commit()

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


#########
# Flask #
#########

@app.route("/index")
def index():
    return "Connected to database"


if __name__ == "__main__":
    app.run()


















