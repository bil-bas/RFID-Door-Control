package LAMM::RFID::DoorServer::Controller::Admin::Assign;
use Mojo::Base 'Mojolicious::Controller';

sub index {
  my $c = shift;
  $c->redirect_to($c->url_for(action => 'list'));
}

sub list {
  my $c = shift;
  $c->render( door_rs => $c->db->resultset('Door'), card_rs => $c->db->resultset('Card') );
}

sub door {
  my $c = shift;

  my $door_id = $c->param('door');

  my $door_result = $c->db->resultset('Door')->find($door_id);

  if ($door_result) {
    $c->render( door_result => $door_result, card_rs => $c->db->resultset('Card') );
  } else {
    $c->flash(message => 'No Such Door');
    $c->redirect_to($c->url_for(action => 'list'));
  }
}

sub assign_card {
  my $c = shift;

  my $card_id = $c->param('card');
  my $door_id = $c->param('door');

  my $card_result = $c->db->resultset('Card')->find($card_id);
  my $door_result = $c->db->resultset('Door')->find($door_id);

  if ( ! defined $door_result ) {
    $c->flash(message => 'No Such Door');
    $c->redirect_to($c->url_for(action => 'list'));
    return;
  } elsif ( ! defined $card_result ) {
    $c->flash(message => 'No Such Card');
  } else {
    $c->_toggle_assignment($card_result, $door_result);
  }

  $c->redirect_to($c->url_for(action => 'door')->query(door => $door_id));
}

sub card {
  my $c = shift;

  my $card_id = $c->param('card');

  my $card_result = $c->db->resultset('Card')->find($card_id);

  if ($card_result) {
    $c->render( card_result => $card_result, door_rs => $c->db->resultset('Door') );
  } else {
    $c->flash(message => 'No Such Card');
    $c->redirect_to($c->url_for(action => 'list'));
  }
}

sub assign_door {
  my $c = shift;

  my $card_id = $c->param('card');
  my $door_id = $c->param('door');

  my $card_result = $c->db->resultset('Card')->find($card_id);
  my $door_result = $c->db->resultset('Door')->find($door_id);

  if ( ! defined $card_result ) {
    $c->flash(message => 'No Such Card');
    $c->redirect_to($c->url_for(action => 'list'));
    return;
  } elsif ( ! defined $door_result ) {
    $c->flash(message => 'No Such Door');
  } else {
    $c->_toggle_assignment($card_result, $door_result);
  }

  $c->redirect_to($c->url_for(action => 'card')->query(card => $card_id));
}

sub _toggle_assignment {
  my ($c, $card_result, $door_result) = @_;

  my $assign_result = $card_result->find_or_new_related(
    'card_doors',
    { door_id => $door_result->id }
  );
  if ( $assign_result->in_storage ) {
    $assign_result->delete;
  } else {
    $assign_result->insert;
  }
}

1;
