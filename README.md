# System zarządzania kolekcją muzeum

Author: Julia Winiarz

Aplikacja wspierająca zarządzanie kolekcją muzeum sztuki – umożliwia rejestrowanie, lokalizowanie, wypożyczanie oraz przeszukiwanie eksponatów i artystów. 
Projekt wykonany w ramach zaliczenia przedmiotu "Bazy Danych i Usługi Sieciowe" na Uniwersytecie Warszawskim.


## Cel projektu

Celem było stworzenie systemu wspomagającego ewidencję dzieł sztuki (obrazów, rzeźb itp.) w muzeum. System obsługuje:

- Wprowadzanie eksponatów, artystów, galerii i wypożyczeń.
- Śledzenie lokalizacji i historii eksponatów.
- Przestrzeganie ograniczeń (maks. 30 dni poza muzeum / eksponat, min. 1 dzieło każdego artysty w muzeum).
- Udostępnianie publicznego podglądu dostępnych eksponatów (bez informacji historycznych).
- Obsługę przez przeglądarkę internetową.


## Technologie

- PosgreSQL:  baza danych + procedury składowane
- ERD: model związków encji (Entity-Relationship Diagram)
- PHP – język strony internetowej
- HTML – interfejs użytkownika (frontend strony internetowej)


## Funkcjonalności

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


## Ograniczenia i rozwój

Projekt powstał jako praca zaliczeniowa i zawiera system logowania, jednak obecnie dostęp do sekcji pracownika jest możliwy tylko przy użyciu jednego, stałego loginu i hasła.

W przyszłości możliwe rozszerzenia:
- Rozbudowana kontrola uprawnień i system zarządzania użytkownikami.
- Integracja z rzeczywistymi zasobami muzeów.
- Generowanie statystyk i raportów.
