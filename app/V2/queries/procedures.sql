-- users table related operations;
-- list all users
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

-- get a user by id
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

-- get a user by username
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

-- add a new user
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

-- edit an existing user
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

-- modify username
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

-- check if username exists
CREATE OR REPLACE FUNCTION check_username_exists(
  user_name varchar
)
  RETURNS boolean AS $$
BEGIN
  return (select exists(select * from tbl_users where username = user_name));
END;
$$
LANGUAGE plpgsql;

-- delete user record
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

-- select * from modify_user(3, 'tash', 'francis', 'gitau', 'kinuthia', 'fgkinus@gmail.com', 'pass', FALSE);





