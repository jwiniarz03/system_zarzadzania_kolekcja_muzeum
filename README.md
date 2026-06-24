# System zarządzania kolekcją muzeum

Projekt bazodanowy prezentujący kompleksowy proces modelowania, tworzenia i zarządzania relacyjną bazą danych. Aplikacja wspiera zarządzanie ewidencją dzieł sztuki, śledzenie historii lokalizacji oraz egzekwowanie skomplikowanych reguł biznesowych bezpośrednio na poziomie silnika bazy danych.


## Kluczowe funkcjonalności

- Architektura Danych (ERD): Zaprojektowanie zoptymalizowanego modelu relacyjnego (Entity-Relationship Diagram) obsługującego eksponaty, twórców, historie lokalizacji oraz instytucje wypożyczające.
- Zaawansowany SQL i Procedury Składowane: Implementacja złożonej logiki biznesowej za pomocą zapytań i procedur bezpośrednio w systemie PostgreSQL.
- Integracja Danych i Restrykcje (Constraints/Triggers): Ochrona spójności bazy poprzez twarde reguły walidacyjne. System automatycznie blokuje operacje niezgodne z polityką muzeum (m.in. zakaz wypożyczania eksponatu na więcej niż 30 dni w roku, wymóg pozostawienia min. jednego dzieła danego artysty w zasobach).
- Aplikacja Webowa (CRUD): Interfejs przeglądarkowy pozwalający na łatwe dodawanie, edytowanie i zaawansowane przeszukiwanie zasobów, z uwzględnieniem podziału na widok publiczny (zwiedzający) oraz administracyjny (pracownicy).

1. Dodawanie i edytowanie:
- Eksponatów (kod, tytuł, typ, rozmiar, twórca)
- Artystów (ID, imię, nazwisko, lata życia)
- Lokalizacji eksponatu (galeria/sala, magazyn, wypożyczenie)
- Instytucji wypożyczających

2. Przeszukiwanie (dla pracowników i zwiedzających):
- Lista dzieł danego artysty aktualnie dostępnych na wystawie
- Sprawdzanie historii lokalizacji eksponatu
- Informacje o możliwych wypożyczeniach

3. Walidacje:
- Maksymalnie 30 dni wypożyczenia rocznie / eksponat
- Każdy artysta musi mieć co najmniej 1 dzieło w muzeum


## Technologie

- Baza Danych i Logika: PostgreSQL, zaawansowany SQL, procedury składowane, modelowanie ERD
- Warstwa Aplikacyjna (Backend / Frontend): PHP, HTML


## Ograniczenia i rozwój

Obecnie aplikacja bazodanowa działa w środowisku demonstracyjnym. Sekcja administracyjna (zarządzanie eksponatami i wypożyczeniami) zabezpieczona jest podstawowym modułem logowania pracownika.
Kierunki dalszego rozwoju architektury obejmują:
- Rozbudowę systemu zarządzania uprawnieniami (Role-Based Access Control) na poziomie bazy danych.
- Zaimplementowanie zautomatyzowanego modułu do generowania statystyk i analitycznych raportów z wypożyczeń (np. w postaci hurtowni danych).
