package LAMM::RFID::DoorServer::Command::deploy;
use Mojo::Base 'Mojolicious::Command';

use Getopt::Long 'GetOptionsFromArray';
use Term::ReadKey;

has description => 'Deploy Database for LAMM::RFID::DoorServer';

has usage => <<EOF;
Usage: APPLICATION deploy

EOF

sub run {
  my ( $self, @args) = @_;

  $self->app->db->deploy;
}

1;
