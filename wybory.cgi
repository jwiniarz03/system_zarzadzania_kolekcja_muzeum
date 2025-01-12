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
    <title>Strona główna muzeum sztuki</title>
</head>

<body>
    <?php
    if ($_SERVER['REQUEST_METHOD'] == 'GET') {
        parse_str($_SERVER["QUERY_STRING"], $form_data);

        if (isset($form_data['akcja'])) {
            $wybor = $form_data['akcja'];

            if ($wybor === 'wprowadzanie_info') {
                echo '<h3> O czym chcesz wprowadzić informacje? <h3>';
                echo '<form action="wprowadzanie.cgi" method="GET">
                    <p> Wybierz 1 opcję. </p>
                    <input type="radio" name="wybor" value="wpr_eksponat"> o eksponacie <br>
                    <input type="radio" name="wybor" value="wpr_artysta"> o artyscie <br>
                    <input type="radio" name="wybor" value="wpr_galeria"> o galerii <br><br>
                    <input type="submit" name="enter" value="Przejdź dalej">
                </form>';
            } elseif ($wybor === 'zmiana_lokalizacji') {
                echo '<h3>Podaj szczegoly zmiany lokalizacji eksponatu:</h3>';
                echo '<form action="zmiana_lokalizacji_formularz.cgi" method="GET">
                    <p>ID eksponatu: <input type="number" name="eksponat_id" required></p>
                    <p> Aktualne miejsce: </p>
                    <select name="aktualne_miejsce" required>
                        <option> Magazyn
                        <option> Galeria
                        <option> Instytucja
                    </select>
                    <p> Docelowe miejsce: </p>
                    <select name="docelowe_miejsce" required>
                        <option> Magazyn
                        <option> Galeria
                        <option> Instytucja
                    </select><br><br>
                    <input type="submit" value="Przejdź dalej">
                </form>';
            } elseif ($wybor === 'wprowadzanie_wypozyczen') {
                echo '<h3>Wybierz co chcesz zrobić i podaj szczegoly:</h3>';
                echo '<form action="wypozyczenie.cgi" method="GET">
                    <input type="radio" name="cel" value="wypozyczenie"> Wypozycz<br>
                    <input type="radio" name="cel" value="zwrot"> Zwroc<br>
                    <p>ID eksponatu: <input type="number" name="eksponat_id" required></p>
                    <p>Identyfikator instytucji: <input type="number" name="eksponat_id" required></p><br>
                    <input type="submit" value="Potwierdź">
                </form>';
            } elseif ($wybor === 'przeszukiwanie_historia') {
                echo '<p>Tu coś będzie w przyszłości :</p>';
            }
        }
    } else {
        echo "<h3>Wybierz co chcesz dzisiaj zrobić:</h3>";
        echo '<form action="wybory.cgi" method="GET">
                        <input type="radio" name="akcja" value="wprowadzanie_info"> Wprowadzanie informacji 
                        o eksponatach, artystach i galeriach<br>
                        <input type="radio" name="akcja" value="zmiana_lokalizacji">Zmienianie informacji 
                        o polozeniu eksponatow<br>
                        <input type="radio" name="akcja" value="wprowadzanie_wypozyczen">Wprowadzanie informacji 
                        o wypozyczeniach<br>
                        <input type="radio" name="akcja" value="przeszukiwanie_historia">Przeszukiwanie 
                        zgromadzonych informacji<br><br>
                        <input type="submit" value="Przejdź dalej">
                    </form>';
    }
    ?>