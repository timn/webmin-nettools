
#    Network Utilities Webmin Module - acl_security.pl
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

require './nettools-lib.pl';

# acl_security_form(&options)
# Output HTML for editing security options for the apache module
sub acl_security_form
{

print "<TR><TD COLSPAN=4 ALIGN=left><B>User has Access to the following commands:</B></TD></TR>\n";
print "<TR><TD><INPUT TYPE=checkbox NAME=\"ipsc\" VALUE=\"1\"", ($_[0]->{'ipsc'}) ? " CHECKED" : "", "> IP Subnet Calculator </TD><TR>\n";
print "<TR><TD><INPUT TYPE=checkbox NAME=\"whois\" VALUE=\"1\"", ($_[0]->{'whois'}) ? " CHECKED" : "", "> Whois Interface </TD><TR>\n";

for (my $i=0; $i <= $programcount-1; $i++) {
 print "<TR><TD><INPUT TYPE=checkbox NAME=\"$programnames[$i]\" VALUE=\"1\"", ($_[0]->{"$programnames[$i]"}) ? " CHECKED" : "", "> \u$programnames[$i] Interface</TD><TR>\n";

} ## end of for


}

# acl_security_save(&options)
# Parse the form for security options for the apache module
sub acl_security_save
{

 for (my $i=0; $i <= $programcount-1; $i++) {
  $_[0]->{"$programnames[$i]"} = $in{"$programnames[$i]"};
 } ## end of for

 $_[0]->{'ipsc'} = $in{'ipsc'};
 $_[0]->{'whois'} = $in{'whois'};

}

### END.