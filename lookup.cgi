#!/usr/bin/perl

#    Network Utilities Webmin Module - Lookup
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
&init_command('nslookup');


%LookupOpt = (
    a           => $text{'lookup_opt_a'},
    cname       => $text{'lookup_opt_cname'},
    any         => $text{'lookup_opt_any'},
    mx          => $text{'lookup_opt_mx'},
    ns          => $text{'lookup_opt_ns'},
    soa         => $text{'lookup_opt_soa'},
    hinfo       => $text{'lookup_opt_hinfo'},
    minfo       => $text{'lookup_opt_minfo'},
    ptr         => $text{'lookup_opt_ptr'},
    txt         => $text{'lookup_opt_txt'},
    uinfo       => $text{'lookup_opt_uinfo'},
    wks         => $text{'lookup_opt_wks'}
    );

for (sort keys %LookupOpt) {
        $options .= "<OPTION VALUE=\"$_\">$LookupOpt{$_}\n";
}


&ReadParse();

my $execline = &CheckAll() if($ENV{'REQUEST_METHOD'} ne 'GET');


&header($text{'lookup_title'}, undef, "lookup", 0, 0, 0,
        "Written by<BR>Tim Niemueller<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<BR><HR>\n";

if ($execline) {

 print "<BR><BR>".&text('running', $tet{'lookup_title'});
 print "<HR SIZE=4 NOSHADE ALIGN=center>\n$Errors";

 print "<PRE>\n$execline\n";
   open (CHILD, "$execline |");
    while (<CHILD>) {
     print $_;
    }
   close (CHILD);
 print "</PRE>\n<HR SIZE=4 NOSHADE ALIGN=center>\n\n";
}
 if ($critical_err) {
  print "<BR><BR>";
  print &text('error_crit', $text{'lookup_title'});
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
<TD><B>$text{'lookup_title'} $text{'interface'}</B></TD>
</TR></TABLE>

</TD></TR>
<TR><TD>
<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=2 WIDTH=100%>

<TR><TD>
<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=2 WIDTH=100%>
<TR>
<TD>$text{'hostname'} <INPUT TYPE=text NAME="host" SIZE=20 VALUE="$in{'host'}"></TD>
<TD>Typ: <SELECT NAME="type">$options</SELECT></TD>
<TD ROWSPAN=2 ALIGN=center VALIGN=center><INPUT TYPE=submit NAME=\"lookup\" VALUE=\"  $text{'lib_lookup'}  \"></TD></TR>
<TR><TD>$text{'lookup_nameserver'}: <INPUT TYPE=radio NAME="nsdefault" VALUE="1"
EOM

if ($in{'nsdefault'}) {print " checked"}

print "> $text{'lookup_default'} <INPUT TYPE=radio NAME=\"nsdefault\" VALUE=\"0\"";
if (!$in{'nsdefault'}) {print " checked"}
print "> <INPUT TYPE=text NAME=\"nameserver\" SIZE=20 VALUE=\"$in{'nameserver'}\"></TD>";

print "<TD>$text{'lookup_timeout'}";
print " <INPUT TYPE=text NAME=\"timeout\" SIZE=5 VALUE=\"";
if ($in{'timeout'}) {print "$in{'timeout'}"} else {print "10"}
print "\"></TD>";


print <<EOM;
</TR></TABLE>
</TD></TR>
</TABLE>
</TD></TR></TABLE>
</TD></TR>

</TABLE>
</FORM>

EOM

&footer("index.cgi", $text{'lookup_return'});









sub CheckAll {

  my $execline="";
  my $lookup_opt="";

  # Check host, or IP
  &terror('error_nohost') if ($in{'host'} eq '');
  &terror('error_longhostname') if (length($in{'host'}) > 64);
  &terror('error_badchar', $in{'host'}) if ($in{'host'} !~ /^([a-z]*[A-Z]*[0-9]*[+.-]*)+$/);

  $lookup_opt = "-query=$in{'type'}";

  if ($in{'timeout'} ne '') {
    &terror('lookup_inv_timeout') if (length($in{'timeout'}) > 2);

    $lookup_opt = "$lookup_opt -timeout=$in{'timeout'}";
  }

  if (!$in{'nsdefault'}) { $execline = "$binary $lookup_opt $in{'host'} $in{'nameserver'} 2>&1" }
  else { $execline = "$binary $lookup_opt $in{'host'} 2>&1" }

return $execline;
} # End Sub CheckAll



### End of lookup.cgi ###