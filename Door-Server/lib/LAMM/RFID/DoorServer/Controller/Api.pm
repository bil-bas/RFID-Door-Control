package LAMM::RFID::DoorServer::Controller::Api;
use Mojo::Base 'Mojolicious::Controller';

sub auth {
  my $c = shift;

  my $key = $c->param('key') || undef;
  my $door = $c->param('door') || undef;

  if ( defined $door && defined $key ) {

    $c->app->log->debug("Received API Auth for [$door:$key]");

    my $door_result = $c->db->resultset('Door')->find({name => $door});

    if ( $door_result && $door_result->key eq $key ) {
      $c->stash( door_result => $door_result );
      return 1;
    }

  } else {
    $c->render(json => { success => 0 });
    return 0;
  }
}

sub index {
  my $c = shift;
  $c->render(json => { success => 1 });
}

sub fetch {
  my $c = shift;

  my $door_result = $c->stash('door_result');

  my $cards_rs = $door_result->cards->search({},{
    select => [ qw/ id card_key / ],
    'as' => [ qw/ user_id card_key / ],
  });

  $cards_rs->result_class('DBIx::Class::ResultClass::HashRefInflator');

  my @cards = $cards_rs->all;

  $c->render(json => { allowed_card => \@cards });
}

1;
