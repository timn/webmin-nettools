#!/usr/bin/perl

#    Network Utilities Webmin Module
#    Copyright (C) 1999-2003 by Tim Niemueller
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    Created  : 22.07.1998


require './nettools-lib.pl';
&ReadParse();

if ($in{'ping'}) {
  redirect("ping.cgi?host=$in{'host'}");
} else {
  if ($in{'traceroute'}) {
    redirect("traceroute.cgi?host=$in{'host'}");
  } else {
    if ($in{'nslookup'}) {
      redirect("lookup.cgi?host=$in{'host'}");
    } else {
      if ($in{'nmap'}) {
        redirect("nmap.cgi?host=$in{'host'}");
      } else {
        if ($in{'dig'}) {
          redirect("dig.cgi?host=$in{'host'}");
        } else {
          terror("dispatch_invserv");
        }
      }
    }
  }
}
## END.

