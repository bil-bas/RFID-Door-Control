package LAMM::RFID::DoorServer;

use Web::Simple;

sub dispatch_request {
  GET => sub {
    [ 200, [ 'Content-type', 'text/plain' ], [ 'Hello world!' ] ]
  },
  '' => sub {
    [ 405, [ 'Content-type', 'text/plain' ], [ 'Method not allowed' ] ]
  }
}

__PACKAGE__->run_if_script;
