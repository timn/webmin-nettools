#!/usr/bin/perl

#    Network Utilities Webmin Module
#    Copyright (C) 1999 by Tim Niemueller
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
#
# Changes
# =========================================================================================
#
# 10.02.1998  - Habe bessere Fehlerroutine eingebaut. Fuehrt nun Programm
#               bei schwereren Fehlern nicht mehr aus!
#             - Fehler in Fehlermeldung :) behoben
#             - Fehlermeldungen abgeaendert
# 22.07.1999  - New Version of Tools-Port, made it a Webmin Module
#             - Using English instead of German for international use
# 27.07.1999  - Added option for allowing use of other services if one fails
# 01.08.1999  - Because I added "Find self"-Option in configure I had to
#               change CheckBinaries() and some parts of PrintScreen()
# 02.08.1999  - Changed the $execline for ping and traceroute
# 31.08.1999  - Solved the "Access denied" error!
#             - Changes to Ping execline for Solaris (Thanx to Robert Setterlund
#               for the information about Solaris)
#             - New icon for IP Subnet Calculator
#             - Now it is possible to configure options to be used for quick versions
#               in configuration module. HOST is a wildcard for the hostname.
#             - Better handling of programs, not written for every program but with a
#               for-loop checking for programs etc.
#             - Changed the handling of errormessages, it's now an array, so all
#               encountered errors may be reported, not only one.
#             - Much code clean up for better reading, all is in for-loops now
# 01.09.1999  - Changed some problem with the init_config on webmin systems < 0.73
# 28.09.1999  - Fixed Bug, init_command needed binary also if some progs
#               don't need a special binary (as ipsc and whois)
# 17.10.1999  - Checked Webmin 0.74 Compliance, all OK
#             - Added Dig interface
#             - Added GPL header to all files
# 15.02.2000  - Long time, since I worked on this module. I will now fix some smaller
#               bugs and make it ready for 0.76+
#
# =========================================================================================


#######################
#    Configuration    #
#######################

require './nettools-lib.pl';

&ReadParse;

if($ENV{'REQUEST_METHOD'} eq 'GET') { &CheckBinaries }
else { &CheckAll; &PrintScreen }

##################################################################
# Print Screen

sub CheckBinaries {
 if (!$allow)
 {
 
  $whatfailed=$text{'index_error'};
 
  for (my $i=0; $i <= $programcount-1; $i++)
  {

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

 &PrintScreen;
}

sub PrintScreen {

$Errors="<H3><FONT COLOR=\"red\">\n";
foreach $tmperr (@error) {
 $Errors .= $tmperr . "<BR>";
}
$Errors .= '</FONT></H3>';

&header($text{'index_title'}, undef, "intro", 1, 1, undef,
        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A><BR><A HREF=http://www.niemueller.de>Home://page</A>");

my @images = ("images/icon.ping.gif", "images/icon.traceroute.gif", "images/icon.lookup.gif",
              "images/icon.nmap.gif", "images/icon.ipsc.gif", "images/icon.whois.gif",
              "images/icon.dig.gif");
my @texts  = ($text{'index_ping'}, $text{'index_traceroute'}, $text{'index_lookup'},
              $text{'index_nmap'}, $text{'index_ipsc'}, $text{'index_whois'}, $text{'index_dig'});
my @links  = ("ping.cgi", "traceroute.cgi", "lookup.cgi", "nmap.cgi", "ipsc.cgi", "whois.cgi", "dig.cgi");

print "<BR><HR>\n";
&icons_table(\@links, \@texts, \@images, 4);
print "<HR>\n";

if ($execline && !$critical_err) {

 print "<BR><BR>";

for (my $i=0; $i <= $programcount-1; $i++)
{
 if ($in{"$programnames[$i]"}) {
  print &text('index_running', $programnames[$i]);
 }
}

 print "<HR SIZE=4 NOSHADE ALIGN=center>\n$Errors";

 print "<PRE>\n$execline\n";
   open (CHILD, "$execline |");
    while (<CHILD>) {
     print $_;
    }
   close (CHILD);
 print "</PRE>\n<HR SIZE=4 NOSHADE ALIGN=center>\n\n";

} elsif ($critical_err) {

 foreach $c ("ping", "traceroute", "nslookup", "nmap", "dig") {
  if ($in{$c}) { print $text{"index_err_crit_$c"} }
 }

 print "<HR SIZE=4 NOSHADE ALIGN=center>\n$Errors";
 print "</PRE>\n<HR SIZE=4 NOSHADE ALIGN=center>\n\n";
}

print <<EOM;

<FORM METHOD="POST" ACTION="$progname">

<BR>
<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 $cb WIDTH=100%>
<TR><TD>

<TABLE BORDER=0 $tb CELLPADDING=0 CELLSPACING=0 WIDTH=100%>
<TR><TD $tb>

<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=2 $tb WIDTH=100%>
<TR>
<TD ALIGN=center WIDTH=20%><B>Hostname</B></TD>
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

EOM

&footer("/", $text{'index_return'});

} # end of sub PrintScreen

sub CheckAll {

# Check host, or IP
if ($in{'host'} eq '') {
        push(@error, "$text{'error_nohost'}\n");
	$critical_err = 1;
} elsif (length $in{'host'} >64) {
        push(@error, "$text{'error_longhostname'}\n");
} elsif ($in{'host'} =~ /[^\w\-\.]/) {
        push(@error, &text('error_badchar', $in{'host'})."\n");
}

for (my $i=0; $i <= $programcount-1; $i++)
{
 if ($in{"$programnames[$i]"})
 {
  if ($programs[$i]) { $binary=$programs[$i] } else { $binary=$programnames[$i] }

  if ($config{"$programnames[$i]_opt"}) {
   $options = $config{"$programnames[$i]_opt"};
  } else {
   $options = $standopt[$i];
  }

  $options =~ s/HOST/$in{'host'}/;
  $execline = "$binary $options";
 }
} ## End For

} # End Sub CheckAll

