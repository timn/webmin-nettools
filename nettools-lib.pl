################################################################################
#                                                                              #
#          nettools-lib.pl Library of Nettools Definitions and subs            #
#                    Tim Niemueller <tim@niemueller.de>                        #
#                         http://www.niemueller.de                             #
#                                                                              #
################################################################################
#              Copyright (C) 1999-2000 by Tim Niemueller (GPL)                 #
################################################################################

#    Network Utilities Webmin Module
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

#    Created: 01.09.1999



do '../web-lib.pl';

$|=1;

&init_config("nettools");
%access = &get_module_acl();
$allow = $config{"allow_other_if_failed"};
$cl=$text{'config_link'};

@programs=($config{"ping_path"}, $config{"traceroute_path"},$config{"nslookup_path"},
           $config{"nmap_path"},$config{"dig_path"});
@programnames=("ping", "traceroute", "nslookup", "nmap", "dig");
@programbuttons=("   $text{'lib_ping'}   ", "  $text{'lib_traceroute'}  ", "  $text{'lib_lookup'}  ",
                 "  $text{'lib_nmap'}  ", "   $text{'lib_dig'}   ");
@standopt=("-c 5 -s 56 HOST 2>&1", "-m 30 HOST 40 2>&1", "-query=A HOST 2>&1", "-sT -v -F HOST 2>&1", "HOST A IN");
 if ($gconfig{'os_type'} eq "solaris") {
   $standopt[0]="HOST 2>&1";
 }
@progs_wo_bin=('ipsc', 'whois');

 
$programcount=@programnames;

$tdwidth=80/($programcount); ## 80 because 20% for hostname cell

$progname = $ENV{'SCRIPT_NAME'};
$user = $ENV{'REMOTE_USER'};
$binary = "";


sub init_command
{
 
 $prog = $config{"$_[0]_path"};
 if ($prog) { $binary=$prog } else { $binary="$_[0]" }

 if (!$access{$_[0]})
 {
  &error(&text('lib_accden', $user, $_[0]));
 }

 $whatfailed=$text{'lib_init_error'};

  if ($prog) {
   if (! -e $binary) {
    &error(&text('lib_init_fnex', $binary, $cl))
   } elsif(! -x $binary) {
    &error(&text('lib_init_fne', $binary, $cl))
   }
  } else {
   if (! has_command($binary) && &indexof($binary, @progs_wo_bin) < 0) {
    &error(&text('lib_init_dfnf', $binary, $cl))
   }
  }  

}


sub is_number {
 return ($_[0] =~ /^\d+$/);
}

$version="0.79.1";
### END.