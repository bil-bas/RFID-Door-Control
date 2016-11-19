package LAMM::RFID::DoorServer::DB::Result::Door;

use DBIx::Class::Candy
  -autotable => v1;

primary_column id => {
  data_type => 'int',
  is_auto_increment => 1,
};

unique_column name => {
  data_type => 'varchar',
  size => 255,
};

column key => {
  data_type => 'varchar',
  size => 100,
};

has_many 'card_doors', 'LAMM::RFID::DoorServer::DB::Result::CardDoor', 'door_id';
many_to_many 'cards' => 'card_doors', 'card';
1;
