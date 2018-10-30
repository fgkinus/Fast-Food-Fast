create table if not exists tbl_users
(
  id         serial                not null
    constraint tbl_users_pkey
    primary key,
  username   varchar(50)           not null,
  email      varchar(50)           not null,
  firstname  varchar(50),
  secondname varchar(50),
  surname    varchar(50),
  password   varchar(5000)         not null,
  isadmin    boolean default false not null,
  created    timestamp default now(),
  modified   timestamp
);


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
  location varchar(55)             not null,
  created  timestamp default now() not null,
  modified timestamp
);


create unique index if not exists tbl_orders_id_uindex
  on tbl_orders (id);

create table if not exists tbl_ref_status
(
  id          serial not null
    constraint tbl_ref_status_pkey
    primary key,
  description varchar(10) unique default 'New' :: character varying,
  created     timestamp          default now(),
  modified    timestamp
);


create unique index if not exists tbl_ref_status_id_uindex
  on tbl_ref_status (id);

create table if not exists tbl_order_status
(
	id serial not null
		constraint tbl_order_status_pkey
			primary key,
	"order" integer not null
		constraint tbl_order_status_tbl_orders_id_fk
			references tbl_orders
				on update cascade on delete cascade,
	status integer
		constraint tbl_order_status_tbl_ref_status_id_fk
			references tbl_ref_status
				on update cascade on delete cascade,
	created timestamp default now(),
	modified timestamp,
	owner integer not null
		constraint tbl_order_status_tbl_users_id_fk
			references tbl_users
				on update cascade on delete cascade
)
;


create unique index if not exists tbl_order_status_id_uindex
	on tbl_order_status (id)
;

create unique index if not exists tbl_order_status_order_uindex
	on tbl_order_status ("order")
;



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


create unique index if not exists tbl_user_images_id_uindex
  on tbl_user_images (id);

create table if not exists tbl_menuitem_images
(
  id      serial  not null
    constraint tbl_menuitem_images_pkey
    primary key,
  image   varchar   not null,
  item_id integer not null
    constraint tbl_menuitem_images_tbl_menuitems_id_fk
    references tbl_menuitems
    on update cascade on delete cascade,
  created timestamp default now()
);


create unique index if not exists tbl_menuitem_images_id_uindex
  on tbl_menuitem_images (id);

insert into tbl_users (username, email, firstname, secondname, surname, password, isadmin)
VALUES ('admin',
        'admin@email.com',
        'first',
        'second',
        'surname',
        '$pbkdf2-sha256$29000$qdV6j7E25lxLae1dK2UMAQ$RdOvB.vKESGyl6H15Y6byTvLczKdSbqVd.hcKK6YCX8',
        TRUE)
ON CONFLICT (email) DO NOTHING;

insert into tbl_users (username, email, firstname, secondname, surname, password, isadmin)
VALUES ('fgkinus',
        'kinusfg@email.com',
        'francis',
        'GItau',
        'surname',
        '$pbkdf2-sha256$29000$qdV6j7E25lxLae1dK2UMAQ$RdOvB.vKESGyl6H15Y6byTvLczKdSbqVd.hcKK6YCX8',
        FALSE)
ON CONFLICT (email) DO NOTHING;

insert into tbl_ref_status (description)
VALUES ('New')
on conflict (description) DO NOTHING;
insert into tbl_ref_status (description)
VALUES ('Processing')
on conflict (description) DO NOTHING;
insert into tbl_ref_status (description)
VALUES ('Approved')
on conflict (description) DO NOTHING;
insert into tbl_ref_status (description)
VALUES ('Cancelled')
on conflict (description) DO NOTHING;

