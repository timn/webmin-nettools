#!/usr/bin/perl

#    Network Utilities Webmin Module
#    Copyright (C) 1999-2000 by Tim Niemueller
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


if (!$allow) {
  $whatfailed=$text{'index_error'};
 
  for (my $i=0; $i <= $programcount-1; $i++) {

   if ($programs[$i]) {
    if (! -e $programs[$i]) {
     &error(&text('index_err_fnex', $programs[$i], $cl))
    } elsif(! -x $programs[$i]) {
     &error(&text('index_err_fne', $programs[$i], $cl))
    }
   } else {
    if (! has_command($programnames[$i])) {
     &error(&text('index_err_dfnf', $programnames[$i], $cl))
    }
   }  
  }

 } # End if allow eq no



&header($text{'index_title'}, undef, "intro", 1, 1, undef,
        "<a href=\"about.cgi\">About</a>");

my @images = ("images/icon.ping.gif", "images/icon.traceroute.gif", "images/icon.lookup.gif",
              "images/icon.nmap.gif", "images/icon.ipsc.gif", "images/icon.whois.gif",
              "images/icon.dig.gif");
my @texts  = ($text{'index_ping'}, $text{'index_traceroute'}, $text{'index_lookup'},
              $text{'index_nmap'}, $text{'index_ipsc'}, $text{'index_whois'}, $text{'index_dig'});
my @links  = ("ping.cgi", "traceroute.cgi", "lookup.cgi", "nmap.cgi", "ipsc.cgi", "whois.cgi", "dig.cgi");

print "<BR><HR>\n";
&icons_table(\@links, \@texts, \@images, 4);
print "<HR>\n";
print "<TABLE BORDER=0 CELLPADDING=0 CELLSPACING=0 WIDTH=100%>";
print "<TR><TD ALIGN=right><FONT FACE=\"Arial,Helvetica\" COLOR=#505050>";
print "[ Network Utilities $version ]</FONT></TD></TR></TABLE>\n";


print <<EOM;
<FORM METHOD="POST" ACTION="dispatch.cgi">

<BR>
<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 $cb WIDTH=100%>
<TR><TD>

<TABLE BORDER=0 $tb CELLPADDING=0 CELLSPACING=0 WIDTH=100%>
<TR><TD $tb>

<TABLE BORDER=0 CELLSPACING=2 CELLPADDING=2 $tb WIDTH=100%>
<TR>
<TD ALIGN=center WIDTH=20%><B>$text{'hostname'}</B></TD>
EOM

for (my $i=0; $i <= $programcount-1; $i++) {
 print "<TD ALIGN=center WIDTH=$tdwidth%><B>\u$programnames[$i]</B></TD>"
}

print <<EOM;
</TR></TABLE>

</TD></TR>
<TR $cb>
<TD> <TABLE BORDER=0 $cb CELLPADDING=2 CELLSPACING=0 WIDTH=100%>
<TR>
<TD ALIGN=center WIDTH=20%><INPUT TYPE=text NAME="host" SIZE=20 VALUE="$in{'host'}"></TD>
EOM

for (my $i=0; $i <= $programcount-1; $i++) {

if ($access{$programnames[$i]})
{
 if ($programs[$i]) {
  if (-x $programs[$i]) {
   print "<TD ALIGN=center WIDTH=$tdwidth%><INPUT TYPE=submit NAME=\"$programnames[$i]\" VALUE=\"$programbuttons[$i]\"></TD>";
  } else { print "<TD ALIGN=center WIDTH=$tdwidth%>N/A</TD>" }
 } else {
  if (has_command($programnames[$i])) {
   print "<TD ALIGN=center WIDTH=$tdwidth%><INPUT TYPE=submit NAME=\"$programnames[$i]\" VALUE=\"$programbuttons[$i]\"></TD>";
  } else { print "<TD ALIGN=center WIDTH=$tdwidth%>$text{'index_na'}</TD>" }
 }
}
else ## User has no access
{
 print "<TD ALIGN=center WIDTH=$tdwidth%>".&text('index_deny_user', $user)."</TD>";
}

} ## end of for

print <<EOM;
</TR></TABLE>
</TD></TR></TABLE>
</TD></TR></TABLE>
</FORM>

<br/><br/>
EOM

&footer("/", $text{'index_return'});

### End of index.cgi ###
