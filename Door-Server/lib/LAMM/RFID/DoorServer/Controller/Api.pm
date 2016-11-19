package LAMM::RFID::DoorServer::Controller::Api;
use Mojo::Base 'Mojolicious::Controller';
use Devel::Dwarn;
sub auth {
  my $c = shift;

  my $key = $c->param('key');
  my $door = $c->param('door');

  $c->app->log->debug("Received API Auth for [$door:$key]");

  return 1;
}

sub index {
  my $c = shift;
  $c->render(json => { success => 1 });
}

1;
