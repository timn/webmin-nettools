#!/usr/bin/perl

#    Network Utilities Webmin Module - Ping
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
&init_command('ping');

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

&header($text{'ping_title'}, undef, "ping", 1, 0, 0,
        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A><BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<BR><HR>\n";

if ($execline && !$critical_err) {

 print "<BR><BR>".&text('running', $text{'ping_title'});

 print "<HR SIZE=4 NOSHADE ALIGN=center>\n$Errors";

 print "<PRE>\n$execline\n";
   open (CHILD, "$execline |");
    while (<CHILD>) {
     print $_;
    }
   close (CHILD);
 print "</PRE>\n<HR SIZE=4 NOSHADE ALIGN=center>\n\n";

} elsif ($critical_err) {
 print "<BR><BR>"&text('error_crit', $text{'ping_title'});

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
<TD><B>$text{'ping_title'} $text{'interface'}</B></TD>
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
print "> $text{'ping_verbout'}</TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"numeric\" VALUE=\"X\"";
if ($in{'numeric'} eq "X") { print " checked" }
print "> $text{'ping_numout'}</TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"bypass\" VALUE=\"X\"";
if ($in{'bypass'} eq "X") { print " checked" }
print "> $text{'ping_bypass'}</TD>";

print <<EOM;
</TR></TABLE>
</TD></TR>
<TR><TD><TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=2 WIDTH=100%>
EOM

print "<TR><TD>$text{'ping_numpack'}</TD>";
print "</TD><TD ALIGN=left> <INPUT TYPE=text NAME=\"count\" SIZE=5 VALUE=\"";
if ($in{'count'}) {print "$in{'count'}"} else {print "5"}

print "\"></TD><TD>$text{'ping_packsize'}</TD>";
print "<TD ALIGN=left> <INPUT TYPE=text NAME=\"size\" SIZE=8 VALUE=\"";
if ($in{'size'}) {print "$in{'size'}"} else {print "56"}
print "\"></TD><TD ROWSPAN=2 ALIGN=center VALIGN=center><INPUT TYPE=submit NAME=\"ping\" VALUE=\"   $text{'lib_ping'}   \"></TD></TR>";

print "<TR><TD>$text{'ping_packsec'}</TD>";
print "<TD ALIGN=left> <INPUT TYPE=text NAME=\"wait\" SIZE=5 VALUE=\"";
if ($in{'wait'}) {print "$in{'wait'}"} else {print "1"}

print "\"></TD><TD>$text{'ping_pattern'}</TD>";

if ($gconfig{'os_type'} eq "solaris") {
 print "<TD ALIGN=left> $text{'ping_nasolaris'}</TD></TR>";
} else {
 print "<TD ALIGN=left> <INPUT TYPE=text NAME=\"padbytes\" SIZE=8 VALUE=\"$in{'padbytes'}\"></TD></TR>";
}

print <<EOM;
</TABLE>
</TD></TR></TABLE>
</TD></TR></TABLE>
<!-- </TD></TR></TABLE> -->
</TD></TR>

</TABLE>
</FORM>

EOM



&footer("index.cgi", $text{'ping_return'});

} # end of sub PrintScreen

sub CheckAll {

@error=();

# Check host, or IP
if ($in{'host'} eq '') {
        push(@error, "$text{'error_nohost'}\n");
	$critical_err = "true";
} elsif (length $in{'host'} >64) {
        push(@error, "$text{'error_longhostname'}\n");
	$critical_err = "true";
} elsif ($in{'host'} =~ /[^\w\-\.]/) {
        push(@error, &text('error_badchar', $in{'host'})."\n");
	$critical_err = "true";
}

if ($in{'ping'}) {

#Check for Counts
if ($in{'count'} ne '') {

 if (length $in{'count'} > 2) {
  push(@error, "$text{'ping_err_tmpack'}\n");
  if ($gconfig{'os_type'} eq "solaris") { $ping_cnt="5" } else { $ping_opt = "-c 5" }

 }
 else {
    if ($in{'count'} eq "0") {
        push(@error, "$text{'ping_err_zeropack'}\n");
        if ($gconfig{'os_type'} eq "solaris") { $ping_cnt="5" } else { $ping_opt = "-c 5" }
    }
    else
    {
     if ($gconfig{'os_type'} eq "solaris") {
       $ping_cnt = "$in{'count'}";
     }
     else {
       $ping_opt = "-c $in{'count'}";
     }
    }
 }
}
else
{
 push(@error, "$text{'ping_err_nothing'}\n");
 if ($gconfig{'os_type'} eq "solaris") {
     $ping_cnt = "5"
 }
 else {
    $ping_opt = "-c 5"
 }
}

#Check for Size
if ($in{'size'} ne '') {
 if (length $in{'size'} > 4) {
        push(@error, $text{'ping_err_bigpack'});
 } else {
        if ($gconfig{'os_type'} eq "solaris") {
           $ping_opt = "$ping_opt -s";
           $ping_size = "$in{'size'}";
        }
        else {
           $ping_opt = "$ping_opt -s $in{'size'}"
        }
 }
}

if ($in{'wait'} ne '') {
 if (length $in{'wait'} > 2) {
        push(@error, $text{'ping_err_time'});
 } else {
        if ($gconfig{'os_type'} eq "solaris") {
            $ping_opt = "$ping_opt -I $in{'wait'}"
        }
        else {
           $ping_opt = "$ping_opt -i $in{'wait'}"
        }
 }
}

if ($in{'padbytes'} ne '') {
 if (length $in{'padbytes'} > 32) {
        push(@$error, $text{'ping_err_bigpatt'});
 } else {
        $ping_opt = "$ping_opt -p $in{'padbytes'}"
 }
}

if ($in{'verbosity'} eq 'X') { $ping_opt = "$ping_opt -v" }
if ($in{'numeric'} eq 'X') { $ping_opt = "$ping_opt -n" }
if ($in{'bypass'} eq 'X') { $ping_opt = "$ping_opt -r" }

if ($gconfig{'os_type'} eq "solaris") {
    $execline ="$binary $ping_opt $in{'host'} $ping_size $ping_cnt 2>&1";
}
else {
    $execline ="$binary $ping_opt $in{'host'} 2>&1";
}


} # End IF PING
} # End Sub CheckAll

### End of ping.cgi ###