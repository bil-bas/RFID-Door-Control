package LAMM::RFID::DoorServer::DB::Result::CardDoor;

use DBIx::Class::Candy
  -autotable => v1;

column card_id => {
  data_type => 'int',
};

column door_id => {
  data_type => 'int',
};

primary_key qw/ card_id door_id /;

belongs_to 'card', 'LAMM::RFID::DoorServer::DB::Result::Card', { id => 'card_id' };
belongs_to 'door', 'LAMM::RFID::DoorServer::DB::Result::Door', { id => 'door_id' };

1;
