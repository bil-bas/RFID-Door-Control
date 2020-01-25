package LAMM::RFID::DoorServer::Command::user;
use Mojo::Base 'Mojolicious::Command';

use Getopt::Long 'GetOptionsFromArray';
use Term::ReadKey;

has description => 'User management for LAMM::RFID::DoorServer';

has usage => <<EOF;
Usage: APPLICATION user --add|--rem [OPTIONS]

Options:
  --add              Add a new user
  --rem              Remove a user

  --user <username>  Username to perform operation on


EOF

sub run {
  my ( $self, @args) = @_;

  my $add = 0;
  my $remove = 0;
  my $user = '';
  my $email = '';
  my $password = '';

  GetOptionsFromArray \@args,
    'add'    => \$add,
    'rem'    => \$remove,
    'pass=s' => \$password,
    'user=s' => \$user;

  if ( ! defined $user ) {
    print "Must provide a user!\n";
    print $self->usage;
    return;
  }

  my $user_rs = $self->app->db->resultset('User');

  if ($add) {
    print "Adding $user\n";

    if ( $user_rs->find({ username => $user }) ) {
      print "User already exists, aborting\n";
      return;
    }

    if ( ! defined $password ) {
      print "Input Password: ";
      ReadMode('noecho');
      $password = ReadLine(0);
      chomp $password;
      ReadMode('normal');
      print "\n";
    }

    $user_rs->create({
      username => $user,
      password => $password,
    });

  } elsif ($remove) {
    print "Removing $user\n";

    my $user_result = $user_rs->find({ username => $user });

    if ( $user_result ) {
      $user_result->delete;
    } else {
      print "No User with that name\n";
    }
  } else {
    print "Must provide --add or --remove\n";
    print $self->usage;
  }
}

1;
