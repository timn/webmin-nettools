#!/usr/bin/perl
#
#    Network Utilities Webmin Module - Dig
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

#    Created: 17.10.1999

require './nettools-lib.pl';
&init_command('dig');

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

my $execline="";
if ($in{'host'}) {
  $execline = CheckAll();
}

$Errors="<H3><FONT COLOR=\"red\"><BR>";
foreach $tmperr (@error) {
 $Errors .= $tmperr . "<BR>";
}
$Errors .= '</FONT></H3>';

&header($text{'dig_title'}, undef, undef, 1, 0, 0,
        "<a href=\"about.cgi\">$text{'about'}</a>");

if ($execline && !$critical_err) {

 print "<BR><BR>".&text('running', $text{'dig_title'});
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
  print &text('error_crit', $text{'dig_name'});
  print "<HR SIZE=4 NOSHADE ALIGN=center>\n$Errors";
  print "</PRE>\n<HR SIZE=4 NOSHADE ALIGN=center>\n\n";
 }

print <<EOM;

<br/>
<FORM METHOD="POST" ACTION="$progname">

<TABLE BORDER=0 CELLPADDING=0 CELLSPACING=2 WIDTH=100%>
<TR><TD>
<TABLE BORDER=0 CELLPADDING=0 CELLSPACING=2 WIDTH=100%>
<TR>
<TD>$text{'hostname'}:</td><td><INPUT TYPE=text NAME="host" SIZE=20 VALUE="$in{'host'}"></TD>
<TD>$text{'dig_type'}:</td><td><SELECT NAME="type">$options</SELECT></TD></tr>
<TR><TD>$text{'dig_nameserver'}:</td><td><INPUT TYPE=radio NAME="nsdefault" VALUE="1"
EOM

if ($in{'nsdefault'}) {print " checked"}

print "> $text{'default'} <INPUT TYPE=radio NAME=\"nsdefault\" VALUE=\"0\"";
if (!$in{'nsdefault'}) {print " checked"}
print "> <INPUT TYPE=text NAME=\"nameserver\" SIZE=20 VALUE=\"$in{'nameserver'}\"></TD>";

print "<TD>$text{'dig_dottednot'}</td><td><INPUT TYPE=checkbox NAME=\"dotted\" VALUE=\"1\"";
if ($in{'dotted'}) { print " checked" }
print "></TD></TR>";


print <<EOM;
</TD></TR></TABLE>
</TD></TR></TABLE>
<br/>
<INPUT TYPE=submit NAME="dig" VALUE="   $text{'lib_dig'}   ">
</FORM>
<br/>

EOM

&footer("", $text{'dig_return'});















sub CheckAll {

@error=();

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

if (!$in{'nsdefault'}) { $dig_opt="@$in{'nameserver'}" }

if ($in{'dotted'}) {
 if (!&check_ipaddress($in{'host'})) {
   push(@error, "$text{'dig_err_dotted'}\n");
   $critical_err = 1;
 } else {
  $dig_opt .= " -x $in{'host'}";
 }
} else {
 $dig_opt .= " $in{'host'}";
}

$dig_opt .= " $in{'type'}";

$execline = "$binary $dig_opt 2>&1";

} # End Sub CheckAll



### End of dig.cgi ###
