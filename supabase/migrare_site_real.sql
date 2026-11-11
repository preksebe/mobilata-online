-- MobilaTa, site real: completeaza schema din schema_si_date.sql. Se ruleaza o singura data.
-- Datele (created_at) devin text de forma "2026-11-11 14:30", ca in versiunea SQLite, ora Romaniei.

alter table products alter column created_at drop default;
alter table products alter column created_at type text using to_char(created_at at time zone 'Europe/Bucharest', 'YYYY-MM-DD HH24:MI');
alter table products alter column created_at set default to_char(now() at time zone 'Europe/Bucharest', 'YYYY-MM-DD HH24:MI');

alter table reviews alter column created_at drop default;
alter table reviews alter column created_at type text using to_char(created_at at time zone 'Europe/Bucharest', 'YYYY-MM-DD HH24:MI');
alter table reviews alter column created_at set default to_char(now() at time zone 'Europe/Bucharest', 'YYYY-MM-DD HH24:MI');

alter table orders alter column created_at drop default;
alter table orders alter column created_at type text using to_char(created_at at time zone 'Europe/Bucharest', 'YYYY-MM-DD HH24:MI');
alter table orders alter column created_at set default to_char(now() at time zone 'Europe/Bucharest', 'YYYY-MM-DD HH24:MI');

create table if not exists users (
  id bigint generated always as identity primary key,
  username text unique not null,
  password_hash text not null,
  role text not null,
  created_at text not null
);
create table if not exists customers (
  id bigint generated always as identity primary key,
  email text unique not null,
  name text not null,
  password_hash text,
  google_sub text unique,
  phone text,
  preferred_payment text,
  marketing_opt_in integer not null default 0,
  terms_accepted_at text not null,
  created_at text not null
);
create table if not exists addresses (
  id bigint generated always as identity primary key,
  customer_id bigint not null references customers(id) on delete cascade,
  label text not null,
  address text not null,
  city text not null,
  is_default integer not null default 0
);
create table if not exists customer_log (
  id bigint generated always as identity primary key,
  customer_id bigint not null references customers(id) on delete cascade,
  staff_username text not null,
  action text not null,
  created_at text not null
);
alter table orders add column if not exists customer_id bigint references customers(id) on delete set null;

-- Securitate: tabelele cu date personale si parole nu au nicio regula de acces pentru cheia publica.
-- Doar site-ul (prin conexiunea serverului) le poate citi si scrie.
alter table users enable row level security;
alter table customers enable row level security;
alter table addresses enable row level security;
alter table customer_log enable row level security;
