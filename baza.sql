drop table if exists artysta;

drop table if exists eksponat;

drop table if exists galeria;

drop table if exists historia_magazynowania;

drop table if exists historia_wypozyczen;

drop table if exists historia_wystaw;

drop table if exists instytucja;

drop table if exists magazyn;

-- Table: Artysta
create table artysta (
   id            integer primary key,
   imie          varchar(20) not null,
   nazwisko      varchar(30) not null,
   rok_urodzenia integer check ( rok_urodzenia > 0 ) not null,
   rok_smierci   integer check ( rok_smierci > 0 )
);

-- Table: Eksponat
create table eksponat (
   id                integer primary key,
   tytul             varchar(50),
   typ               varchar(30) not null,
   wysokosc          numeric(10,3) check ( wysokosc > 0 ) not null,
   szerokosc         numeric(10,3) check ( szerokosc > 0 ) not null,
   waga              numeric(10,3) check ( waga > 0 ) not null,
   czy_najcenniejszy boolean default false not null,
   artysta_id        integer
      references artysta
);

-- Table: Galeria
create table galeria (
   identyfikator integer primary key,
   nazwa         varchar(50) not null,
   miasto        varchar(40) not null
);

-- Table: Instytucja
create table instytucja (
   identyfikator integer primary key not null,
   nazwa         varchar(50) not null,
   miasto        varchar(40) not null
);

-- Table: Magazyn
create table magazyn (
   identyfikator integer primary key not null,
   miasto        varchar(40) not null
);

-- Table: Historia_magazynowania
create table historia_magazynowania (
   id                    serial primary key,
   data_rozpoczecia      date not null,
   data_zakonczenia      date null,
   cel                   varchar(40) not null,
   magazyn_identyfikator integer not null
      references magazyn,
   eksponat_id           integer not null
      references eksponat
);

-- Table: Historia_wypozyczen
create table historia_wypozyczen (
   id                       serial primary key,
   data_wypozyczenia        date not null,
   data_zwrotu              date,
   eksponat_id              integer not null
      references eksponat,
   instytucja_identyfikator integer not null
      references instytucja
);

-- Table: Historia_wystaw
create table historia_wystaw (
   id                    serial primary key,
   data_rozpoczecia      date not null,
   data_zakonczenia      date,
   nr_sali               integer not null,
   eksponat_id           integer not null
      references eksponat,
   galeria_identyfikator integer not null
      references galeria
);


-- zmien lokalizacje eksponatu
create or replace function zmien_lokalizacje_eksponatu (
   p_eksponat_id integer,
   p_aktualne_miejsce varchar,
   p_docelowe_miejsce varchar,
   p_parametry_dodatkowe jsonb
)
returns void as $$
begin
   if p_aktualne_miejsce = 'magazyn' then
      if not exists (
         select 1
         from historia_magazynowania
         where eksponat_id = p_eksponat_id 
         and data_zakonczenia is null 
         and magazyn_identyfikator = (p_parametry_dodatkowe->>'magazyn_identyfikator')::integer) then
         raise exception 'W magazynie nr % nie znajduje sie eksponat %.', p_parametry_dodatkowe->>'magazyn_identyfikator', p_eksponat_id;
      end if;
      update historia_magazynowania
      set data_zakonczenia = CURRENT_DATE
      where eksponat_id = p_eksponat_id and data_zakonczenia is null;
   elsif p_aktualne_miejsce = 'instytucja' then
      if not exists (
            select 1
            from historia_wypozyczen
            where eksponat_id = p_eksponat_id 
            and instytucja_identyfikator = (p_parametry_dodatkowe->>'instytucja_identyfikator')::integer
            and data_zakonczenia is null) then
            raise exception 'W instytucji nr % nie znajduje sie eksponat %.', (p_parametry_dodatkowe->>'instytucja_identyfikator')::integer, p_eksponat_id;
         end if;
      update historia_wypozyczen
      set data_zwrotu = CURRENT_DATE
      where eksponat_id = p_eksponat_id and data_zwrotu is null;
   elsif p_aktualne_miejsce = 'galeria' then
      if not exists (
            select 1
            from historia_wystaw
            where eksponat_id = p_eksponat_id 
            and galeria_identyfikator = (p_parametry_dodatkowe->>'galeria_identyfikator')::integer
            and data_zakonczenia is null) then
            raise exception 'W galerii nr % nie znajduje sie eksponat %.', (p_parametry_dodatkowe->>'galeria_identyfikator')::integer, p_eksponat_id;
         end if;
      update historia_wystaw 
      set data_rozpoczecia = CURRENT_DATE
      where eksponat_id = p_eksponat_id and data_zakonczenia is null;
   else
      raise exception 'Nieznane aktualne miejsce przebywania eksponatu %.', p_aktualne_miejsce;
   end if;

   if p_docelowe_miejsce = 'magazyn' then
      insert into historia_magazynowania (
         data_rozpoczecia,
         cel,
         magazyn_identyfikator,
         eksponat_id
      )
      values (
         CURRENT_DATE,
         p_parametry_dodatkowe->>'cel',
         (p_parametry_dodatkowe->>'magazyn_identyfikator')::integer,
         p_eksponat_id
      );
   elsif p_docelowe_miejsce = 'instytucja' then
      insert into historia_wypozyczen (
         data_wypozyczenia,
         eksponat_id,
         instytucja_identyfikator
      )
      values (
         CURRENT_DATE,
         p_eksponat_id,
         (p_parametry_dodatkowe->>'instytucja_identyfikator')::integer
      );
   elsif p_docelowe_miejsce = 'galeria' then
      insert into historia_wystaw (
         data_rozpoczecia,
         nr_sali,
         eksponat_id,
         galeria_identyfikator
      )
      values (
         CURRENT_DATE,
         (p_parametry_dodatkowe->>'nr_sali')::integer,
         p_eksponat_id,
         (p_parametry_dodatkowe->>'galeria_identyfikator')::integer
      );
   else
      raise exception 'Nieznane miejsce docelowe %.', p_docelowe_miejsce;
   end if;
