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
    country text not null
);