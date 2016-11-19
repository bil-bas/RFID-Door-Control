package LAMM::RFID::DoorServer::DB::Result::Card;

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

unique_column card_key => {
  data_type => 'varchar',
  size => 100,
};

has_many 'card_doors', 'LAMM::RFID::DoorServer::DB::Result::CardDoor', 'card_id';
many_to_many 'doors' => 'card_doors', 'door';

1;