end;
$$ language 'plpgsql';


-- czy najcenniejszy - nie wypozyczamy
create or replace function sprawdz_czy_najcenniejszy()
returns trigger as $$
begin
   if exists(
      select 1
      from eksponat e
      where e.id = new.eksponat_id
         and e.czy_najcenniejszy
   ) then raise exception 'Nie mozna wypozyczyc najcenniejszego dziela.';
   end if;

   return new;

end;
$$ language 'plpgsql';


-- 30 dniowy limit wypozyczen
create or replace function sprawdz_30_dni () 
returns trigger as $$ 
DECLARE 
    suma INTEGER :=0;
begin
    select sum(DATE_PART('day', COALESCE(data_zwrotu, CURRENT_DATE) - data_wypozyczenia))
    into suma
    from historia_wypozyczen
    where eksponat_id = new.eksponat_id
      and DATE_PART('year', data_wypozyczenia) = DATE_PART('year', NEW.data_wypozyczenia);

    if suma > 30 then RAISE EXCEPTION 'Eksponat nie moze byc poza muzeum dłuzej niz 30 dni rocznie.';
    end IF;

    return new;
end;
$$ language 'plpgsql';

-- conajmniej 1 eksponat kazdego artysty
create or replace function sprawdz_eskponaty_artysty_przed_wypozyczeniem ()
returns trigger as $$
declare 
   liczba_eksponatow INTEGER;
begin
   select COUNT(*) 
   into liczba_eksponatow
   from eksponat e
   where e.artysta_id = OLD.artysta_id
      and id not in (
         select eksponat_id from historia_wypozyczen 
         where data_zwrotu is null
      )
      and (
         exists (
            select 1
            from historia_magazynowania
            where eksponat_id = e.id
               and data_zakonczenia is null
         ) or exists (
            select 1 
            from historia_wystaw
            where eksponat_id = e.id
               and data_zakonczenia is null
         )
      );
   
   if liczba_eksponatow = 1 then raise exception 'Nie mozna wypozyczyc ostatniego dziela artysty.';
   end if;

   return new;
end;
$$ language 'plpgsql';

-- sprawdzanie, czy istnieja dziela artysty - jesli nie to usuwamy
create or replace function sprawdz_dziela_artysty()
returns trigger as $$
declare 
   liczba_eksponatow INTEGER
begin
   select COUNT(*) 
   into liczba_eksponatow
   from eksponat e
   where e.artysta_id = OLD.artysta_id;

   if liczba_eksponatow = 0 then
      delete from artysta 
         where id = OLD.artysta_id;
   end if;

   return old;
end;
$$ language 'plpgsql';



-- wyzwalacz limit wypozyczen
create or replace trigger sprawdz_30_dni_trigger
    BEFORE insert or update on historia_wypozyczen
    for each row
    execute procedure sprawdz_30_dni();

-- wyzwalacz conajmniej 1 eksponat kazdego artsyty
create or replace trigger sprawdz_eskponaty_artysty_przed_wypozyczeniem_trigger
   before insert or update on historia_wypozyczen
   for each row
   execute procedure sprawdz_eskponaty_artysty_przed_wypozyczeniem();

-- wyzwalacz usun artyste gdy nie ma juz jego dziel w muzeum
create or replace trigger sprawdz_dziela_artysty_trigger
   after delete on eksponat
   for each row
   execute procedure sprawdz_dziela_artysty();

-- wyzwalacz sprawdz czy najcenniejszy
create or replace trigger sprawdz_czy_najcenniejszy_trigger
   before insert on historia_wypozyczen
   for each ROW
   execute procedure sprawdz_czy_najcenniejszy();