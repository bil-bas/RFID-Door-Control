package LAMM::RFID::DoorServer::Controller::Admin::User;
use Mojo::Base 'Mojolicious::Controller';

sub index {
  my $c = shift;
  $c->redirect_to($c->url_for(action => 'list'));
}

sub list {
  my $c = shift;
  $c->render( user_rs => $c->db->resultset('User') );
}

sub edit {
  my $c = shift;
  my $user_result = $c->db->resultset('User')->find($c->param('uid'));
  if ( $user_result ) {
    $c->render( user_result => $user_result );
  } else {
    $c->flash( message => 'User Not Found');
    $c->redirect_to($c->url_for(action => 'list'));
  }
}

sub add {
  my $c = shift;
  
  my $username = $c->param('username');
  my $password = $c->param('password');

  if ( $username && $password ) {
    if ( $c->db->resultset('User')->find({ username => $username }) ) {
      $c->flash( message => 'User already exists, not creating' );
    } else {
      $c->db->resultset('User')->create({
          username => $username,
          password => $password,
        });
      $c->flash( message => 'User Added');
    }
  } else {
    $c->flash( message => 'Need Username and Password to Add User');
  }
  $c->redirect_to($c->url_for(action => 'list'));
}

sub update {
  my $c = shift;
  
  my $user_result = $c->db->resultset('User')->find($c->param('uid'));
  my $username = $c->param('username');
  my $password = $c->param('password');

  if ( !$user_result ) {
    $c->flash( message => 'User Not Found');
    $c->redirect_to($c->url_for(action => 'list'));
  }

  if ( $user_result && $username ) {
    $user_result->update({
        username => $username,
        ( $password ? ( password => $password ) : () )
      });
    $c->flash( message => 'User Updated');
  } else {
    $c->flash( message => 'Need Username for Edit User');
  }
  $c->redirect_to($c->url_for(action => 'edit')->query(uid => $user_result->id));
}

sub del {
  my $c = shift;

  my $uid = $c->param('uid');

  if ( my $user_result = $c->db->resultset('User')->find($uid) ) {
    $user_result->delete;
    $c->flash( message => 'User Deleted' );
  }
  $c->redirect_to($c->url_for(action => 'list'));
}

1;
