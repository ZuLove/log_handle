#drop database logdatabase;
create database if not exists xytx_jiuzhou;
use xytx_jiuzhou;

create table if not exists login(
id int not null auto_increment primary key,
date date not null,
time time not null,
role_name varchar(32) not null,
ip varchar(32) not null
);

create table if not exists online_player_count(
id int not null auto_increment primary key,
date date not null,
time time not null,
clock int not null,
num int not null
);

create table if not exists item_move(
id int not null auto_increment primary key,
date date not null,
time time not null,
type varchar(32) not null,
source varchar(32) not null,
dest varchar(32) not null,
item_name varchar(32) not null,
item_count int not null,
map_id int not null,
x int not null,
y int not null,
source_ip varchar(32) not null,
dest_ip varchar(32) not null
);

create table if not exists monster_die(
id int not null auto_increment primary key,
date date not null,
time time not null,
role_name varchar(32) not null,
monster_name varchar(32) not null,
x int not null,
y int not null
);