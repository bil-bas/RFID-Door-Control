package LAMM::RFID::DoorServer::Controller::Admin::Door;
use Mojo::Base 'Mojolicious::Controller';

sub index {
  my $c = shift;
  $c->redirect_to($c->url_for(action => 'list'));
}

sub list {
  my $c = shift;
  $c->render( door_rs => $c->db->resultset('Door') );
}

sub add {
  my $c = shift;

  my $name = $c->param('name');

  if (defined $name && length $name) {
    $c->app->log->debug("Creating door with name [$name]");
    $c->db->resultset('Door')->create_door($name);
  }
  $c->redirect_to($c->url_for('list'));
}

sub del {
  my $c = shift;
  
  my $door = $c->param('door');

  my $door_result = $c->db->resultset('Door')->find($door);

  if (defined $door_result) {
    $door_result->delete;
    $c->flash(message => 'Door Deleted');
  } else {
    $c->flash(message => 'No such door');
  }
  $c->redirect_to($c->url_for('list'));
}

1;
