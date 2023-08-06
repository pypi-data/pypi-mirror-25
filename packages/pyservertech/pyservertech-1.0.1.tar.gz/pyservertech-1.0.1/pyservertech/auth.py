#!/usr/bin/env python3
# coding=utf-8
# author: @netmanchris
# -*- coding: utf-8 -*-
"""
This module contains functions for authenticating to the ServerTech


"""

class STAuth:
    def __init__(self, ipaddr, rostring, rwstring, Port="161"):
        self.ipaddr = ipaddr
        self.rostring = rostring
        self.rwstring = rwstring
        self.port = Port