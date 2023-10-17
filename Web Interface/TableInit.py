# python -m pip install flask
# pip3 install pymysql
# pip install mysql-connector-python
# mysql -u root -p : Login for consol
from flask import Flask
import pymysql
import sys

#Swapped to pymysql for import consistancy 

######################
# CONNECT TO MARIADB #
######################

# Attempt to connect with current credentials
# currently set to localhost
# Maybe for website purposes have username and password be the same as website login
# This could be easy access for credentials of who can manipulate the DB

app = Flask(__name__)
try:
    conn = pymysql.connect(
        host='10.10.9.43',
        user='root',
        password='',
        database='customer_data'
    )
except pymysql.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
cur = conn.cursor()

###################
# CREATE DATABASE #
###################

#Drop Database for testing purposes 
cur.execute("DROP DATABASE IF EXISTS ArchFiber")
cur.execute("DROP DATABASE IF EXISTS customer_data")
#Create and Select Database, Create Table
cur.execute("CREATE DATABASE customer_data; ")
cur.execute("USE customer_data;")

################
# CREATE TABLE #
################

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


# Table Creations
cur.execute("DROP TABLE IF EXISTS `radacct`;")
# Preserving the value of character_set_client in the variable @saved_cs_client
# in a way that is compatible with MySQL 4.01.01 and later.
cur.execute("/*!40101 SET @saved_cs_client     = @@character_set_client */;")
# Sets the MySQL session variable character_set_client to use the UTF-8 character set.
cur.execute("/*!40101 SET character_set_client = utf8 */;")

#Create Table radacct. Check Raddact.png for an easy display of information

#####################
# IMPORTANT NUMBERS #
#####################
# nasportid (Port ID),
# acctstarttime (for uptime calculation)
# acctupdatetime (Date/Time in device table)
# acctstoptime (Time for stop entry)
# callingstationid (MAC Address)
# acctterminatecause (Termination Reason)
# framedipaddress (IPv4 Address)
# framedipv6address (IPv6 Address)


#Create Table radacct. Check Raddact.png for an easy display of information

#Note To Self: See at somepoint if I can make this take up mutliple lines instead of years of scrolling
cur.execute("CREATE TABLE `radacct` (`radacctid` bigint(21) NOT NULL AUTO_INCREMENT, `acctsessionid` varchar(64) NOT NULL DEFAULT '', `acctuniqueid` varchar(32) NOT NULL DEFAULT '', `username` varchar(64) NOT NULL DEFAULT '', `realm` varchar(64) DEFAULT '', `nasipaddress` varchar(15) NOT NULL DEFAULT '', `nasportid` varchar(32) DEFAULT NULL, `nasporttype` varchar(32) DEFAULT NULL, `acctstarttime` datetime DEFAULT NULL, `acctupdatetime` datetime DEFAULT NULL, `acctstoptime` datetime DEFAULT NULL, `acctinterval` int(12) DEFAULT NULL, `acctsessiontime` int(12) unsigned DEFAULT NULL, `acctauthentic` varchar(32) DEFAULT NULL, `connectinfo_start` varchar(128) DEFAULT NULL, `connectinfo_stop` varchar(128) DEFAULT NULL, `acctinputoctets` bigint(20) DEFAULT NULL, `acctoutputoctets` bigint(20) DEFAULT NULL, `calledstationid` varchar(50) NOT NULL DEFAULT '', `callingstationid` varchar(50) NOT NULL DEFAULT '', `acctterminatecause` varchar(32) NOT NULL DEFAULT '', `servicetype` varchar(32) DEFAULT NULL, `framedprotocol` varchar(32) DEFAULT NULL, `framedipaddress` varchar(15) NOT NULL DEFAULT '', `framedipv6address` varchar(45) NOT NULL DEFAULT '', `framedipv6prefix` varchar(45) NOT NULL DEFAULT '', `framedinterfaceid` varchar(44) NOT NULL DEFAULT '', `delegatedipv6prefix` varchar(45) NOT NULL DEFAULT '', `class` varchar(64) DEFAULT NULL, PRIMARY KEY (`radacctid`), UNIQUE KEY `acctuniqueid` (`acctuniqueid`), KEY `username` (`username`), KEY `framedipaddress` (`framedipaddress`), KEY `framedipv6address` (`framedipv6address`), KEY `framedipv6prefix` (`framedipv6prefix`), KEY `framedinterfaceid` (`framedinterfaceid`), KEY `delegatedipv6prefix` (`delegatedipv6prefix`), KEY `acctsessionid` (`acctsessionid`), KEY `acctsessiontime` (`acctsessiontime`), KEY `acctstarttime` (`acctstarttime`), KEY `acctinterval` (`acctinterval`), KEY `acctstoptime` (`acctstoptime`), KEY `nasipaddress` (`nasipaddress`), KEY `class` (`class`)) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;")
cur.execute("LOCK TABLES `radacct` WRITE;")
cur.execute("/*!40000 ALTER TABLE `radacct` DISABLE KEYS */;")


########################
# INSERT CONSTANT DATA #
########################

