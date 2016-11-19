package LAMM::RFID::DoorServer::DB::Result::User;

use DBIx::Class::Candy
  -autotable => v1,
  -components => [ 'PassphraseColumn' ];
use Authen::Passphrase::RejectAll;

primary_column id => {
  data_type => 'int',
  is_auto_increment => 1,
};

unique_column username => {
  data_type => 'varchar',
  size => 255,
};

column password => {
  data_type => 'varchar',
  size => 100,
  passphrase => 'crypt',
  passphrase_class => 'BlowfishCrypt',
  passphrase_args => {
    salt_random => 20,
    cost => 8,
  },
  passphrase_check_method => 'check_password',
  default => Authen::Passphrase::RejectAll->new->as_crypt,
};

1;
