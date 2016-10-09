#!/usr/bin/env python


#import sqlite3
import MySQLdb

#The size for the notebook tabs
panel_size = (1024, 700)


application_dictionary = {0:'netTunes', 20:'FTP', 21:'FTP', 22:'SSH', 23:'Telnet', 25:'SMTP', 53:'DNS', 80:'HTTP',
                            110:'POP3', 143:'IMAP', 443:'Secure HTTP', 1187:'Alias Service', 51413:'Transmission bittorent',
                            587:'Google SMTP', 1474:'Telefinder'}
protocols_dictionary = {1:'ICMP', 4:'IP', 6:'TCP', 17:'UDP', 88:'EIGRP'}

KB = 1024
MB = 1048576.00
GB = 1073741824.00

#database = "/temp/flows.sqlite"
conn = MySQLdb.connect (host = "localhost",
    user = "tony",
    passwd = "murewa",
    db = "netflow")

def getRowset(sql):
    #conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(sql)
    rowset = cursor.fetchall()
    cursor.close()
    conn.close()
    return rowset

def getFormatedVolume(volume):
    print "volume = %d" % volume
    if (volume>GB):
        val = "%.1f" % (volume/GB)
        return str(val) + " GB"
    elif (volume > MB):
        val = "%.1f" % (volume/MB)
        return str(val) + " MB"
    elif volume > KB:
        val = "%.1f" % (volume/KB)
        return str(val) + " KB"
    else:
        return str(volume) + " Bytes"



def getApplicationName(port):
    if port in application_dictionary:
        return application_dictionary.__getitem__(port)
    else:
        return str(port)

def getProtocolName(protocol):
    if protocol in protocols_dictionary:
        return protocols_dictionary.__getitem__(protocol)
    else:
        return str(protocol)


