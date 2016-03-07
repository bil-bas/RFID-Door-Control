package LAMM::RFID::DoorControl;

use Moo;
use aliased 'LAMM::RFID::DoorControl::Schema';
use aliased 'LAMM::RFID::DoorControl::Fetch';
use Config::Simple;
use namespace::clean;

has config_file => (
  is => 'lazy',
  default => 'config.cfg',
);

has config => (
  is => 'lazy',
  builder => sub {
    my $self = shift;
    my $cfg = Config::Simple->new( syntax => 'ini' );
    $cfg->read( $self->config_file );
    return $cfg->vars();
  },
);

has fetcher => (
  is => 'lazy',
  builder => sub {
    my $self = shift;
    return Fetch->new(
      endpoint => $self->config->{ 'fetch.endpoint' },
      door => $self->config->{ 'main.door' },
    );
  },
);

has schema => (
  is => 'lazy',
  builder => sub {
    my $self = shift;
    return Schema->connect(
      $self->config->{ 'db.dsn' },
      $self->config->{ 'db.username' },
      $self->config->{ 'db.password' },
    );
  },
);

sub deploy {
  my $self = shift;

  $self->schema->deploy;
}

sub update {
  my ( $self ) = @_;

  my $data = $self->fetcher->get;
  my $allowed_rs = $self->schema->resultset( 'AllowedCard' );

  for my $card ( @{ $data->{ allowed_card } } ) {
    $allowed_rs->update_or_create(
      $card,
      { key => 'primary' },
    );
  }
}

1;
