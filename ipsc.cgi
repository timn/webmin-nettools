#!/usr/bin/perl

#    Network Utilities Webmin Module - IP Subnet Calculator
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


require './ipsc-lib.pl';
&init_command('ipsc');

if($ENV{'REQUEST_METHOD'} eq 'GET') { &PrintScreen }
else { &Calculate; &PrintScreen }

##################################################################

sub PrintScreen {

my $bits_options ="";
for (my $i = 0; $i <= 24; $i++) {
       my $selected="";
       if ($in{'bits'} eq "$i") { $selected=" SELECTED" }
       $bits_options .= "<OPTION VALUE=\"$i\"$selected>$i\n";
}

my $class_options="";
for (my $i = 0; $i <= 2; $i++) {
       my $selected="";
       if ($infstruct[0] eq "$i") { $selected= " SELECTED"; $test=" test3" }
       $class_options .= "<OPTION VALUE=\"$i\"$selected>$classes[$i] ($classrange[$i])\n";
}

&header($text{'ipsc_title'}, undef, "ipsc", 1, 0, 0,
        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A><BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<BR><HR>\n";

print <<EOM;

<FORM METHOD="POST" ACTION="$progname">

<BR>
<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 $cb WIDTH=100%>
<TR><TD>

<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=0 WIDTH=100%>
<TR><TD $tb>

<TABLE BORDER=0 CELLSPACING=3 CELLPADDING=0 $tb WIDTH=100%>
<TR><TD><B>$text{'ipsc_class_n_bits'}</B></TD></TR>
</TABLE>

</TD></TR>
<TR><TD>
<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=2 WIDTH=100%>
<TR>
<TD>$text{'ipsc_class'}: <SELECT NAME="class">$class_options</SELECT></TD>
<TD>$text{'ipsc_subnetbits'}: <SELECT NAME="bits">$bits_options</SELECT></TD>
<TD ALIGN=right><INPUT TYPE=submit NAME="csnclassbits" VALUE="$text{'ipsc_calc'}"></TD>
</TR>
$csnclassbitsresult
</TABLE>
</TD></TR></TABLE>
</TD></TR></TABLE>


<BR>
<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 $cb WIDTH=100%>
<TR><TD>

<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=0 WIDTH=100%>
<TR><TD $tb>

<TABLE BORDER=0 CELLSPACING=3 CELLPADDING=0 $tb WIDTH=100%>
<TR><TD><B>$text{'ipsc_bynumber'}</B></TD></TR>
</TABLE>

</TD></TR>
<TR><TD>
<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=2 WIDTH=100%>
<TR>
<TD COLSPAN=2>$text{'ipsc_number'}: <INPUT TYPE=text NAME="numhosts" SIZE=8 VALUE="$in{'numhosts'}"></TD>
<TD ALIGN=right><INPUT TYPE=submit NAME="csnnumhosts" VALUE="$text{'ipsc_calc'}"></TD>
</TR>
$csnnumhostsresult
</TABLE>
</TD></TR></TABLE>
</TD></TR></TABLE>


$keepclassbits
$keepnumhosts
</FORM>


EOM

&footer("", $text{'ipsc_return'});
} # end of sub PrintScreen


### End of ipsc.cgi ###