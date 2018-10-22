proceedures = [
    """
    CREATE OR REPLACE FUNCTION get_users2()
  RETURNS setof tbl_users AS $$
DECLARE
  rReturn tbl_users;
BEGIN
  for rReturn in
  SELECT * FROM tbl_users -- Open a cursor
  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION get_users_by_id(
  id_no INT
)
  RETURNS setof tbl_users AS $$
DECLARE
  rReturn tbl_users;
BEGIN
  for rReturn in
  SELECT * FROM tbl_users u WHERE u.id = id_no -- Open a cursor
  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION get_users_by_username(
  user_name VARCHAR
)
  RETURNS setof tbl_users AS $$
DECLARE
  rReturn tbl_users;
BEGIN
  for rReturn in
  SELECT * FROM tbl_users u WHERE u.username = user_name -- Open a cursor
  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION get_user_by_email(
  user_email VARCHAR
)
  RETURNS setof tbl_users AS $$
DECLARE
  rReturn tbl_users;
BEGIN
  for rReturn in
  SELECT * FROM tbl_users u WHERE u.email = user_email -- Open a cursor
  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION add_user(
  username   varchar,
  firstname  varchar,
  secondname varchar,
  surname    varchar,
  email      varchar,
  password   varchar,
  isadmin    boolean
)
  RETURNS setof tbl_users AS $$
DECLARE
  rReturn tbl_users;
BEGIN
  for rReturn in
  INSERT INTO tbl_users (username, firstname, secondname, surname, email, password, isadmin) VALUES
  (
    username, firstname, secondname, surname, email, password, isadmin
  )
  returning *
  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION modify_user(
  user_id       int,
  user_name     varchar,
  firs_tname    varchar,
  second_name   varchar,
  sur_name      varchar,
  user_email    varchar,
  user_password varchar,
  user_role     boolean
)
  RETURNS setof tbl_users AS $$
DECLARE
  rReturn tbl_users;
BEGIN
  for rReturn in
  update tbl_users u
  set
    username   = user_name,
    firstname  = firs_tname,
    secondname = second_name,
    surname    = sur_name,
    email      = user_email,
    password   = user_password,
    isadmin    = user_role,
    modified   = now()
  where u.id = user_id
  returning *
  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION modify_user_name(
  user_id   int,
  user_name varchar
)
  RETURNS setof tbl_users AS $$
DECLARE
  rReturn tbl_users;
BEGIN
  for rReturn in
  update tbl_users u
  set
    username = user_name,
    modified = now()
  where u.id = user_id
  returning *
  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;

-- check if email exists
CREATE OR REPLACE FUNCTION check_email_exists(
  user_email varchar
)
  RETURNS boolean AS $$
BEGIN
  return (select exists(select * from tbl_users where email = user_email));
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION check_username_exists(
  user_name varchar
)
  RETURNS boolean AS $$
BEGIN
  return (select exists(select * from tbl_users where username = user_name));
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION delete_user(
  user_id int
)
  RETURNS setof tbl_users AS $$
DECLARE
  rReturn tbl_users;
BEGIN
  for rReturn in
  DELETE from tbl_users where tbl_users.id = user_id
  returning *
  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION get_menu_items()
  RETURNS setof tbl_menuitems AS $$
DECLARE
  rReturn tbl_menuitems;
BEGIN
  for rReturn in
  SELECT * FROM tbl_menuitems -- Open a cursor
  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
--select * from get_menu_items();

--get menu item by id
CREATE OR REPLACE FUNCTION get_menu_item_by_id(
  item_id int
)
  RETURNS setof tbl_menuitems AS $$
DECLARE
  rReturn tbl_menuitems;
BEGIN
  for rReturn in
  SELECT * FROM tbl_menuitems where id = item_id -- Open a cursor
  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION get_menu_item_by_name(
  item_name varchar
)
  RETURNS setof tbl_menuitems AS $$
DECLARE
  rReturn tbl_menuitems;
BEGIN
  for rReturn in
  SELECT * FROM tbl_menuitems where name = item_name
  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION add_menu_item(
  item_name  varchar,
  item_price DOUBLE PRECISION,
  item_owner int
)
  RETURNS setof tbl_menuitems AS $$
DECLARE
  rReturn tbl_menuitems;
BEGIN
  for rReturn in

  INSERT INTO tbl_menuitems (name, price, owner) VALUES (item_name, item_price, item_owner)
  RETURNING *


  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION edit_menu_item(
  item_id    int,
  item_name  varchar,
  item_price DOUBLE PRECISION,
  item_owner int
)
  RETURNS setof tbl_menuitems AS $$
DECLARE
  rReturn tbl_menuitems;
BEGIN
  for rReturn in

  UPDATE tbl_menuitems
  SET name = item_name, price = item_price, owner = item_owner, modified = now()
  WHERE id = item_id
  RETURNING *


  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION delete_menu_item(
  item_id int
)
  RETURNS setof tbl_menuitems AS $$
DECLARE
  rReturn tbl_menuitems;
BEGIN
  for rReturn in

  DELETE FROM tbl_menuitems WHERE id = item_id
  RETURNING *

  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION get_order_items()
  RETURNS setof tbl_orders AS $$
DECLARE
  rReturn tbl_orders;
BEGIN
  for rReturn in
  SELECT * FROM tbl_orders -- Open a cursor
  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION get_order_item_by_id(
  item_id int
)
  RETURNS setof tbl_orders AS $$
DECLARE
  rReturn tbl_orders;
BEGIN
  for rReturn in
  SELECT * FROM tbl_orders where id = item_id -- Open a cursor
  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION get_order_item_by_user_id(
  user_id int
)
  RETURNS setof tbl_orders AS $$
DECLARE
  rReturn tbl_orders;
BEGIN
  for rReturn in
  SELECT * FROM tbl_orders where "user" = user_id -- Open a cursor
  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION add_order_item(
  order_item     int,
  order_quantity int,
  order_location varchar,
  order_owner    int
)
  RETURNS setof tbl_orders AS $$
DECLARE
  rReturn tbl_orders;
BEGIN
  for rReturn in

  INSERT INTO tbl_orders ("user", item, quantity, location)
  VALUES (order_owner, order_item, order_quantity, order_location)
  RETURNING *


  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION delete_order_item(
  order_id int
)
  RETURNS setof tbl_orders AS $$
DECLARE
  rReturn tbl_orders;
BEGIN
  for rReturn in

  DELETE FROM tbl_orders WHERE id = order_id
  RETURNING *

  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION edit_order_item(
  order_id       int,
  order_item     int,
  order_quantity int,
  order_location varchar(50),
  order_owner    int
)
  RETURNS setof tbl_orders AS $$
DECLARE
  rReturn tbl_orders;
BEGIN
  for rReturn in

  UPDATE tbl_orders
  SET "user" = order_owner, item = order_item, quantity = order_quantity, modified = now(), location = order_location
  WHERE id = order_id
  RETURNING *


  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION get_all_order_status()
  RETURNS setof tbl_ref_status AS $$
DECLARE
  rReturn tbl_ref_status;
BEGIN
  for rReturn in

  select id, description from tbl_ref_status

  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION set_order_status(
  order_id       INT,
  response_id    INT,
  response_owner int
)
  RETURNS setof tbl_order_status AS $$
DECLARE
  rReturn tbl_order_status;
BEGIN
  for rReturn in

  INSERT INTO tbl_order_status ("order", status, owner) VALUES (order_id, response_id, response_owner)
  RETURNING *

  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION edit_order_status(
  order_id       int,
  response_id    int,
  response_owner int
)
  RETURNS setof tbl_order_status AS $$
DECLARE
  rReturn tbl_order_status;
BEGIN
  for rReturn in

  UPDATE tbl_order_status
  SET status = response_id, owner = response_owner, modified = now()
  WHERE "order" = order_id
  RETURNING *

  loop
    return next rReturn;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """,
    """CREATE OR REPLACE FUNCTION get_order_status(
o_id int
)
  RETURNS TABLE (
  order_id int ,
  description varchar
  )
AS $$
DECLARE
  var_r record;
BEGIN
  FOR var_r IN (SELECT st."order",ref.description from tbl_order_status st
  inner join tbl_ref_status ref on st.status  = ref.id
  where "order" = o_id)
    loop
    order_id := var_r."order";
    description := var_r.description;
    RETURN NEXT ;
  end loop;
END;
$$
LANGUAGE plpgsql;
    """
    ,
    """
    insert into tbl_users (username, email, firstname, secondname, surname, password, isadmin)
VALUES ('admin',
        'admin@email.com',
        'first',
        'second',
        'surname',
        '$pbkdf2-sha256$29000$qdV6j7E25lxLae1dK2UMAQ$RdOvB.vKESGyl6H15Y6byTvLczKdSbqVd.hcKK6YCX8',
        TRUE)
ON CONFLICT (email) DO NOTHING;
    """,
    """
    insert into tbl_users (username, email, firstname, secondname, surname, password, isadmin)
VALUES ('fgkinus',
        'kinusfg@email.com',
        'francis',
        'GItau',
        'surname',
        '$pbkdf2-sha256$29000$qdV6j7E25lxLae1dK2UMAQ$RdOvB.vKESGyl6H15Y6byTvLczKdSbqVd.hcKK6YCX8',
        FALSE)
ON CONFLICT (email) DO NOTHING;
    """

]
