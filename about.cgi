#!/usr/bin/perl

#    Webmin Module Generic About
#    Copyright (C) 2003 by Tim Niemueller
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
#
#    Created : 12.02.2003
#

# Changes:
# 12.02.2003 - Created about.cgi

#############################################################################

do '../web-lib.pl';
$|=1;
&init_config();

my %modconf;
&read_file("module.conf", \%modconf);

# real output
&header($modconf{'TITLE'}, "images/$modconf{'ICON'}", undef, 1, undef, undef,
        "<a href=\"about.cgi\">About</a>");



print <<EOM;
<br/>

<table border="0">
 <tr><td>Module:</td><td>$modconf{'MODNAME'}</td></tr>
 <tr><td>Version:</td><td>$modconf{'VERSION'}</td></tr>
 <tr><td>Author:</td><td>$modconf{'AUTHOR'}</td></tr>
 <tr><td>eMail:</td><td><a href="mailto:$modconf{'EMAIL'}?Subject=$modconf{'MODNAME'} $modconf{'VERSION'}">$modconf{'EMAIL'}</a></td></tr>
 <tr><td>Website:</td><td><a href="$modconf{'WEBSITE'}">$modconf{'WEBSITE'}</a></td></tr>
 <tr><td>Copyright:</td><td>$modconf{'CRIGHT'}</td></tr>
 <tr><td>License:</td><td><a href="LICENSE">$modconf{'LICENSE'}</a></td></tr>
</table>
<br/><br/>
EOM

&footer("", "module index");

