#!/usr/bin/env python3
# coding=utf-8
# author: @netmanchris
# -*- coding: utf-8 -*-
"""
This module contains functions for authenticating to the ServerTech


"""



from pysnmp.hlapi import *
from pyservertech.auth import *

def get_socket_status(myauth, socket_num):
    socket_status = {}
    socket_status['number'] = socket_num
    g = getCmd(SnmpEngine(),
               CommunityData(myauth.rostring),
               UdpTransportTarget((myauth.ipaddr, myauth.port)),
               ContextData(),
               ObjectType(ObjectIdentity('.1.3.6.1.4.1.1718.3.2.3.1.3.1.1.' + str(socket_num))))
    socket_status['description']=(next(g)[3][0].prettyPrint().rsplit(sep="=")[1])
    g = getCmd(SnmpEngine(),
               CommunityData(myauth.rostring),
               UdpTransportTarget((myauth.ipaddr, myauth.port)),
               ContextData(),
               ObjectType(ObjectIdentity('.1.3.6.1.4.1.1718.3.2.3.1.2.1.1.' + str(socket_num))))
    socket_status['name'] = (next(g)[3][0].prettyPrint().rsplit(sep="=")[1])
    g = getCmd(SnmpEngine(),
               CommunityData(myauth.rostring),
               UdpTransportTarget((myauth.ipaddr, myauth.port)),
               ContextData(),
               ObjectType(ObjectIdentity('.1.3.6.1.4.1.1718.3.2.3.1.5.1.1.' + str(socket_num))))
    socket_status['power_state'] =(next(g)[3][0].prettyPrint().rsplit(sep="=")[1])
    return socket_status

def get_bulk_socket_status(myauth, num_of_sockets):
    socket_list = []
    for i in range(1,num_of_sockets+1):
        socket = get_socket_status(myauth, i)
        socket_list.append(socket)
    return socket_list

def power_on(myauth, socket_num):
    g = setCmd(SnmpEngine(),
           CommunityData(myauth.rwstring),
           UdpTransportTarget((myauth.ipaddr, myauth.port)),
           ContextData(),
           ObjectType(ObjectIdentity('.1.3.6.1.4.1.1718.3.2.3.1.11.1.1.'+str(socket_num)),
                      Integer('1')))
    next(g)


def power_off(myauth, socket_num):
    """
    Function takes STAuth object and socket_num which corresponds to the SNMP index for the specific
    power socket and sends a SNMP SET request with the integer "2" which corresponds to the OFF state
    :param myauth: instance pyservertech.auth STAuth object
    :param socket_num: integer representing the SNMP index value for the desired power socket
    :return: None
    """
    g = setCmd(SnmpEngine(),
           CommunityData(myauth.rwstring),
           UdpTransportTarget((myauth.ipaddr, myauth.port)),
           ContextData(),
           ObjectType(ObjectIdentity('.1.3.6.1.4.1.1718.3.2.3.1.11.1.1.'+ str(socket_num)),
                      Integer('2')))
    next(g)



