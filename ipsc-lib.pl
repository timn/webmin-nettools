
################################################################################
#                                                                              #
#              ipsc-lib.pl Library of IP Subnet Calculator subs                #
#                    Tim Niemueller <tim@niemueller.de>                        #
#                         http://www.niemueller.de                             #
#                                                                              #
################################################################################
#              Copyright (C) 1998-1999 by Tim Niemueller (lGPL)                #
################################################################################

#    Network Utilities Webmin Module - ipsc-lib.pl
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

#    Created  : 02.08.1999

require './nettools-lib.pl';

&ReadParse();

# I misuse this lists as constants
@classes=("A", "B", "C");
@classmask=("255.0.0.0", "255.255.0.0", "255.255.255.0");
@hexclmask=("FF000000", "FFFF0000", "FFFFFF00");
@classrange=("1.x.x.x.-126.x.x.x", "128.x.x.x-191.x.x.x", "192.x.x.x-223.x.x.x");
@classbits=(8, 16, 24);

# I use this list as something like a struct, known from C
# For field description see set_infstruct() at the bottom
@infstruct="";
if ($in{'class'} ne "") { @infstruct=&set_infstruct($in{'class'}) } else { @infstruct=&set_infstruct(2) }



# calculate()
# Validates input which method has been chosen and calls the appropriate
# sub.
sub Calculate
{
 if ($in{'csnclassbits'})
 {
  &calc_by_class_bits;
  if ($config{'keepresults'} && $in{'keepnumhosts'})
  {
  &calc_by_num_hosts;
  }
 }
 elsif ($in{'csnnumhosts'})
 {
  &calc_by_num_hosts;
  if ($config{'keepresults'} && $in{'keepclassbits'})
  {
   &calc_by_class_bits;
  }
 } # End of ELSIF Calc by Num of Hosts
} # End Sub Calculate


sub calc_by_class_bits
{
 my $error="";
 if ($infstruct[0] eq "1" && $in{'bits'} > 16) {
  $error=$text{'ipsc_lib_err_b'};
 }
 elsif ($infstruct[0] eq "2" && $in{'bits'} > 8) {
  $error=$text{'ipsc_lib_err_c'};
 }

 if ($error) {
  $csnclassbitsresult="<TR><TD COLSPAN=3><TABLE BORDER=0 WIDTH=100%><TR><TD>$error</TD></TR></TABLE></TD></TR>";
 } else {
  $csnclassbitsresult=&output_by_bits($in{'bits'});
 }

 if ($config{'keepresults'})
 {
  $keepclassbits="<INPUT TYPE=\"hidden\" NAME=\"keepclassbits\" VALUE=1>";
 }
}

sub calc_by_num_hosts
{
 my $error="";
 my $num=$in{'numhosts'};
 if (! &is_number($num) ) {
    $error=$text{'ipsc_lib_err_nan'};
 } elsif ($num > pow(2, 24) ) {
    $error=&text('ipsc_lib_err_toobig', &pow(2, 24));
 } elsif ($num eq '') {
    $error=$text{'ipsc_lib_err_nothing'};
 }

 if ($error)
 {
  $csnnumhostsresult="<TR><TD>$error</TD></TR>";
 }
 else
 {
  for (my $i=0; $i <= 2; $i++)
  {
   if ($num <= &pow(2, 32-$classbits[$i]) )
   {
    @infstruct=&set_infstruct($i);
   }
  }

  my $subnetbits = 0;
  while ( (&pow(2, (32-$subnetbits-$infstruct[5]-1) ) - $num) >= 0)
  {
   $subnetbits++;
  }    
  $csnnumhostsresult = &output_by_bits($subnetbits);
 }

 if ($config{'keepresults'})
 {
  $keepnumhosts="<INPUT TYPE=\"hidden\" NAME=\"keepnumhosts\" VALUE=1>";
 }
} ## END of calc_by_num_hosts()


sub numberize {
 (my $a, my $b, my $c, my $d) = split(/\./, $_[0]);
 return(($a << 24) | ($b << 16) | ($c << 8) |  $d);
}

sub denumberize {
 my $tmpstr=join('.', ($_[0] & 0xff000000) >> 24,
                     ($_[0] & 0x00ff0000) >> 16,
                     ($_[0] & 0x0000ff00) >> 8,
                     ($_[0] & 0x000000ff) );
$tmpstr;
}

sub ip_range {
 my $start=&numberize($_[0]);
 my $end=&numberize($_[1]);

 my @tmp="";

 if ($start <= $end) {

  for (my $i=$start; $i <= $end; $i++) {
   push(@tmp, &denumberize($i))
  }
 } else { $tmp[0] = $text{'ipsc_lib_err_startgtend'} }

@tmp;
}

