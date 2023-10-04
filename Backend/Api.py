#python -m pip install flask
#pip3 install mariadb
#pip install mysql-connector-python

import json
import mysql.connector as mariadb;

## Create mysql connector and define cursor
## Replace Database, LocalHost,Port, once we get a DB on the VMs
mariadb_connection = mariadb.connect(user = 'r00t', password = 'ArchFiber23', database = 'ArchFiber', host = 'Localhost', port = '')
##Return  Values in a Dictionary Statement
create_cursor = mariadb_connection.cursor() # Dictonary = True
######################
#CREATE DB AND TABLES
######################

create_cursor.execute("CREATE DATABASE ArchFiber")
#Show DB
create_cursor.execute("SHOW DATABASES")

for x in create_cursor:
    print(x)
    
#Create Tables
create_cursor.execute("CREATE TABLE Users (COLUMN String(1) COLUMN Int)")
#Six Strings For Each IP Tag: We Can Convert Them into Integers if need be
#Mac Address, IPV4, IPV6, Type (Static or Dynamic), Status, Tags
create_cursor.execute("CREATE TABLE IPS (COLUMN String(1), COLUMN String(1), COLUMN String(1), COLUMN String(1), COLUMN String(1), COLUMN String(1))")
