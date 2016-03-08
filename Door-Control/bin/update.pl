use strict;
use warnings;

use LAMM::RFID::DoorControl;

my $dc = LAMM::RFID::DoorControl->new_with_options;

$dc->update;
