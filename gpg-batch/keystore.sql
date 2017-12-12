CREATE TABLE keystore (
	keyid		varchar(10) primary key,
	fingerprint varchar(40),
	created 	datetime default current_timestamp,
	name		text,
	email		varchar(128),
	pubkey      text
);