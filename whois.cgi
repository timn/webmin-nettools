#!/usr/bin/perl

#    Network Utilities Webmin Module - Whois
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

#     Created  : 02.09.1999


#######################
#    Configuration    #
#######################

require './nettools-lib.pl';
&init_command('whois');

eval "use Net::XWhois";
if ($@) {
 $whatfailed=$text{'whois_error'};
 &error($text{'whois_err_xwhois'});
}

if (!$config{'whois_servers'}) {
 @servers=("whois.networksolutions.com", "whois.internic.net", "whois.nic.de", "whois.ripe.net");
} else {
 my $tmpstr=$config{'whois_servers'};
 $tmpstr =~ s/\ //g;
 @servers=();
 foreach $_ (split(/\,/, $tmpstr) ) {
  push(@servers, $_);
 }
}

@formats=("INTERNIC", "INTERNIC_CONTACT", "RIPE", "RIPE_CH", "JAPAN");
$format_options="";
map {$format_options .= "<OPTION VALUE=\"$_\">$_\n" } @formats;

$server_options="";
map {$server_options .= "<OPTION VALUE=\"$_\">$_\n" } @servers;


&ReadParse;

if($ENV{'REQUEST_METHOD'} eq 'GET') { &PrintScreen }
else { &whoisit; &PrintScreen }

##################################################################
# Print Screen

sub PrintScreen {

&header($text{'whois_title'}, undef, undef, 1, 0, 0,
        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A><BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<BR><HR>\n";

$Errors="<H3><FONT COLOR=\"red\"><BR>";
foreach $tmperr (@error) {
 $Errors .= $tmperr . "<BR>";
}
$Errors .= '</FONT></H3>';

if ($in{'whois'} && !$critical_err) {

 print "<BR><BR>".&text('running', $text{'whois_title'});
 print "<HR SIZE=4 NOSHADE ALIGN=center>\n$Errors<PRE>\n";

 print $w->response();

 print "</PRE><HR SIZE=4 NOSHADE ALIGN=center>\n\n";

 if ($critical_err) {
  print "<BR><BR>";
  print &text('error_crit', $text{'whois_title'});
  print "<HR SIZE=4 NOSHADE ALIGN=center>\n$Errors";
  print "</PRE>\n<HR SIZE=4 NOSHADE ALIGN=center>\n\n";
 }
}



print <<EOM;
<HR>
<FORM METHOD="POST" ACTION="$progname">

<BR>
<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 $cb>
<TR><TD>

<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=0 WIDTH=100%>
<TR><TD $tb>

<TABLE BORDER=0 CELLSPACING=3 CELLPADDING=0 $tb WIDTH=100%>
<TR><TD><B>$text{'whois_title'} $text{'interface'}</I></B></TD></TR>
</TABLE>

</TD></TR>
<TR><TD>
<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=2 WIDTH=100%>
<TR>
<TD>$text{'whois_domain'}: <INPUT TYPE=text SIZE=20 NAME="domain" VALUE="$in{'domain'}"></TD>
<TD>$text{'whois_server'}: <SELECT NAME="server">$server_options</SELECT></TD>
<TD ALIGN=right><INPUT TYPE=submit NAME="whois" VALUE=" $text{'whois_button'} "></TD>
</TR>
</TABLE>
</TD></TR></TABLE>
</TD></TR></TABLE>

</FORM>


EOM

## Not really needed, because no result extraction by script
## <TD>Format: <SELECT NAME="format">$format_options</SELECT></TD>

&footer("index.cgi", $text{'whois_return'});
} # end of sub PrintScreen


sub whoisit
{

# Check host, or IP
if ($in{'domain'} eq '') {
        push(@error, "$text{'error_nohost'}\n");
	$critical_err = "true";
} elsif (length $in{'doamin'} >64) {
        push(@error, "$text{'error_longhostname'}\n");
	$critical_err = "true";
} elsif ($in{'domain'} =~ /[^\w\-\.]/) {
        push(@error, &text('error_badchar', $in{'host'})."\n");
	$critical_err = "true";
}

 $w = new Net::XWhois;

 $w->lookup( Domain => "$in{'domain'}",
             Server => "$in{'server'}",
             Format => "$in{'format'}",
             Retain => 1,
             Nocache => 1
           );

}


### End of whois.cgi ###