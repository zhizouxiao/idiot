drop table if exists account;
create table account(
  id integer primary key autoincrement,
  username varchar(100) not null,
  apply_money float,
  actual_money float,
  datetime date,
  note text not null
);
