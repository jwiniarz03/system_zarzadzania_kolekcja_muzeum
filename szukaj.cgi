#!/usr/bin/php
<?php
echo ("Content-type: text/html\n\n");
ini_set('display_errors', 1);
error_reporting(E_ALL);
?>

<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>Oficjalna strona muzeum sztuki</title>
</head>

<body>

    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'GET') {
        parse_str($_SERVER["QUERY_STRING"], $form_data);

        $tytul = $form_data["tytul"];

        $link = pg_connect("host=lkdb dbname=mrbd user=ti392 password=bjulkadkulka");

        if (!$link) {
            die("Nie udało się połączyć z bazą danych.");
        }

        $query = "SELECT e.tytul, e.typ, e.wysokosc, e.szerokosc, e.waga, a.imie || ' ' || a.nazwisko AS autor, 
              COALESCE(g.nazwa || ', Sala nr: ' || hw.nr_sali, i.nazwa, 'Eksponat obecnie nie jest dostępny do oglądania') AS aktualna_lokalizacja
              FROM eksponat e
              LEFT JOIN artysta a ON e.artysta_id = a.id
              LEFT JOIN historia_wystaw hw ON e.id = hw.eksponat_id AND hw.data_zakonczenia IS NULL
              LEFT JOIN galeria g ON hw.galeria_identyfikator = g.identyfikator
              LEFT JOIN historia_magazynowania hm ON e.id = hm.eksponat_id AND hm.data_zakonczenia IS NULL
              LEFT JOIN magazyn m ON hm.magazyn_identyfikator = m.identyfikator
              LEFT JOIN historia_wypozyczen hwyp ON e.id = hwyp.eksponat_id AND hwyp.data_zwrotu IS NULL
              LEFT JOIN instytucja i ON hwyp.instytucja_identyfikator = i.identyfikator
              WHERE e.tytul ILIKE $1";
        $result = pg_query_params($link, $query, ['%' . $tytul . '%']);

        if (pg_num_rows($result) > 0) {
            while ($row = pg_fetch_assoc($result)) {
                echo "<p><strong>Tytuł:</strong> " . $row['tytul'] . "</p>";
                echo "<p><strong>Autor:</strong> " . $row['autor'] . "</p>";
                echo "<p><strong>Typ:</strong> " . $row['typ'] . "</p>";
                echo "<p><strong>Wymiary:</strong> " . $row['wysokosc'] . " x " . $row['szerokosc'] . "</p>";
                echo "<p><strong>Waga:</strong> " . $row['waga'] . " kg</p>";
                echo "<p><strong>Aktualna Lokalizacja:</strong> " . $row['aktualna_lokalizacja'] . "</p>";
                echo "<hr>";
            }
        } else {
            echo "<p>Nie znaleziono informacji o eksponacie.</p>";
        }

        pg_close($link);
    }
    ?>

</body>

</html>