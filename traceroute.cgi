#!/usr/bin/perl

#    Network Utilities Webmin Module - Traceroute
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

#    Created  : 27.07.1999


require './nettools-lib.pl';
&init_command('traceroute');

&ReadParse();

if($ENV{'REQUEST_METHOD'} eq 'GET') { &PrintScreen }
else { &CheckAll; &PrintScreen }

##################################################################

sub PrintScreen {

$Errors="<H3><FONT COLOR=\"red\"><BR>";
foreach $tmperr (@error) {
 $Errors .= $tmperr . "<BR>";
}
$Errors .= '</FONT></H3>';

&header($text{'traceroute_title'}, undef, "traceroute", 1, 0, 0,
        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A><BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<BR><HR>\n";

if ($execline && !$critical_err) {

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

} elsif ($critical_err) {
 print "<BR><BR>";
 if ($in{'trace'}) { print &text('error_crit', $text{'traceroute_title'}) }

 print "<HR SIZE=4 NOSHADE ALIGN=center>\n$Errors";
 print "</PRE>\n<HR SIZE=4 NOSHADE ALIGN=center>\n\n";
}

print <<EOM;

<FORM METHOD="POST" ACTION="$progname">

<BR>
<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 $cb WIDTH=100%>
<TR><TD>

<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=0 WIDTH=100%>
<TR><TD $tb>

<TABLE BORDER=0 CELLSPACING=3 CELLPADDING=0 $tb WIDTH=100%>
<TR>
<TD><B>$text{'traceroute_title'} $text{'interface'}</B></TD>
</TR></TABLE>

</TD></TR>
<TR><TD>
<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=2 WIDTH=100%>

<TR><TD>
<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=2 WIDTH=100%>
<TR>
<TD>$text{'hostname'}</TD>
<TD><INPUT TYPE=text NAME="host" SIZE=20 VALUE="$in{'host'}"></TD>
EOM
print "<TD><INPUT TYPE=checkbox NAME=\"verbosity\" VALUE=\"X\"";
if ($in{'verbosity'} eq "X") { print " checked" }
print "> $text{'traceroute_verbout'}</TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"numeric\" VALUE=\"X\"";
if ($in{'numeric'} eq "X") { print " checked" }
print "> $text{'traceroute_numout'}</TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"bypass\" VALUE=\"X\"";
if ($in{'bypass'} eq "X") { print " checked" }
print "> $text{'traceroute_bypass'}</TD>";

print <<EOM;
</TR></TABLE>
</TD></TR>
<TR><TD><TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=2 WIDTH=100%>
EOM

print "<TD><INPUT TYPE=checkbox NAME=\"icmp\" VALUE=\"X\"";
if ($in{'icmp'} eq "X") { print " checked" }
print "> $text{'traceroute_icmp'}</TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"toggle\" VALUE=\"X\"";
if ($in{'toggle'} eq "X") { print " checked" }
print "> $text{'traceroute_toggle'}</TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"debug\" VALUE=\"X\"";
if ($in{'debug'} eq "X") { print " checked" }
print "> $text{'traceroute_debug'}</TD> <TD> </TD>";

print "<TD ROWSPAN=4 ALIGN=center VALIGN=center><INPUT TYPE=submit NAME=\"trace\" VALUE=\"  Trace It!  \"></TD></TR>";

print "<TR><TD>$text{'traceroute_hops'}</TD>";
print "<TD ALIGN=left> <INPUT TYPE=text NAME=\"hops\" SIZE=5 VALUE=\"";
if ($in{'hops'}) {print "$in{'hops'}"} else {print "30"}

print "\"></TD><TD>$text{'traceroute_packlen'}</TD>";
print "<TD ALIGN=left> <INPUT TYPE=text NAME=\"length\" SIZE=5 VALUE=\"";
if ($in{'length'}) {print "$in{'length'}"} else {print "40"}

print "\"></TD></TR><TR><TD>$text{'traceroute_waittime'}</TD>";
print "<TD ALIGN=left> <INPUT TYPE=text NAME=\"wait\" SIZE=5 VALUE=\"";
if ($in{'wait'}) {print "$in{'wait'}"} else {print "5"}

print "\"></TD><TD>$text{'traceroute_ittl'}</TD>";
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
<TR><TD><TD>$text{'traceroute_interface'}:</TD>
<TD ALIGN=left COLSPAN=3><INPUT TYPE=text NAME=\"iface\" SIZE=5 VALUE=\"$in{'iface'}\"></TD></TR>
</TABLE>
</TD></TR></TABLE>
</TD></TR></TABLE>
<!-- </TD></TR></TABLE> -->
</TD></TR>

</TABLE>
</FORM>

EOM

&footer("index.cgi", $text{'traceroute_return'});

} # end of sub PrintScreen

sub CheckAll {

# Check host, or IP
if ($in{'host'} eq '') {
        push(@error, "$text{'error_nohost'}\n");
	$critical_err = 1;
} elsif (length $in{'host'} >64) {
        push(@error, "$text{'error_longhostname'}\n");
	$critical_err = "1";
} elsif ($in{'host'} =~ /[^\w\-\.]/) {
        push(@error, &text('error_badchar', $in{'host'})."\n");
	$critical_err = "1";
}


if ($in{'trace'}) {
if ($in{'hops'} ne '') {
 if (length $in{'hops'} > 2) {
        push(@error, $text{'traceroute_err_hops'});
 } else {
        $trace_opt = "-m $in{'hops'}";
 }
}

if ($in{'iface'} ne '') {
 if (length $in{'iface'} > 6) {
        push(@error, $text{'traceroute_err_iface'});
 } else {
        $trace_opt = "$trace_opt -i $in{'iface'}";
 }
}

if ($in{'wait'} ne '') {
 if (length $in{'wait'} > 2) {
        push(@error, $text{'traceroute_err_time'});
 } else {
        $trace_opt = "$trace_opt -w $in{'wait'}";
 }
}

if ($in{'inittime'} ne '') {
 if (length $in{'inittime'} > 2) {
        push(@error, $text{'traceroute_err_ittl'});
 } else {
        $trace_opt = "$trace_opt -f $in{'inittime'}";
 }
}

if ($in{'verbosity'} eq 'X') { $trace_opt = "$trace_opt -v" }
if ($in{'numeric'} eq 'X') { $trace_opt = "$trace_opt -n" }
if ($in{'bypass'} eq 'X') { $trace_opt = "$trace_opt -r" }
if ($in{'icmp'} eq 'X') { $trace_opt = "$trace_opt -I" }
if ($in{'toggle'} eq 'X') { $trace_opt = "$trace_opt -x" }
if ($in{'debug'} eq 'X') { $trace_opt = "$trace_opt -d" }


if ($in{'length'} ne '') {
 if (length $in{'length'} > 3) {
        push(@error, $text{'traceroute_err_length'});
 } else {
        $trace_opt = "$trace_opt $in{'host'} $in{'length'}";
 }
}


$execline = "$binary $trace_opt 2>&1";

}


} # End Sub CheckAll

### End of traceroute.cgi ###