sub calc_netmask {
 my $bits=$_[0]; ## hostbits as parameter
 my $netmask=pow(2, 32);
 
 $netmask -= pow(2, $bits);

&denumberize($netmask);
}

sub output_by_bits
{
 my $bits=$_[0];
 my $output="";
 
 if (!&is_number($bits))
 {
  $output="<TR><TD COLSPAN=3>".&text('ipsc_lib_err_bitsnan', $bits);
 }
 else
 {
  $output = " <TR><TD COLSPAN=3><BR><HR></TD></TR>";
  $output .= " <TR><TD COLSPAN=3><BR><U>".&text('ipsc_lib_classinfo', $infstruct[1]).":</U></TD></TR>";
  $output .= "<TR><TD>$text{'ipsc_lib_iprange'}: $infstruct[4]</TD>\n";
  $output .= "<TD>$text{'ipsc_lib_classmask'}: $infstruct[2]</TD>\n";
  $output .= "<TD>$text{'ipsc_lib_hexclassmask'}: $infstruct[3]</TD>\n</TR>";

  $output .= " <TR><TD COLSPAN=3><BR><U>".&text('ipsc_lib_netmaskinfo', $bits).":</U></TD></TR>";

  if ( $bits == 0 ) { $subnet_max = 1 } else {$subnet_max = pow(2, $bits) }
  $output .= "<TR><TD>$text{'ipsc_lib_subnets'}: $subnet_max</TD>\n";

  $hostbits = 32 - ($infstruct[5] + $bits);
  $host_max = pow(2, $hostbits);  
  $output .= "<TD>$text{'ipsc_lib_hosts'}: $host_max</TD>\n";

  $netmask = &calc_netmask($hostbits);
  $output .= "<TD><B>$text{'ipsc_lib_netmask'}: $netmask</B></TD></TR>\n";
  $output .= " <TR><TD COLSPAN=3><BR><U>$text{'ipsc_lib_bitmap'}</U></TD></TR>";
  $bitmap=&get_bitmap($infstruct[5], $bits, $hostbits);
  $output .= " <TR><TD COLSPAN=3>$bitmap</TD>";
 
  $output .= "</TR>\n";
 } 

return $output;
}

sub get_bitmap {
 my $classbits = $_[0];
 my $subnetbits = $_[1];
 my $hostbits = $_[2];
 
 my $dots=0;
 my $bitmap = "x" x 8 . "." . "x" x 8 . "." . "x" x 8 ."." . "x" x 8;
 
 for (my $i=1; $i <= 35; $i++) {
  if ($bitmap[$i] ne ".")
  {
   if ($i <= $classbits+$dots) { $bitmap =~ s/x/n/ }
   elsif ($i <= $classbits+$subnetbits+$dots) { $bitmap =~ s/x/s/ }
   elsif ($i <= $classbits+$subnetbits+$hostbits+$dots) { $bitmap =~ s/x/h/ }
  }
  else
  {
   $dots++
  }
  
 } 

$bitmap;
}

sub pow {
 # function returns the value of $base raised to the power of $exponent.
 # This implementation is not usable for negative exponents!
 # Slow version, should implement another, we'll see...

 my $base = $_[0];
 my $exponent = $_[1];
 my $tmpresult=0;

 if ($exponent == 0) { $tmpresult = 1 } else { $tmpresult=$base }
 for (my $i=2; $i <= $exponent; $i++) {
  $tmpresult = $tmpresult * $base;
 }
 if ($exponent < 0) { $tmpresult = 0 }

return $tmpresult;
}

sub set_infstruct
{
 my @tmpstruct="";

 # INFSTRUCT is a list used as something like a struct. It has the following fields:
 # 0: Class-ID - 0 is A, 1 is B, 2 is C (is standard, probably C-nets are most common)
 # 1: Class-Letter - A, B, or C
 # 2: Classmask: Subnetmask for the class
 # 3: Hex-Classmask: Subnetmask for the class as hex
 # 4: Class range: Range of IP for the class
 # 5: Bits for Network reserved in appropriate class

 my $class=$_[0];
 $tmpstruct[0] = $class;

 push(@tmpstruct, $classes[$tmpstruct[0]]);
 push(@tmpstruct, $classmask[$tmpstruct[0]]);
 push(@tmpstruct, $hexclmask[$tmpstruct[0]]);
 push(@tmpstruct, $classrange[$tmpstruct[0]]);
 push(@tmpstruct, $classbits[$tmpstruct[0]]);

@tmpstruct;
}

### End of ipsc-lib.pl ###