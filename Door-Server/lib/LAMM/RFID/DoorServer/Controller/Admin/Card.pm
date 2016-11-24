package LAMM::RFID::DoorServer::Controller::Admin::Card;
use Mojo::Base 'Mojolicious::Controller';

sub index {
  my $c = shift;
  $c->redirect_to($c->url_for(action => 'list'));
}

sub list {
  my $c = shift;
  $c->render( card_rs => $c->db->resultset('Card') );
}

sub add {
  my $c = shift;

  my $name = $c->param('name');

  if (defined $name && length $name) {
    $c->app->log->debug("Creating card with name [$name]");
    my $card_result = $c->db->resultset('Card')->create_card($name);
    if (defined $card_result) {
      $c->flash(message => 'Card Created');
    } else {
      $c->flash(message => 'Card Creation Failed');
    }
  }
  $c->redirect_to($c->url_for('list'));
}

sub del {
  my $c = shift;

  my $card_id = $c->param('card');

  my $card_result = $c->db->resultset('Card')->find($card_id);

  if (defined $card_result) {
    $card_result->delete;
    $c->flash(message => 'Card Deleted');
  } else {
    $c->flash(message => 'No such card');
  }
  $c->redirect_to($c->url_for('list'));
}


1;
