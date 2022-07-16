 create table if not exists country
(
        id serial constraint country_pk primary key,
        country_code text,
        zip_code text,
        place text,
        statee text,
        state_code text,
        province text,
        province_code text,
        community text,
        community_code text,
        latitude float8,
        longtitude float8
);
create table if not exists users
(
    id       serial
        constraint customer_pk
            primary key,
    name     varchar(256) not null unique,
    password text  not null,
    applicant text not null,
    addres_applicant text not null,
    country text not null,
    il text not null
);
create table if not exists categories
(
    id serial primary key,
    name text not null unique
);
create table if not exists subcategories
(
    name text primary key,
    parent_category int references categories(id)
);
create table if not exists items
(
    id integer primary key,
     latitude float8,
     longtitude float8,
     unique(latitude, longtitude)
);
create table if not exists items_subcategories
(
    item_id int references items(id) on delete cascade,
    name_sub text references subcategories(name) on delete cascade,
    unique(item_id, name_sub)
);
create table if not exists dataset
(
    id integer primary key,
    codes text,
    reglaments text,
    group text,
    name text,
    il text,
    applicant text,
    address_applicant text,
    maker text,
    country text,
    address_maker text
);
