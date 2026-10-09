-- Déclic — schéma Supabase (production). Le mode démo utilise localStorage ; pour passer en prod,
-- remplacer les lectures/écritures de js/store.js par des appels supabase-js sur ces tables.
create table profiles (
  id uuid primary key references auth.users on delete cascade,
  role text not null check (role in ('coach','client')) default 'client',
  prenom text, nom text, phone text, created_at timestamptz default now()
);
create table clients (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users,
  prenom text not null, nom text, email text unique not null, phone text, source text,
  stage text not null default 'decouverte', offer_id text, score int,
  done jsonb not null default '{}', answers jsonb not null default '{}', unlocked text[] not null default '{}',
  signed jsonb, pay_pending boolean default false, lost boolean default false,
  referrer text, ref_code text unique, last_activity timestamptz default now(), created_at timestamptz default now()
);
create table sessions (
  id uuid primary key default gen_random_uuid(), client_id uuid references clients on delete cascade,
  n int not null, theme text, minutes int, state text default 'locked', date timestamptz, notes text,
  exo_done int[] default '{}', exo_unlocked boolean default false, done_at timestamptz, unique (client_id, n)
);
create table appointments (id uuid primary key default gen_random_uuid(), client_id uuid references clients on delete cascade, kind text, date timestamptz unique, label text);
create table invoices (
  id uuid primary key default gen_random_uuid(), number text unique not null, client_id uuid references clients on delete cascade,
  label text, amount numeric(10,2) not null, status text default 'due', issued_at timestamptz default now(), due_at timestamptz, paid_at timestamptz
);
create table outbox (
  id uuid primary key default gen_random_uuid(), client_id uuid references clients on delete cascade, key text, to_email text,
  subject text, body text, send_at timestamptz, status text default 'scheduled', unless_done text, sent_at timestamptz
);
create table activity (id uuid primary key default gen_random_uuid(), client_id uuid, text text, kind text, t timestamptz default now());

create or replace function is_coach() returns boolean language sql stable security definer as
$$ select exists (select 1 from profiles where id = auth.uid() and role = 'coach') $$;

alter table profiles enable row level security; alter table clients enable row level security; alter table sessions enable row level security;
alter table appointments enable row level security; alter table invoices enable row level security; alter table outbox enable row level security; alter table activity enable row level security;

create policy coach_all_clients on clients for all using (is_coach()) with check (is_coach());
create policy own_client on clients for select using (user_id = auth.uid());
create policy own_client_upd on clients for update using (user_id = auth.uid());
create policy coach_all_sessions on sessions for all using (is_coach()) with check (is_coach());
create policy own_sessions on sessions for select using (client_id in (select id from clients where user_id = auth.uid()));
create policy coach_all_appts on appointments for all using (is_coach()) with check (is_coach());
create policy own_appts on appointments for all using (client_id in (select id from clients where user_id = auth.uid()));
create policy coach_all_inv on invoices for all using (is_coach()) with check (is_coach());
create policy own_inv on invoices for select using (client_id in (select id from clients where user_id = auth.uid()));
create policy coach_outbox on outbox for all using (is_coach()) with check (is_coach());
create policy coach_activity on activity for all using (is_coach()) with check (is_coach());
create policy own_profile on profiles for select using (id = auth.uid() or is_coach());
