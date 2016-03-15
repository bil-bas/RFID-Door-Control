package LAMM::RFID::DoorControl::Schema;

use base qw/ DBIx::Class::Schema /;

__PACKAGE__->load_classes({ __PACKAGE__.'::Result' => [ qw(AllowedCard) ] });

1;
