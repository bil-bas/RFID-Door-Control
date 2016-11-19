package LAMM::RFID::DoorServer::DB::ResultSet::Door;

use strict;
use warnings;

use base 'DBIx::Class::ResultSet';

use String::Random;
use Devel::Dwarn;

sub create_door {
  my ( $self, $name ) = @_;

  my $key = String::Random::random_regex('\w{20}');

  if ( defined $self->find({ name => $name }) ) {
    return;
  }

  return $self->create({
    name => $name,
    key => $key,
  });
}

1;
