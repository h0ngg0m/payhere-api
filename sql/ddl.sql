create table product
(
    id           bigint auto_increment
        primary key,
    category     varchar(255) not null,
    price        bigint       not null,
    cost         bigint       not null,
    name         varchar(255) not null,
    description  varchar(255) not null,
    barcode      varchar(255) not null,
    expiry_date  varchar(255) not null,
    size         varchar(255) not null,
    name_chosung varchar(255) not null
) collate = utf8mb4_general_ci;

create table user
(
    id          bigint auto_increment
        primary key,
    tel         varchar(255)  not null,
    password    varchar(1000) not null,
    logout_flag tinyint(1) null
) collate = utf8mb4_general_ci;