create table if not exists admin(
    id int auto_increment primary key,
    username varchar(50) not null unique,
    password varchar(200) not null
);