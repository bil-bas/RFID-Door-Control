package LAMM::RFID::DoorControl::Schema::Result::AllowedCard;

use DBIx::Class::Candy -autotable => v1;

primary_column user_id => {
  data_type => 'int',
};

unique_column card_key => {
  data_type => 'varchar',
  size => '64',
  is_nullable => 0,
};

1;
