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
  coerce => sub {
    # Make sure the endpoint has a trailing slash
    $_[0] =~ m!/$! ? $_[0] : $_[0] . "/";
  },
);

has door => (
  is => 'ro',
  required => 1,
);

has key => (
  is => 'ro',
  required => 1,
);

has uri => (
  is => 'lazy',
  builder => sub {
    my $self = shift;
    my $uri = URI->new( $self->endpoint );
    $uri->query_form( door => $self->door, key => $self->key );
    return $uri;
  },
);

sub get {
  my $self = shift;

  my $return = $self->ua->get( $self->uri );
  return undef if $return->code != 200;
  return $self->json->decode( $return->decoded_content );
}

1;
