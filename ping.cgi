#!/usr/bin/perl

#    Network Utilities Webmin Module - Ping
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

#    Created  : 27.07.1999


require './nettools-lib.pl';
&init_command('ping');

&ReadParse();

$binary = $config{'ipv6'} ? "${binary}6" : $binary;
my $execline = &CheckAll() if ($ENV{'REQUEST_METHOD'} ne 'GET');


&header($text{'ping_title'}, undef, "ping", 0, 0, 0,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<BR><HR>\n";

if ($execline) {

 print "<BR><BR>".&text('running', $text{'ping_title'});

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


&footer("", $text{'ping_return'});










sub CheckAll {

  my $ping_opt = "";
  my $ping_cnt = "";
  my $ping_size= "";
  my $execline = "";

  # Check host, or IP
  &terror('error_nohost') if (! $in{'host'});
  &terror('error_longhostname') if (length($in{'host'}) > 64);
  &terror('error_badchar', $in{'host'}) if ($in{'host'} !~ /^([a-z]*[A-Z]*[0-9]*[+.-]*)+$/);

  &terror('ping_err_zeropack') if (! $in{'count'});
  &terror('ping_err_tmpack') if (length($in{'count'}) > 2);

  if ($gconfig{'os_type'} eq "solaris") { $ping_cnt=$in{'count'} }
  else { $ping_opt = "-c $in{'count'}" }


  #Check for Size
  if ($in{'size'} ne '') {
    &terror('ping_err_bigpack') if (length $in{'size'} > 4);

    if ($gconfig{'os_type'} eq "solaris") {
      $ping_opt = "$ping_opt -s";
      $ping_size = "$in{'size'}";
    } else {
      $ping_opt = "$ping_opt -s $in{'size'}"
    }
  }
  
  if ($in{'wait'} ne '') {
    &terror('ping_err_time') if (length($in{'wait'}) > 2);
  
    if ($gconfig{'os_type'} eq "solaris") {
      $ping_opt = "$ping_opt -I $in{'wait'}"
    } else {
      $ping_opt = "$ping_opt -i $in{'wait'}"
    }
  }

  if ($in{'padbytes'} ne '') {
    &terror('ping_err_bigpatt') if (length($in{'padbytes'}) > 32);
    $ping_opt = "$ping_opt -p $in{'padbytes'}"

  }

  if ($in{'verbosity'} eq 'X') { $ping_opt = "$ping_opt -v" }
  if ($in{'numeric'} eq 'X') { $ping_opt = "$ping_opt -n" }
  if ($in{'bypass'} eq 'X') { $ping_opt = "$ping_opt -r" }

  if ($gconfig{'os_type'} eq "solaris") {
    $execline ="$binary $ping_opt $in{'host'} $ping_size $ping_cnt 2>&1";
  } else {
    $execline ="$binary $ping_opt $in{'host'} 2>&1";
  }

return $execline;
} # End Sub CheckAll



### End of ping.cgi ###