package LAMM::RFID::DoorServer::DB::ResultSet::Card;

use strict;
use warnings;

use base 'DBIx::Class::ResultSet';

use String::Random;
use Devel::Dwarn;

sub create_card {
  my ( $self, $name ) = @_;

  my $key = String::Random::random_string('0' x 32, [ 0 .. 9, 'a' .. 'f' ]);

  if ( defined $self->find({ name => $name }) ) {
    return;
  }

  return $self->create({
    name => $name,
    card_key => $key,
  });
}

1;
