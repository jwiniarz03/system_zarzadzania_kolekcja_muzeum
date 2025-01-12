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
    if ($_SERVER['REQUEST_METHOD'] == 'GET') {
        parse_str($_SERVER["QUERY_STRING"], $form_data);

        if (isset($form_data['nazwa']) && ($form_data['haslo'])) {
            $login = $form_data['nazwa'];
            $password = $form_data['haslo'];

            $correct_login = "fajnanazwa";
            $correct_password = "tajnehaslouuu";

            if ($login == $correct_login && $password == $correct_password) {
                echo "<h2>Zalogowano pomyślnie!</h2>";
                echo "<h2>Witaj w sekcji pracowników muzeum!</h2><br><br>";
                echo "<h3>Wprowadzanie informacji o eksponatach: </h3>";
                echo "<h4>UWAGA! Jeśli dodajesz eksponat nowego artysty, 
                    musisz najpierw dodać artystę, a dopiero poźniej jego eksponat!!</h4>";
                echo '<form action="akcje.cgi" method="GET">
                    <input type="hidden" name="action" value="dodaj_eksponat">
                    id eksponatu: <input type="number" name="id_eks" min="1" required><br>
                    <br>
                    tytuł: <input type="text" name="tytul" maxlength="50" required><br>
                    <br>
                    typ: <input type="text" name="typ" maxlength="30" required><br>
                    <br>
                    wysokość (w cm): <input type="number" name="wysokosc" step="0.001" min="0" required><br>
                    <br>
                    szerokość (w cm): <input type="number" name="szerokosc" step="0.001" min="0" required><br>
                    <br>
                    waga: <input type="number" name="waga" step="0.001" min="0" required><br>
                    <br>
                    najcenniejszy: 
                    <input type=radio name="najcenniejszy" value="tak"> tak  
                    <input type=radio name="najcenniejszy" value="nie" checked> nie<br>
                    <br>
                    id artysty: <input type="number" name="id_art" min="1"><br>
                    <br>
                    <input type=submit value="Dodaj"><br><br>
                </form>';

                echo "<h3>Wprowadzanie informacji o artystach: </h3>";
                echo '<form action="akcje.cgi" method="GET">
                    <input type="hidden" name="action" value="dodaj_artyste">
                    id artysty: <input type="number" name="id_arty" min="1" required><br>
                    <br>
                    imię: <input type="text" name="imie" maxlength="20" required><br>
                    <br>
                    nazwisko: <input type="text" name="nazwisko" maxlength="30" required><br>
                    <br>
                    rok urodzenia: <input type="number" name="rok_uro" min="0" required><br>
                    <br>
                    rok śmierci: <input type="number" name="rok_sm" min="0"><br>
                    <br>
                    <input type=submit value="Dodaj"><br><br>
                </form>';

                echo "<h3>Wprowadzanie informacji o galeriach: </h3>";
                echo '<form action="akcje.cgi" method="GET">
                    <input type="hidden" name="action" value="dodaj_galerie">
                    identyfikator galerii: <input type="number" name="id_gal" min="1" required><br>
                    <br>
                    nazwa: <input type="text" name="nazwa" maxlength="50" required><br>
                    <br>
                    miasto: <input type="text" name="miasto" maxlength="40" required><br>
                    <br>
                    <input type=submit value="Dodaj"><br><br><br>
                </form>';

                echo "<h3>Wprowadzanie informacji o magazynach: </h3>";
                echo '<form action="akcje.cgi" method="GET">
                    <input type="hidden" name="action" value="dodaj_magazyn">
                    identyfikator magazynu: <input type="number" name="id_mag" min="1" required><br>
                    <br>
                    miasto: <input type="text" name="miasto" maxlength="40" required><br>
                    <br>
                    <input type=submit value="Dodaj"><br><br><br>
                </form>';

                echo "<h3>Wprowadzanie informacji o instytucjach: </h3>";
                echo '<form action="akcje.cgi" method="GET">
                    <input type="hidden" name="action" value="dodaj_instytucje">
                    identyfikator instytucji: <input type="number" name="id_inst" min="1" required><br>
                    <br>
                    nazwa: <input type="text" name="nazwa" maxlength="50" required><br>
                    <br>
                    miasto: <input type="text" name="miasto" maxlength="40" required><br>
                    <br>
                    <input type=submit value="Dodaj"><br><br><br>
                </form>';


                echo "<h3>Zmienianie informacji o połozeniu eksponatów: </h3>";

                echo "<h4>z magazynu do magazynu</h4>";
                echo '<form action="akcje.cgi" method="GET">
                    <input type="hidden" name="action" value="mag_mag">
                    id eksponatu: <input type="number" name="id_eks" min="1" required><br>
                    <br>
                    id aktualnego magazynu: <input type="number" name="id_mag1" min="1" required><br>
                    <br>
                    id docelowego magazynu: <input type="number" name="id_mag2" min="1" required><br>
                    <br>
                    cel magazynowania: <input type="text" name="cel" maxlength="40" required><br>
                    <br>
                    <input type=submit value="Dodaj"><br><br>
                </form>';

                echo "<h4>z magazynu do galerii</h4>";
                echo '<form action="akcje.cgi" method="GET">
                    <input type="hidden" name="action" value="mag_gal">
                    id eksponatu: <input type="number" name="id_eks" min="1" required><br>
                    <br>
                    id aktualnego magazynu: <input type="number" name="id_mag" min="1" required><br>
                    <br>
                    id docelowej galerii: <input type="number" name="id_gal" min="1" required><br>
                    <br>
                    nr sali: <input type="number" name="nr" required><br>
                    <br>
                    <input type=submit value="Dodaj"><br><br>
                </form>';

                echo "<h4>z galerii do magazynu</h4>";
                echo '<form action="akcje.cgi" method="GET">
                    <input type="hidden" name="action" value="gal_mag">
                    id eksponatu: <input type="number" name="id_eks" min="1" required><br>
                    <br>
                    id aktualnej galerii: <input type="number" name="id_gal" min="1" required><br>
                    <br>
                    id docelowego magazynu: <input type="number" name="id_mag" min="1" required><br>
                    <br>
                    cel magazynowania: <input type="text" name="cel" maxlength="40" required><br>
                    <br>
                    <input type=submit value="Dodaj"><br><br>
                </form>';

                echo "<h4>z galerii do galerii</h4>";
                echo '<form action="akcje.cgi" method="GET">
                    <input type="hidden" name="action" value="gal_gal">
                    id eksponatu: <input type="number" name="id_eks" min="1" required><br>
                    <br>
                    id aktualnej galerii: <input type="number" name="id_gal1" min="1" required><br>
                    <br>
                    id docelowej galerii: <input type="number" name="id_gal2" min="1" required><br>
                    <br>
                    nr sali: <input type="number" name="nr" required><br>
                    <br>
                    <input type=submit value="Dodaj"><br><br>
                </form>';

                echo "<h3>Wprowadzanie informacji o wypozyczeniach: </h3>";
                echo '<form action="akcje.cgi" method="GET">
                    <input type="hidden" name="action" value="dodaj_wypozyczenie">
                    id eksponatu: <input type="number" name="eksponat_id" min="1" required><br><br>
                    id magazynu: <input type="number" name="magazyn" min="1" required><br><br>
                    id instytucji: <input type="number" name="instytucja" min="1" required><br><br>
                    <input type="submit" value="Dodaj Wypożyczenie"><br><br>
                </form>';

                echo "<h3>Wprowadzanie informacji o zwrotach: </h3>";
                echo '<form action="akcje.cgi" method="GET">
                    <input type="hidden" name="action" value="dodaj_zwrot">
                    id eksponatu: <input type="number" name="eksponat_id" min="1" required><br><br>
                    id instytucji: <input type="number" name="instytucja" min="1" required><br><br>
                    id magazynu: <input type="number" name="magazyn" min="1" required><br><br>
                    <input type="submit" value="Dodaj Zwrot"><br><br>
                </form>';

                echo "<h3>Przeszukiwanie zgromadzonych informacji: </h3>";
                echo '<form action="akcje.cgi" method="get">
                    <input type="hidden" name="action" value="szukaj_po_id">
                    ID Eksponatu: <input type="number" name="id" min="1"><br><br>
                    <input type="submit" value="Szukaj po ID"><br><br>
                </form>';

                echo '<form action="akcje.cgi" method="get">
                    <input type="hidden" name="action" value="szukaj_po_tytule">
                    Tytuł Eksponatu: <input type="text" name="tytul" maxlength="50"><br><br>
                    <input type="submit" value="Szukaj po Tytule"><br><br>
                </form>';

                echo '<form action="akcje.cgi" method="get">
                    <input type="hidden" name="action" value="szukaj_po_autorze">
                    Autor Eksponatu (imię i nazwisko): <input type="text" name="autor" maxlength="50"><br><br>
                    <input type="submit" value="Szukaj po Autorze"><br><br>
                </form>';
            } else {
                echo "<h2>Niepoprawny login lub haslo!</h2>";
                echo "<p>Sprobuj ponownie.</p>";
                echo '<form action="login.cgi" method="GET">
                        <p>Nazwa użytkownika: <input type="text" name="nazwa" required></p>
                        <p>Hasło: <input type="password" name="haslo" required></p>
                        <input type="submit" value="Zaloguj się">
                    </form>';
            }
        } else {
            echo "<h2>Nie wypelniono wszystkich pol formularza!</h2>";
            echo "<p>Sprobuj ponownie.</p>";
            echo '<form action="login.cgi" method="GET">
                <p>Nazwa użytkownika: <input type="text" name="nazwa" required></p>
                <p>Hasło: <input type="password" name="haslo" required></p>
                <input type="submit" value="Zaloguj się">
            </form>';
        }
    } else {
        echo '<form action="login.cgi" method="GET">
                <p>Nazwa użytkownika: <input type="text" name="nazwa" required></p>
                <p>Hasło: <input type="password" name="haslo" required></p>
                <input type="submit" value="Zaloguj się">
            </form>';
    }
    ?>