#Note To Self: See at somepoint if I can make this take up mutliple lines instead of years of scrolling, 
cur.execute("INSERT INTO `radacct` VALUES (1,'000000000000-0021000000-0006000000-003E6F2565','43920d1a27c58bc035fe0f9e75d17bb5','=25=7BUser-Name=7D=25','','10.245.10.15','301:1011','41','2023-10-10 17:35:36','2023-10-10 17:35:36','2023-10-10 18:05:41',NULL,1805,'','','',635593,51066,'','CC-66-18-5C-3F-10','NAS-Request','','','204.11.161.15','','2607:2040:300:80b::/64','','',NULL),(2,'000000000000-0023000000-0008000000-00A2712565','fecfad9f6e05df35123095c7b2ff3d74','=25=7BUser-Name=7D=25','','10.245.10.15','301:1011','41','2023-10-10 17:45:48','2023-10-10 17:45:48','2023-10-10 18:16:48',NULL,1860,'','','',1372705,584436,'','CC-66-18-5C-3F-D0','NAS-Error','','','204.11.161.15','','2607:2040:300:80c::/64','','',NULL),(3,'000000000000-0026000000-0012000000-0048812565','c3bbe10ad601b2873d2aab4d049c44ce','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 17:52:34','2023-10-10 18:16:15','2023-10-10 18:17:14',195,1480,'','','',29792518,538507873,'','CC-66-18-EA-E4-20','NAS-Error','','','204.11.161.15','','2607:2040:300:140e::/64','','',NULL),(4,'000000000000-0027000000-0013000000-0093902565','8bf25ed587bd21c52b8a3a2732818603','=25=7BUser-Name=7D=25','','10.245.10.15','301:1011','41','2023-10-10 17:57:49','2023-10-10 17:57:51','2023-10-10 18:00:00',2,131,'','','',648807,39983899,'','CC-66-18-EE-B8-90','User-Request','','','204.11.161.15','','2607:2040:300:80e::/64','','',NULL),(5,'000000000000-0028000000-0014000000-006E912565','5b58390ed184947bbfeef4a46ad4bd15','=25=7BUser-Name=7D=25','','10.245.10.15','301:1011','41','2023-10-10 18:01:19','2023-10-10 18:01:20','2023-10-10 18:17:48',1,989,'','','',718631,341907,'','CC-66-18-EE-B8-90','NAS-Error','','','204.11.161.15','','2607:2040:300:140f::/64','','',NULL),(6,'000000000000-002A000000-0016000000-0097962565','a8c98f1486326b69992dba1c909d13b2','=25=7BUser-Name=7D=25','','10.245.10.15','301:1011','41','2023-10-10 18:23:19','2023-10-11 13:23:19',NULL,3600,68400,'','','',14837148286,55983282547,'','CC-66-18-5C-3F-D0','','','','204.11.161.15','','2607:2040:300:810::/64','','',NULL),(7,'000000000000-0029000000-0015000000-0091962565','227820edd9f09b61565baf9b9616e472','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 18:23:23','2023-10-10 18:23:25','2023-10-10 18:26:02',2,159,'','','',148214,85721,'','CC-66-18-EE-B8-90','NAS-Request','','','204.11.161.15','','2607:2040:300:80f::/64','','',NULL),(8,'000000000000-002B000000-0017000000-0098962565','96a79329dfa1a3183350d27ac7eb0f77','=25=7BUser-Name=7D=25','','10.245.10.15','301:1011','41','2023-10-10 18:23:40','2023-10-11 13:23:40',NULL,3600,68400,'','','',8925668142,8120440260,'','CC-66-18-EA-E4-20','','','','204.11.161.15','','2607:2040:300:1410::/64','','',NULL),(9,'000000000000-002C000000-0019000000-001F982565','651f0497eb1454e4c8554a3fa0fcf9aa','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 18:30:03','2023-10-10 18:30:03',NULL,0,NULL,'','','',348,1344,'','CC-66-18-EE-B8-90','','','','204.11.161.15','','','','',NULL),(10,'000000000000-002C000000-0026000000-001F982565','cf54e50ba4861b04c618a117a34eeee6','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 18:34:11','2023-10-10 18:34:11',NULL,NULL,NULL,'','','',757,13434,'','CC-66-18-EE-B8-90','','','','204.11.161.15','','2607:2040:300:1411::/64','','',NULL),(11,'000000000000-002D000000-0034000000-0095A02565','62caa3159c8cc14975b32e36c34a4be5','=25=7BUser-Name=7D=25','','10.245.10.15','301:1011','41','2023-10-10 19:06:30','2023-10-10 19:06:30','2023-10-10 19:10:21',NULL,231,'','','',2797662,3786688,'','A0-CE-C8-A5-74-97','NAS-Request','','','204.11.161.15','','','','',NULL),(12,'000000000000-002C000000-0033000000-001F982565','92a4a72690b5e665389e4e940bfe2191','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 19:01:46','2023-10-10 19:10:13','2023-10-10 19:10:13',NULL,507,'','','',36175,73950,'','CC-66-18-EE-B8-90','NAS-Request','','','204.11.161.15','','2607:2040:300:1411::/64','','',NULL),(13,'000000000000-002E000000-0035000000-00C7A12565','07e816d6e3b86294bb30fe255018f3bb','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 19:11:04','2023-10-10 19:11:04',NULL,NULL,0,'','','',0,0,'','A0-CE-C8-A5-74-97','','','','','','2607:2040:300:811::/64','','',NULL),(14,'000000000000-002E000000-0038000000-00C7A12565','a013658568bebba287159a87c8680c13','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 19:11:19','2023-10-10 19:11:19',NULL,NULL,NULL,'','','',2192,3799,'','A0-CE-C8-A5-74-97','','','','204.11.161.15','','2607:2040:300:811::/64','','',NULL),(15,'000000000000-002E000000-004D000000-00C7A12565','aa1116591f2bcaec54551b565a8fa0e8','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 19:19:57','2023-10-10 19:20:02','2023-10-10 19:20:02',NULL,5,'','','',580588,15343,'','A0-CE-C8-A5-74-97','NAS-Request','','','204.11.161.15','','2607:2040:300:811::/64','','',NULL),(16,'000000000000-002F000000-004F000000-00F7A32565','f8c4a6e354df221fad7b32c17ef2adfd','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 19:20:45','2023-10-10 19:20:45',NULL,0,NULL,'','','',348,672,'','A0-CE-C8-A5-74-97','','','','204.11.161.15','','','','',NULL),(17,'000000000000-002F000000-0050000000-00F7A32565','b5c5c97c16c859bd9b799e7493fc83c9','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 19:20:48','2023-10-10 19:21:41',NULL,NULL,53,'','','',410,1008,'','A0-CE-C8-A5-74-97','','','','204.11.161.15','','2607:2040:300:1412::/64','','',NULL),(18,'000000000000-002F000000-0056000000-00F7A32565','63ecd0265442568c1eab9d1114af670c','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 19:22:39','2023-10-10 19:23:04','2023-10-10 19:23:04',NULL,25,'','','',1785785,2042882,'','A0-CE-C8-A5-74-97','NAS-Request','','','204.11.161.15','','2607:2040:300:1412::/64','','',NULL),(19,'000000000000-007C000000-00A3000000-00B2A72565','2ad9ed072123f12eee64ab593062565b','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 19:36:38','2023-10-10 19:36:38',NULL,NULL,0,'','','',0,0,'','A0-CE-C8-A5-74-97','','','','','','2607:2040:300:812::/64','','',NULL),(20,'000000000000-007C000000-00A4000000-00B2A72565','a86c9293bf61bf42833723e6ab0b4c3e','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 19:37:14','2023-10-10 19:37:14',NULL,NULL,NULL,'','','',1972,3372,'','A0-CE-C8-A5-74-97','','','','204.11.161.15','','2607:2040:300:812::/64','','',NULL),(21,'000000000000-007C000000-00C3000000-00B2A72565','749fb43a658b2b1548aea520f5f95e8e','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 19:48:56','2023-10-10 19:52:50','2023-10-10 19:52:50',NULL,234,'','','',17668253,56074348,'','A0-CE-C8-A5-74-97','NAS-Request','','','204.11.161.15','','2607:2040:300:812::/64','','',NULL),(22,'000000000000-0089000000-00D1000000-004FAC2565','2ec3e4b6ceb1e45ebe4721dceaf732c6','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 19:56:02','2023-10-10 19:56:02',NULL,0,NULL,'','','',342,1008,'','A0-CE-C8-A5-74-97','','','','204.11.161.15','','','','',NULL),(23,'000000000000-0089000000-00D7000000-004FAC2565','4a483f6e4d2f5eafc5775de043bdb3ef','=25=7BUser-Name=7D','','10.245.10.15','301:1011','41','2023-10-10 19:59:06','2023-10-10 20:14:06','2023-10-10 20:14:06',NULL,900,'','','',2177749,1282446,'','A0-CE-C8-A5-74-97','NAS-Request','','','204.11.161.15','','','','',NULL),(24,'000000000000-008A000000-00D8000000-0022CA2565','f86dc38d85d02e020e9673a5de5a46d3','=25=7BUser-Name=7D=25','','10.245.10.15','301:1011','41','2023-10-10 22:03:23','2023-10-11 12:03:23','2023-10-11 12:35:47',3600,52344,'','','',4029677,305820,'','CC-66-18-EE-B8-90','NAS-Request','','','204.11.161.15','','2607:2040:300:1413::/64','','',NULL),(25,'000000000000-008B000000-00D9000000-008CA52665','cc990bdb66e060f61fe51c46b1915e53','=25=7BUser-Name=7D=25','','10.245.10.15','301:1011','41','2023-10-11 13:39:35','2023-10-11 13:39:36',NULL,1,1,'','','',410,1008,'','CC-66-18-EE-B8-90','','','','204.11.161.15','','2607:2040:300:813::/64','','',NULL);")
conn.commit()
# Enabling keys. Enabling keys means rebuilding or activating indexes on the table, which can improve query performance.
cur.execute("/*!40000 ALTER TABLE `radacct` ENABLE KEYS */;")
cur.execute("UNLOCK TABLES;")

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
