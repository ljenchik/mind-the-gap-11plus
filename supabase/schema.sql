-- Mind the Gap 11+ : the small database (Supabase / Postgres)
-- Paste all of this into Supabase → SQL Editor → New query → Run.
-- Three tables:
--   family   one row per parent account: the saved progress of all their children
--   access   what the parent has paid for (written only by the Stripe webhook)
--   qstats   anonymous counts per question: how often it is answered, missed and reported

create table if not exists public.family (
  user_id    uuid primary key references auth.users (id) on delete cascade,
  data       jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

create table if not exists public.access (
  user_id            uuid primary key references auth.users (id) on delete cascade,
  plan               text not null,            -- 'monthly' or 'until-test'
  until              timestamptz not null,     -- full access ends after this time
  stripe_customer    text,
  stripe_subscription text,
  updated_at         timestamptz not null default now()
);

create table if not exists public.qstats (
  qid      text primary key,
  seen     integer not null default 0,
  wrong    integer not null default 0,
  reports  integer not null default 0,
  updated_at timestamptz not null default now()
);

-- Row-level security: a parent can only ever see and change their own row.
alter table public.family enable row level security;
alter table public.access enable row level security;
alter table public.qstats enable row level security;

drop policy if exists "own family read"   on public.family;
drop policy if exists "own family insert" on public.family;
drop policy if exists "own family update" on public.family;
drop policy if exists "own family delete" on public.family;
create policy "own family read"   on public.family for select using (auth.uid() = user_id);
create policy "own family insert" on public.family for insert with check (auth.uid() = user_id);
create policy "own family update" on public.family for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "own family delete" on public.family for delete using (auth.uid() = user_id);

-- access: parents may read their own row; only the webhook (service key) writes.
drop policy if exists "own access read" on public.access;
create policy "own access read" on public.access for select using (auth.uid() = user_id);

-- qstats: nobody reads or writes it directly; the app only calls bump_questions below.
-- You read it yourself in the Supabase table editor (sort by wrong / seen).

create or replace function public.bump_questions(items jsonb)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare it jsonb;
begin
  if jsonb_typeof(items) <> 'array' or jsonb_array_length(items) > 100 then return; end if;
  for it in select * from jsonb_array_elements(items) loop
    if length(coalesce(it->>'qid', '')) between 1 and 40 then
      insert into qstats (qid, seen, wrong, reports)
      values (it->>'qid',
              case when (it->>'report')::boolean then 0 else 1 end,
              case when (it->>'wrong')::boolean then 1 else 0 end,
              case when (it->>'report')::boolean then 1 else 0 end)
      on conflict (qid) do update set
        seen = qstats.seen + excluded.seen,
        wrong = qstats.wrong + excluded.wrong,
        reports = qstats.reports + excluded.reports,
        updated_at = now();
    end if;
  end loop;
end $$;

revoke all on function public.bump_questions(jsonb) from public;
grant execute on function public.bump_questions(jsonb) to anon, authenticated;

-- Handy view for you: questions most children miss (at least 20 tries).
create or replace view public.hardest_questions as
  select qid, seen, wrong, reports, round(100.0 * wrong / nullif(seen, 0)) as pct_wrong
  from qstats where seen >= 20 or reports > 0
  order by reports desc, pct_wrong desc nulls last;
revoke all on public.hardest_questions from anon, authenticated;
