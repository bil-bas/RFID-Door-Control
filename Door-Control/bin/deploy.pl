use strict;
use warnings;

use LAMM::RFID::DoorControl;

my $dc = LAMM::RFID::DoorControl->new;

$dc->deploy;
