#!/usr/bin/perl

#    Network Utilities Webmin Module - Whois
#    Copyright (C) 1999-2001 by Tim Niemueller <tim@niemueller.de>
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

#     Created  : 02.09.1999


require './nettools-lib.pl';
&init_command('whois');

if (!$config{'whois_servers'}) {
 @servers=("whois.crsnic.net", "whois.networksolutions.com", "whois.corenic.net", "whois.internic.net", "whois.denic.de", "whois.ripe.net");
} else {
 my $tmpstr=$config{'whois_servers'};
 $tmpstr =~ s/\ //g;
 @servers=();
 foreach $_ (split(/\,/, $tmpstr) ) {
  push(@servers, $_);
 }
}

$server_options="";
map {$server_options .= "<OPTION VALUE=\"$_\">$_\n" } @servers;


&ReadParse();

my $execline = "";
if ($in{'domain'}) {
  $execline = CheckAll();
}

&header($text{'whois_title'}, undef, undef, 0, 0, 0,
        "<a href=\"about.cgi\">$text{'about'}</a>");

if ($execline) {

 print "<BR><BR>".&text('running', $text{'whois_title'});
 print "<HR SIZE=4 NOSHADE ALIGN=center>\n";

 print "<PRE>\n$execline\n";
   open (CHILD, "$execline |");
    while (<CHILD>) {
     print $_;
    }
   close (CHILD);
 print "</PRE>\n<HR SIZE=4 NOSHADE ALIGN=center>\n\n";
}

print <<EOM;
<br/>
<FORM METHOD="POST" ACTION="$progname">

<table border="0">
 <TR>
  <TD>$text{'whois_domain'}:</td><td><INPUT TYPE=text SIZE=20 NAME="domain" VALUE="$in{'domain'}"></TD>
 </tr>
 <tr>
  <TD>$text{'whois_server'}:</td><td><SELECT NAME="server">$server_options</SELECT></TD>
 </tr>
</table>

<br/>
<INPUT TYPE=submit NAME="whois" VALUE=" $text{'whois_button'} ">
</FORM>
<br/>

EOM

&footer("index.cgi", $text{'whois_return'});



sub CheckAll {

  my $whois_opt = "";
  my $execline = "";

  # Check host, or IP
  &terror('error_nohost') if (! $in{'domain'});
  &terror('error_longhostname') if (length($in{'domain'}) > 64);
  &terror('error_badchar', $in{'domain'}) if ($in{'domain'} !~ /^([a-z]*[A-Z]*[0-9]*[+.-]*)+$/);

  if ($in{'server'} ne '') {
    $whois_opt = "-h $in{'server'}";
  }

  $execline="$binary $whois_opt $in{'domain'}";

return $execline;
} # End Sub CheckAll




### End of whois.cgi ###
