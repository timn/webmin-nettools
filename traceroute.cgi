#!/usr/bin/perl

#    Network Utilities Webmin Module - Traceroute
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

#    Created  : 27.07.1999


require './nettools-lib.pl';
&init_command('traceroute');

&ReadParse();

$binary = $config{'ipv6'} ? "${binary}6" : $binary;
my $execline = "";
if ($in{'host'}) {
  $execline = &CheckAll();
}

&header($text{'traceroute_title'}, undef, "traceroute", 0, 0, 0,
        "<a href=\"about.cgi\">$text{'about'}</a>");

if ($execline) {

 print "<BR><BR>";
 if ($in{'trace'}) { print &text('running', $text{'traceroute_title'}) }

 print "<HR SIZE=4 NOSHADE ALIGN=center>\n$Errors";

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

$text{'hostname'}:
<INPUT TYPE=text NAME="host" SIZE=20 VALUE="$in{'host'}">

<br/><br/>
<table border="0" width="100%">
<tr><td valign="top">
EOM

print "<INPUT TYPE=checkbox NAME=\"verbosity\" VALUE=\"X\"";
if ($in{'verbosity'} eq "X") { print " checked" }
print "> $text{'traceroute_verbout'}<br/>";

print "<INPUT TYPE=checkbox NAME=\"numeric\" VALUE=\"X\"";
if ($in{'numeric'} eq "X") { print " checked" }
print "> $text{'traceroute_numout'}<br/>";

print "<INPUT TYPE=checkbox NAME=\"bypass\" VALUE=\"X\"";
if ($in{'bypass'} eq "X") { print " checked" }
print "> $text{'traceroute_bypass'}<br/>";

print "<INPUT TYPE=checkbox NAME=\"icmp\" VALUE=\"X\"";
if ($in{'icmp'} eq "X") { print " checked" }
print "> $text{'traceroute_icmp'}<br/>";

print "<INPUT TYPE=checkbox NAME=\"toggle\" VALUE=\"X\"";
if ($in{'toggle'} eq "X") { print " checked" }
print "> $text{'traceroute_toggle'}<br/>";

print "<INPUT TYPE=checkbox NAME=\"debug\" VALUE=\"X\"";
if ($in{'debug'} eq "X") { print " checked" }
print "> $text{'traceroute_debug'}<br/>";


print <<EOM;
</td><td valign="top">
<TABLE BORDER=0 CELLPADDING=0 CELLSPACING=2>
EOM

print "<TR><TD>$text{'traceroute_hops'}</TD>";
print "<TD ALIGN=left> <INPUT TYPE=text NAME=\"hops\" SIZE=5 VALUE=\"";
if ($in{'hops'}) {print "$in{'hops'}"} else {print "30"}

print "\"></TD></tr><tr><TD>$text{'traceroute_packlen'}</TD>";
print "<TD ALIGN=left> <INPUT TYPE=text NAME=\"length\" SIZE=5 VALUE=\"";
if ($in{'length'}) {print "$in{'length'}"} else {print "40"}

print "\"></TD></TR><TR><TD>$text{'traceroute_waittime'}</TD>";
print "<TD ALIGN=left> <INPUT TYPE=text NAME=\"wait\" SIZE=5 VALUE=\"";
if ($in{'wait'}) {print "$in{'wait'}"} else {print "5"}

print "\"></TD></tr><tr><TD>$text{'traceroute_ittl'}</TD>";
print "<TD ALIGN=left>";
if ($gconfig{'os_type'} eq "freebsd") { print $text{'traceroute_nofreebsd'} }
elsif ($gconfig{'os_type'} eq "debian-linux") { print $text{'traceroute_nodebian'} }
else {
 print " <INPUT TYPE=text NAME=\"inittime\" SIZE=5 VALUE=\"";
 if ($in{'inittime'}) {print "$in{'inittime'}"} else {print "1"}
 print "\">";
}
print "</TD></TR>";

print <<EOM;
<TR><TD>$text{'traceroute_interface'}:</TD>
<td><INPUT TYPE=text NAME=\"iface\" SIZE=5 VALUE=\"$in{'iface'}\"></TD></TR>
</TABLE>
</td></tr></table>

<br/>
<INPUT TYPE=submit NAME="trace" VALUE="  Trace It!  ">
</FORM>
<br/>
EOM

&footer("", $text{'traceroute_return'});





sub CheckAll {

  my $trace_opt="";

  # Check host, or IP
  &terror('error_nohost') if (! $in{'host'});
  &terror('error_longhostname') if (length($in{'host'}) > 64);
  &terror('error_badchar', $in{'host'}) if ($in{'host'} !~ /^([a-z]*[A-Z]*[0-9]*[+.-]*)+$/);

  if ($in{'hops'} ne '') {
    &terror('traceroute_err_hops') if (length($in{'hops'}) > 2);

    $trace_opt = "-m $in{'hops'}";
  }

  if ($in{'iface'} ne '') {
    &terror('traceroute_err_iface') if (length $in{'iface'} > 6);
    $trace_opt = "$trace_opt -i $in{'iface'}";
  }

  if ($in{'wait'} ne '') {
    &terror('traceroute_err_time') if (length $in{'wait'} > 2);
    $trace_opt = "$trace_opt -w $in{'wait'}";
  }

  if ($in{'inittime'} ne '') {
    &terror('traceroute_err_ittl') if (length $in{'inittime'} > 2);
    $trace_opt = "$trace_opt -f $in{'inittime'}";
  }

  if ($in{'verbosity'} eq 'X') { $trace_opt = "$trace_opt -v" }
  if ($in{'numeric'} eq 'X') { $trace_opt = "$trace_opt -n" }
  if ($in{'bypass'} eq 'X') { $trace_opt = "$trace_opt -r" }
  if ($in{'icmp'} eq 'X') { $trace_opt = "$trace_opt -I" }
  if ($in{'toggle'} eq 'X') { $trace_opt = "$trace_opt -x" }
  if ($in{'debug'} eq 'X') { $trace_opt = "$trace_opt -d" }


  if ($in{'length'} ne '') {
    &terror('traceroute_err_length') if (length($in{'length'}) > 3);

    $trace_opt = "$trace_opt $in{'host'} $in{'length'}";
  } else {
    $trace_opt = "$trace_opt $in{'host'}";
  }

return "$binary $trace_opt 2>&1";
} # End Sub CheckAll



### End of traceroute.cgi ###
