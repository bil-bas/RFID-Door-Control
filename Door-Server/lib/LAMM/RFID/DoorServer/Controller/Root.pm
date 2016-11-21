package LAMM::RFID::DoorServer::Controller::Root;
use Mojo::Base 'Mojolicious::Controller';

sub auth {
  my $c = shift;
  return 1 if $c->is_user_authenticated;

  $c->redirect_to($c->url_for('/'));

  return 0;
}

sub index {
  my $c = shift;
}

sub auth_login {
  my $c = shift;

  my $username = $c->param('username');
  my $password = $c->param('password');

  if ( defined $username && defined $password ) {
    $c->app->log->debug("Login attempt for [$username]");
    $c->authenticate( $username, $password );
  }

  $c->is_user_authenticated
    ? $c->redirect_to($c->url_for('/admin'))
    : $c->redirect_to($c->url_for('/'));
  
}

sub auth_logout {
  my $c = shift;
  $c->logout;
  $c->redirect_to($c->url_for('/'));
}

1;
