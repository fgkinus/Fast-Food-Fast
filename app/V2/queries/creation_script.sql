create table if not exists tbl_users
(
  id         serial                not null
    constraint tbl_users_pkey
    primary key,
  username   varchar(50)           not null,
  email      varchar(50)           not null,
  firstname  varchar(50)           not null,
  secondname varchar(50)           not null,
  surname    varchar(50),
  password   varchar(50)           not null,
  isadmin    boolean default false not null
);

alter table tbl_users
  owner to postgres;

create unique index if not exists tbl_users_username_uindex
  on tbl_users (username);

create unique index if not exists tbl_users_email_uindex
  on tbl_users (email);

create table if not exists tbl_menuitems
(
  id       serial           not null
    constraint tbl_menuitems_pkey
    primary key,
  name     varchar(50)      not null,
  price    double precision not null,
  added    timestamp default now(),
  modified timestamp,
  owner    integer          not null
    constraint tbl_menuitems_tbl_users_id_fk
    references tbl_users
    on update cascade on delete cascade
);

alter table tbl_menuitems
  owner to postgres;

create unique index if not exists tbl_menuitems_id_uindex
  on tbl_menuitems (id);

create unique index if not exists tbl_menuitems_name_uindex
  on tbl_menuitems (name);

create table if not exists tbl_orders
(
  id       serial                  not null
    constraint tbl_orders_pkey
    primary key,
  "user"   integer                 not null
    constraint tbl_orders_tbl_users_id_fk
    references tbl_users
    on update cascade on delete cascade,
  item     integer                 not null
    constraint tbl_orders_tbl_menuitems_id_fk
    references tbl_menuitems
    on update cascade on delete cascade,
  quantity integer default 1       not null,
  created  timestamp default now() not null,
  modified timestamp
);

alter table tbl_orders
  owner to postgres;

create unique index if not exists tbl_orders_id_uindex
  on tbl_orders (id);

create table if not exists tbl_ref_status
(
  id          serial not null
    constraint tbl_ref_status_pkey
    primary key,
  description varchar(10) default 'Pending' :: character varying,
  created     timestamp   default now(),
  modified    timestamp
);

alter table tbl_ref_status
  owner to postgres;

create unique index if not exists tbl_ref_status_id_uindex
  on tbl_ref_status (id);

create table if not exists tbl_order_status
(
  id       serial  not null
    constraint tbl_order_status_pkey
    primary key,
  "order"  integer not null
    constraint tbl_order_status_tbl_orders_id_fk
    references tbl_orders
    on update cascade on delete cascade,
  status   integer
    constraint tbl_order_status_tbl_ref_status_id_fk
    references tbl_ref_status
    on update cascade on delete cascade,
  created  timestamp default now(),
  modified timestamp,
  owner    integer not null
    constraint tbl_order_status_tbl_users_id_fk
    references tbl_users
    on update cascade on delete cascade
);

alter table tbl_order_status
  owner to postgres;

create unique index if not exists tbl_order_status_id_uindex
  on tbl_order_status (id);

create table if not exists tbl_user_images
(
  id         serial                not null
    constraint tbl_user_images_pkey
    primary key,
  "user"     integer               not null
    constraint tbl_user_images_tbl_users_id_fk
    references tbl_users
    on update cascade on delete cascade,
  image      bytea                 not null,
  is_profile boolean default false not null,
  created    timestamp default now()
);

alter table tbl_user_images
  owner to postgres;

create unique index if not exists tbl_user_images_id_uindex
  on tbl_user_images (id);

create table if not exists tbl_menuitem_images
(
  id      serial  not null
    constraint tbl_menuitem_images_pkey
    primary key,
  image   bytea   not null,
  item_id integer not null
    constraint tbl_menuitem_images_tbl_menuitems_id_fk
    references tbl_menuitems
    on update cascade on delete cascade,
  created timestamp default now()
);

alter table tbl_menuitem_images
  owner to postgres;

create unique index if not exists tbl_menuitem_images_id_uindex
  on tbl_menuitem_images (id);