#!/usr/bin/perl

#    Network Utilities Webmin Module - Nmap
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

#    Created  : 31.08.1999


require './nettools-lib.pl';
&init_command('nmap');


%NmapTypes = (
    -sT         => $text{'nmap_tcpconnect'},
    -sS         => $text{'nmap_syn'},
    -sF         => $text{'nmap_stealth'},
    -sX         => $text{'nmap_xmastree'},
    -sN         => $text{'nmap_null'},
    -sP         => $text{'nmap_ping'},
    -sU         => $text{'nmap_udp'}
    );

&ReadParse();

$options = "";
for (keys %NmapTypes) {
        $options .= "<OPTION VALUE=\"$_\"";
        if ($in{'scantype'}) {
         $options .= $in{'scantype'} eq $_ ? " SELECTED" : "";
        } else {
         $options .= $_ eq "-sT" ? " SELECTED" : "";
        }
        $options .= ">$NmapTypes{$_}\n";
}


&CheckAll() if ($ENV{'REQUEST_METHOD'} ne 'GET');

$Errors="<H3><FONT COLOR=\"red\">\n";
foreach $tmperr (@error) {
 $Errors .= $tmperr . "<BR>";
}
$Errors .= '</FONT></H3>';

&header($text{'nmap_title'}, undef, undef, 0, 0, 0,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<BR><HR>\n";

if ($execline && !$critical_err) {

 print "<BR><BR>";
 if ($in{'nmap'}) { print &text('running', $text{'nmap_title'}) }

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
 if ($in{'nmap'}) { print &text('error_crit', "Nmap") }

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
<TD><B>$text{'nmap_title'} $text{'interface'}</B></TD>
</TR></TABLE>

</TD></TR>
<TR><TD>
<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=2 WIDTH=100%>

<TR><TD>
<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=2 WIDTH=100%>
<TR>
<TD>$text{'hostname'}:</TD>
<TD><INPUT TYPE=text NAME="host" SIZE=20 VALUE="$in{'host'}"></TD>
<TD>$text{'nmap_scantype'}:</TD>
<TD><SELECT NAME="scantype">$options</SELECT></TD>
</TR></TABLE>
</TD></TR>
<TR><TD><TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=2 WIDTH=100%>
EOM

print "<TR><TD><INPUT TYPE=checkbox NAME=\"verbosity\" VALUE=\"1\"";
if ($in{'verbosity'}) { print " checked" }
print "> $text{'nmap_verbout'}</TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"p0\" VALUE=\"1\"";
if ($in{'p0'}) { print " checked" }
print "> $text{'nmap_noping'}</TD>";

print "<TD ROWSPAN=7><INPUT TYPE=submit VALUE=\"   $text{'lib_nmap'}   \" NAME=\"nmap\"></TD></TR>";

print "<TR><TD><INPUT TYPE=checkbox NAME=\"pt\" VALUE=\"1\"";
if ($in{'pt'}) { print " checked" }
print "> $text{'nmap_ackport'}: <INPUT TPYE=text NAME=\"ptport\" VALUE=\"$in{'ptport'}\" SIZE=5> </TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"pi\" VALUE=\"1\"";
if ($in{'pi'}) { print " checked" }
print "> $text{'nmap_ping'}</TD></TR>";

print "<TR><TD><INPUT TYPE=checkbox NAME=\"pb\" VALUE=\"1\"";
if ($in{'pb'}) { print " checked" }
print "> $text{'nmap_ackping_parallel'}</TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"o\" VALUE=\"1\"";
if ($in{'o'}) { print " checked" }
print "> $text{'nmap_osdet'}</TD></TR>";

print "<TR><TD><INPUT TYPE=checkbox NAME=\"i\" VALUE=\"1\"";
if ($in{'i'}) { print " checked" }
print "> $text{'nmap_ident'}</TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"f\" VALUE=\"1\"";
if ($in{'f'}) { print " checked" }
print "> $text{'nmap_tinyfrag'}</TD></TR>";

print "<TR><TD><INPUT TYPE=checkbox NAME=\"p\" VALUE=\"1\"";
if ($in{'p'}) { print " checked" }
print "> $text{'nmap_scanports'}: <INPUT TPYE=text NAME=\"ports\" VALUE=\"$in{'ports'}\" SIZE=30> </TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"fast\" VALUE=\"1\"";
if ($in{'fast'}) { print " checked" }
print "> $text{'nmap_fastscan'}</TD></TR>";

print "<TR><TD><INPUT TYPE=checkbox NAME=\"d\" VALUE=\"1\"";
if ($in{'d'}) { print " checked" }
print "> $text{'nmap_decoys'}: <INPUT TYPE=text NAME=\"decoys\" SIZE=30></TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"e\" VALUE=\"1\"";
if ($in{'e'}) { print " checked" }
print "> $text{'nmap_interface'}: <INPUT TYPE=text NAME=\"iface\" SIZE=5 VALUE=\"$in{'iface'}\"></TD></TR>";

print "<TR><TD><INPUT TYPE=checkbox NAME=\"g\" VALUE=\"1\"";
if ($in{'g'}) { print " checked" }
print "> $text{'nmap_sport'}: <INPUT TYPE=text NAME=\"sport\" SIZE=5 VALUE=\"$in{'sport'}\"></TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"m\" VALUE=\"1\"";
if ($in{'m'}) { print " checked" }
print "> $text{'nmap_maxsock'}: <INPUT TYPE=text NAME=\"sockets\" SIZE=5 VALUE=\"$in{'sockets'}\"></TD></TR>";

print <<EOM;
</TABLE>
</TD></TR></TABLE>
</TD></TR></TABLE>
</TD></TR>

</TABLE>
</FORM>

EOM



&footer("index.cgi", $text{'nmap_return'});









sub CheckAll {

@error="";

# Check host, or IP
if ($in{'host'} eq '') {
        push(@error, "$text{'error_nohost'}\n");
	$critical_err = 1;
} elsif (length $in{'host'} >64) {
        push(@error, "$text{'error_longhostname'}\n");
	$critical_err = 1;
} elsif ($in{'host'} =~ /[^\w\-\.]/) {
        push(@error, &text('error_badchar', $in{'host'})."\n");
	$critical_err = 1;
}

if ($in{'nmap'}) {

$nmap_opt="$in{'scantype'}";

if ($in{'verbosity'}) { $nmap_opt .= " -v" }
if ($in{'p0'}) { $nmap_opt .= " -P0" }

if ($in{'pt'}) {
 $in{'ptport'} =~ s/\ //g;
 if (!$in{'ptport'}) {
      push(@error, $text{'nmap_err_ack'});
 }
 elsif ($in{'ptport'} < 0) {
      push(@error, $text{'nmap_err_lowport'});
 }
 elsif ($in{'ptport'} > 65535) {
      push(@error, $text{'nmap_err_highport'});
 }
 else {
  $nmap_opt .= " -PT$in{'ptports'}";
 }
}

if ($in{'pi'}) { $nmap_opt .= " -PI" }
if ($in{'pb'}) { $nmap_opt .= " -PB" }
if ($in{'o'}) { $nmap_opt .= " -O" }
if ($in{'i'}) { $nmap_opt .= " -I" }
if ($in{'f'}) { $nmap_opt .= " -f" }

if ($in{'p'}) {
 $in{'ports'} =~ s/\ //g;
 if (!$in{'ports'}) {
      push(@error, $text{'nmap_err_port'});
 }
 elsif ($in{'ports'} =~ m/[a-z]*[A-Z]*/g) {
      push(@error, $text{'nmap_err_ports'});
 }
 elsif ($in{'ports'} < 0) {
      push(@error, $text{'nmap_err_lowport'});
 }
 elsif ($in{'ports'} > 65535) {
      push(@error, $text{'nmap_err_highport'});
 }
 else {
   $nmap_opt .= " -p $in{'ports'}";
 }
}

if ($in{'fast'}) { $nmap_opt .= " -F" }

if ($in{'d'}) {
 $in{'decoys'} =~ s/\ //g;
 if (!$in{'decoys'}) {
      push(@error, $text{'nmap_err_decoys'});
 }
 else {
   $nmap_opt .= " -D $in{'decoys'}";
 }
}


if ($in{'e'}) {
 $in{'iface'} =~ s/\ //g;
 if (!$in{'iface'}) {
      push(@error, $text{'nmap_err_iface'});
 }
 else {
   $nmap_opt .= " -e $in{'iface'}";
 }
}

if ($in{'g'}) {
 $in{'sport'} =~ s/\ //g;
 if (!$in{'sport'}) {
      push(@error, $text{'nmap_err_sport'});
 }
 else {
   $nmap_opt .= " -g $in{'sport'}";
 }
}

if ($in{'m'}) {
 $in{'sockets'} =~ s/\ //g;
 if (!$in{'sockets'}) {
      push(@error, $text{'nmap_err_maxsock'});
 }
 elsif ($in{'sockets'} < 0) {
      push(@error, $text{'nmap_err_lowsock'});
 }
 elsif ($in{'sockets'} > 16) {
      push(@error, $text{'nmap_err_bigsock'});
 }
 else {
   $nmap_opt .= " -M $in{'sockets'}";
 }
}


$execline ="$binary $nmap_opt $in{'host'} 2>&1";

} # End IF Nmap
} # End Sub CheckAll

### End of nmap.cgi ###