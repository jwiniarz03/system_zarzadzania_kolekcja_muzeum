#!/usr/bin/php
<?php echo ("Content-type: text/html\n\n");
?>

<html>

<head>
    <title>Oficjalna strona muzeum sztuki</title>
    <meta charset="utf-8">
</head>

<body>

    <?php
    function displayHistory($eksponat_id, $type, $link)
    {
        $queries = [
            'wystaw' => "SELECT * FROM historia_wystaw WHERE eksponat_id = $1",
            'magazynowania' => "SELECT * FROM historia_magazynowania WHERE eksponat_id = $1",
            'wypozyczen' => "SELECT * FROM historia_wypozyczen WHERE eksponat_id = $1"
        ];
        $result = pg_query_params($link, $queries[$type], [$eksponat_id]);
        if ($type === 'wystaw') {
            echo "<h3>Historia Wystaw</h3>";
            echo "<table border='1'><tr><th>id</th><th>Data Rozpoczęcia</th><th>Data Zakończenia</th>
                <th>Nr Sali</th><th>Eksponat ID</th><th>Galeria ID</th></tr>";
        } elseif ($type === 'magazynowania') {
            echo "<h3>Historia Magazynowania</h3>";
            echo "<table border='1'><tr><th>id</th><th>Data Rozpoczęcia</th><th>Data Zakończenia</th>
                <th>cel</th><th>Magazyn ID</th><th>Eksponat id</th></tr>";
        } else {
            echo "<h3>Historia Wypożyczeń</h3>";
            echo "<table border='1'><tr><th>id</th><th>Data Wypożyczenia</th><th>Data Zwrotu</th>
                <th>Eksponat ID</th><th>Instytucja ID</th></tr>";
        }
        while ($row = pg_fetch_assoc($result)) {
            echo "<tr>";
            foreach ($row as $value) {
                echo "<td>$value</td>";
            }
            echo "</tr>";
        }
        echo "</table>";
    }
    function displayResults($result, $link)
    {
        if ($result && pg_num_rows($result) > 0) {
            while ($row = pg_fetch_assoc($result)) {
                echo "<h3>Szczegóły Eksponatu</h3>";
                echo "<p>ID Eksponatu: {$row['id']}</p>";
                echo "<p>Tytuł: {$row['tytul']}</p>";
                echo "<p>Typ: {$row['typ']}</p>";
                echo "<p>Wymiary: {$row['wysokosc']} x {$row['szerokosc']}</p>";
                echo "<p>Waga: {$row['waga']}</p>";
                echo "<p>Czy najcenniejszy: " . ($row['czy_najcenniejszy'] ? 'Tak' : 'Nie') . "</p>";
                echo "<p>Autor: {$row['autor']}</p>";
                echo "<p>ID Autora: {$row['autor_id']}</p>";

                displayHistory($row['id'], 'wystaw', $link);

                displayHistory($row['id'], 'magazynowania', $link);

                displayHistory($row['id'], 'wypozyczen', $link);
            }
        } else {
            echo "Nie znaleziono eksponatu.";
        }
    }

    if ($_SERVER['REQUEST_METHOD'] == 'GET') {
        parse_str($_SERVER["QUERY_STRING"], $form_data);

        $action = $form_data["action"] ?? null;

        $link = pg_connect("host=lkdb dbname=mrbd user=ti392 password=bjulkadkulka");
        if (!$link) {
            echo "Nie udało się połączyć z bazą danych!<br>";
            exit;
        }

        if ($action === "dodaj_eksponat") {
            $id_eks = $form_data["id_eks"];
            $tytul = $form_data["tytul"] ?? null;
            $typ = $form_data["typ"];
            $wysokosc = $form_data["wysokosc"];
            $szerokosc = $form_data["szerokosc"];
            $waga = $form_data["waga"];
            $cennosc = isset($form_data["najcenniejszy"]) && $form_data["najcenniejszy"] === "tak" ? 'true' : 'false';
            $id_art = $form_data["id_art"] ?? null;

            if ($id_art !== null) {
                $check_artist_query = "SELECT 1 FROM artysta WHERE id = $1";
                $check_artist_result = pg_query_params($link, $check_artist_query, [$id_art]);

                if (pg_num_rows($check_artist_result) === 0) {
                    echo "Nie można dodać eksponatu, ponieważ artysta o ID {$id_art} nie istnieje.";
                    exit;
                }
            }
            $check_exhibit_query = "SELECT 1 FROM eksponat WHERE id = $1";
            $check_exhibit_result = pg_query_params($link, $check_exhibit_query, [$id_eks]);

            if (pg_num_rows($check_exhibit_result) > 0) {
                echo "Eksponat o ID {$id_eks} już istnieje.";
                exit;
            }

            $query = "INSERT INTO eksponat (id, tytul, typ, wysokosc, szerokosc, waga, czy_najcenniejszy, artysta_id)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)";
            $params = [$id_eks, $tytul, $typ, $wysokosc, $szerokosc, $waga, $cennosc, $id_art];

            $wynik = pg_query_params($link, $query, $params);

            if ($wynik) {
                $cel = 'Przechowywanie';
                $query_historia = "INSERT INTO historia_magazynowania (eksponat_id, magazyn_identyfikator, data_rozpoczecia, cel)
                                   VALUES ($1, 1, CURRENT_DATE, $2)";
                $params_historia = [$id_eks, $cel];

                $wynik_historia = pg_query_params($link, $query_historia, $params_historia);

                if ($wynik_historia) {
                    echo "Eksponat został dodany i umieszczony w magazynie głównym.";
                } else {
                    echo "Eksponat został dodany, ale nie udało się dodać go do magazynu!<br>" . pg_last_error($link);
                }
            } else {
                echo "Nie udało się dodać eksponatu!<br>" . pg_last_error($link);
            }
        } elseif ($action === "dodaj_artyste") {
            $id_arty = $form_data["id_arty"];
            $imie = $form_data["imie"];
            $nazwisko = $form_data["nazwisko"];
            $rok_uro = $form_data["rok_uro"];
            $rok_sm = isset($form_data["rok_sm"]) && $form_data["rok_sm"] !== "" ? $form_data["rok_sm"] : null;

            $check_artist_query = "SELECT 1 FROM artysta WHERE id = $1";
            $check_artist_result = pg_query_params($link, $check_artist_query, [$id_arty]);

            if (pg_num_rows($check_artist_result) > 0) {
                echo "Artysta o ID {$id_arty} już istnieje.";
                exit;
            }
            if ($rok_sm !== null && $rok_sm <= $rok_uro) {
                echo "Rok śmierci musi być większy niż rok urodzenia!";
                exit;
            }

            $query = "INSERT INTO artysta (id, imie, nazwisko, rok_urodzenia, rok_smierci)
                    VALUES ($1, $2, $3, $4, $5)";
            $params = [$id_arty, $imie, $nazwisko, $rok_uro, $rok_sm];

            $wynik = pg_query_params($link, $query, $params);

            if ($wynik) {
                echo "Artysta został dodany pomyślnie.";
            } else {
                echo "Nie udało się dodać artysty!<br>" . pg_last_error($link);
            }
        } elseif ($action === "dodaj_galerie") {
            $id_gal = $form_data["id_gal"];
            $nazwa = $form_data["nazwa"];
            $miasto = $form_data["miasto"];

            $check_gallery_query = "SELECT 1 FROM galeria WHERE identyfikator = $1";
            $check_gallery_result = pg_query_params($link, $check_gallery_query, [$id_gal]);

            if (pg_num_rows($check_gallery_result) > 0) {
                echo "Galeria o identyfikatorze {$id_gal} już istnieje.";
                exit;
            }
            $query = "INSERT INTO galeria (identyfikator, nazwa, miasto)
                    VALUES ($1, $2, $3)";
            $params = [$id_gal, $nazwa, $miasto];

            $wynik = pg_query_params($link, $query, $params);

            if ($wynik) {
                echo "Galeria została dodana pomyślnie.";
            } else {
                echo "Nie udało się dodać galerii!<br>" . pg_last_error($link);
            }
        } elseif ($action === "dodaj_instytucje") {
            $id_inst = $form_data["id_inst"];
            $nazwa = $form_data["nazwa"];
            $miasto = $form_data["miasto"];

            $check_institution_query = "SELECT 1 FROM instytucja WHERE identyfikator = $1";
            $check_institution_result = pg_query_params($link, $check_institution_query, [$id_inst]);

            if (pg_num_rows($check_institution_result) > 0) {
                echo "Instytucja o identyfikatorze {$id_inst} już istnieje.";
                exit;
            }

            $query = "INSERT INTO instytucja (identyfikator, nazwa, miasto)
                      VALUES ($1, $2, $3)";
            $params = [$id_inst, $nazwa, $miasto];

            $wynik = pg_query_params($link, $query, $params);

            if ($wynik) {
                echo "Instytucja została dodana pomyślnie.";
            } else {
                echo "Nie udało się dodać instytucji!<br>" . pg_last_error($link);
            }
        } elseif ($action === "dodaj_magazyn") {
            $id_mag = $form_data["id_mag"];
            $miasto = $form_data["miasto"];

            $check_warehouse_query = "SELECT 1 FROM magazyn WHERE identyfikator = $1";
            $check_warehouse_result = pg_query_params($link, $check_warehouse_query, [$id_mag]);

            if (pg_num_rows($check_warehouse_result) > 0) {
                echo "Magazyn o identyfikatorze {$id_mag} już istnieje.";
                exit;
            }

            $query = "INSERT INTO magazyn (identyfikator, miasto)
                      VALUES ($1, $2)";
            $params = [$id_mag, $miasto];

            $wynik = pg_query_params($link, $query, $params);

            if ($wynik) {
                echo "Magazyn został dodany pomyślnie.";
            } else {
                echo "Nie udało się dodać magazynu!<br>" . pg_last_error($link);
            }
        } elseif ($action === "mag_mag") {
            $id_eks = $form_data['id_eks'];
            $id_mag1 = $form_data['id_mag1'];
            $id_mag2 = $form_data['id_mag2'];
            $cel = $form_data['cel'];

            if ($id_eks && $id_mag1 && $id_mag2 && $cel) {
                $query1 = "UPDATE historia_magazynowania SET data_zakonczenia = CURRENT_DATE WHERE eksponat_id = $1 AND magazyn_identyfikator = $2 AND data_zakonczenia IS NULL";
                $query2 = "INSERT INTO historia_magazynowania (data_rozpoczecia, cel, magazyn_identyfikator, eksponat_id) VALUES (CURRENT_DATE, $1, $2, $3)";

                $result1 = pg_query_params($link, $query1, [$id_eks, $id_mag1]);
                $result2 = pg_query_params($link, $query2, [$cel, $id_mag2, $id_eks]);

                if ($result1 && $result2) {
                    echo "Lokalizacja eksponatu została zmieniona.";
                } else {
                    echo "Nie udało się zmienić lokalizacji eksponatu.";
                }
            } else {
                echo "Brakujące dane do zmiany lokalizacji.";
            }
        } elseif ($action === "mag_gal") {
            $id_eks = $form_data['id_eks'];
            $id_mag = $form_data['id_mag'];
            $id_gal = $form_data['id_gal'];
            $nr_sali = $form_data['nr'];

            if ($id_eks && $id_mag && $id_gal && $nr_sali) {
                $query1 = "UPDATE historia_magazynowania SET data_zakonczenia = CURRENT_DATE WHERE eksponat_id = $1 AND magazyn_identyfikator = $2 AND data_zakonczenia IS NULL";
                $query2 = "INSERT INTO historia_wystaw (data_rozpoczecia, nr_sali, eksponat_id, galeria_identyfikator) VALUES (CURRENT_DATE, $1, $2, $3)";

                $result1 = pg_query_params($link, $query1, [$id_eks, $id_mag]);
                $result2 = pg_query_params($link, $query2, [$nr_sali, $id_eks, $id_gal]);

                if ($result1 && $result2) {
                    echo "Lokalizacja eksponatu została zmieniona.";
                } else {
                    echo "Nie udało się zmienić lokalizacji eksponatu.";
                }
            } else {
                echo "Brakujące dane do zmiany lokalizacji.";
            }
        } elseif ($action === "gal_mag") {
            $id_eks = $form_data['id_eks'];
            $id_gal = $form_data['id_gal'];
            $id_mag = $form_data['id_mag'];
            $cel = $form_data['cel'];

            if ($id_eks && $id_gal && $id_mag && $cel) {
                $query1 = "UPDATE historia_wystaw SET data_zakonczenia = CURRENT_DATE WHERE eksponat_id = $1 AND galeria_identyfikator = $2 AND data_zakonczenia IS NULL";
                $query2 = "INSERT INTO historia_magazynowania (data_rozpoczecia, cel, magazyn_identyfikator, eksponat_id) VALUES (CURRENT_DATE, $1, $2, $3)";

                $result1 = pg_query_params($link, $query1, [$id_eks, $id_gal]);
                $result2 = pg_query_params($link, $query2, [$cel, $id_mag, $id_eks]);

                if ($result1 && $result2) {
                    echo "Lokalizacja eksponatu została zmieniona.";
                } else {
                    echo "Nie udało się zmienić lokalizacji eksponatu.";
                }
            } else {
                echo "Brakujące dane do zmiany lokalizacji.";
            }
        } elseif ($action === "gal_gal") {
            $id_eks = $form_data['id_eks'];
            $id_gal1 = $form_data['id_gal1'];
            $id_gal2 = $form_data['id_gal2'];
            $nr_sali = $form_data['nr'];

            if ($id_eks && $id_gal1 && $id_gal2 && $nr_sali) {
                $query1 = "UPDATE historia_wystaw SET data_zakonczenia = CURRENT_DATE WHERE eksponat_id = $1 AND galeria_identyfikator = $2 AND data_zakonczenia IS NULL";
                $query2 = "INSERT INTO historia_wystaw (data_rozpoczecia, nr_sali, eksponat_id, galeria_identyfikator) VALUES (CURRENT_DATE, $1, $2, $3)";

                $result1 = pg_query_params($link, $query1, [$id_eks, $id_gal1]);
                $result2 = pg_query_params($link, $query2, [$nr_sali, $id_eks, $id_gal2]);

                if ($result1 && $result2) {
                    echo "Lokalizacja eksponatu została zmieniona.";
                } else {
                    echo "Nie udało się zmienić lokalizacji eksponatu.";
                }
            } else {
                echo "Brakujące dane do zmiany lokalizacji.";
            }
        } elseif ($action === "dodaj_wypozyczenie") {
            $eksponat_id = $form_data['eksponat_id'];
            $magazyn_id = $form_data['magazyn'];
            $instytucja_id = $form_data['instytucja'];

            if ($eksponat_id && $magazyn_id && $instytucja_id) {
                $check_institution_query = "SELECT 1 FROM instytucja WHERE identyfikator = $1";
                $check_institution_result = pg_query_params($link, $check_institution_query, [$instytucja_id]);

                if (pg_num_rows($check_institution_result) > 0) {
                    $query1 = "UPDATE historia_magazynowania 
                               SET data_zakonczenia = CURRENT_DATE 
                               WHERE eksponat_id = $1 AND magazyn_identyfikator = $2 AND data_zakonczenia IS NULL";
                    $query2 = "INSERT INTO historia_wypozyczen (data_wypozyczenia, data_zwrotu, eksponat_id, instytucja_identyfikator) 
                               VALUES (CURRENT_DATE, NULL, $1, $2)";

                    $result1 = pg_query_params($link, $query1, [$eksponat_id, $magazyn_id]);
                    $result2 = pg_query_params($link, $query2, [$eksponat_id, $instytucja_id]);

                    if ($result1 && $result2) {
                        echo "Wypożyczenie eksponatu zostało dodane.";
                    } else {
                        echo "Nie udało się dodać wypożyczenia eksponatu.";
                    }
                } else {
                    echo "Instytucja o identyfikatorze {$instytucja_id} nie istnieje w systemie.";
                }
            } else {
                echo "Brakujące dane lub niepoprawna lokalizacja do dodania wypożyczenia.";
            }
        } elseif ($action === "dodaj_zwrot") {
            $eksponat_id = $form_data['eksponat_id'];
            $instytucja = $form_data['instytucja'];
            $magazyn = $form_data['magazyn'];

            if ($eksponat_id && $instytucja && $magazyn) {
                $query1 = "UPDATE historia_wypozyczen SET data_zwrotu = CURRENT_DATE WHERE eksponat_id = $1 AND instytucja_identyfikator = $2 AND data_zwrotu IS NULL";
                $query2 = "INSERT INTO historia_magazynowania (data_rozpoczecia, cel, magazyn_identyfikator, eksponat_id) VALUES (CURRENT_DATE, 'zwrot', $2, $1)";

                $result1 = pg_query_params($link, $query1, [$eksponat_id, $instytucja]);
                $result2 = pg_query_params($link, $query2, [$eksponat_id, $magazyn]);

                if ($result1 && $result2) {
                    echo "Zwrot eksponatu do magazynu został dodany.";
                } else {
                    echo "Nie udało się dodać zwrotu eksponatu do magazynu.";
                }
            } else {
                echo "Brakujące dane lub niepoprawna lokalizacja do dodania zwrotu.";
            }
        }
        if ($action === "szukaj_po_id") {
            $id = $form_data['id'] ?? null;
            if (!empty($id)) {
                $query = "SELECT e.id, e.tytul, e.typ, e.wysokosc, e.szerokosc, e.waga, 
                          e.czy_najcenniejszy, a.id AS autor_id, a.imie || ' ' || a.nazwisko AS autor
                          FROM eksponat e
                          LEFT JOIN artysta a ON e.artysta_id = a.id
                          WHERE e.id = $1";
                $result = pg_query_params($link, $query, [$id]);

                if ($result) {
                    displayResults($result, $link);
                } else {
                    echo "Błąd zapytania: " . pg_last_error($link);
                }
            } else {
                echo "Nie podano ID.";
            }
        } elseif ($action === "szukaj_po_tytule") {
            $tytul = $form_data['tytul'];
            if (!empty($tytul)) {
                $query = "SELECT e.id, e.tytul, e.typ, e.wysokosc, e.szerokosc, e.waga, 
                            e.czy_najcenniejszy, a.id AS autor_id, a.imie || ' ' || a.nazwisko AS autor
                            FROM eksponat e
                            LEFT JOIN artysta a ON e.artysta_id = a.id
                            WHERE LOWER(e.tytul) = LOWER($1)";
                $result = pg_query_params($link, $query, [$tytul]);
                displayResults($result, $link);
            } else {
                echo "Nie podano tytułu.";
            }
        } elseif ($action === "szukaj_po_autorze") {
            $autor = $form_data['autor'];
            if (!empty($autor)) {
                $query = "SELECT e.id, e.tytul, e.typ, e.wysokosc, e.szerokosc, e.waga, 
                            e.czy_najcenniejszy, a.id AS autor_id, a.imie || ' ' || a.nazwisko AS autor
                            FROM eksponat e
                            LEFT JOIN artysta a ON e.artysta_id = a.id
                            WHERE LOWER(a.imie || ' ' || a.nazwisko) = LOWER($1)";
                $result = pg_query_params($link, $query, [$autor]);
                displayResults($result, $link);
            } else {
                echo "Nie podano autora.";
            }
        }

        pg_close($link);
    }
    ?>

</body>

</html>