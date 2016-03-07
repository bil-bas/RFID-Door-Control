package LAMM::RFID::DoorControl::Fetch;

use Moo;
use LWP::UserAgent;
use JSON::MaybeXS;
use namespace::clean;

has ua => (
  is => 'lazy',
  builder => sub {
    return LWP::UserAgent->new();
  },
);

has json => (
  is => 'lazy',
  builder => sub {
    return JSON::MaybeXS->new;
  },
);

has endpoint => (
  is => 'ro',
  required => 1,
);

has door => (
  is => 'ro',
  required => 1,
);

sub get {
  my $self = shift;

  my $return = $self->ua->get( $self->endpoint . "/" . $self->door );
  return $self->json->decode( $return->decoded_content );
}

1;
