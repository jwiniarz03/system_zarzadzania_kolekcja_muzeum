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
    <h1> Muzeum sztuki </h1>
    <?php
    if ($_SERVER['REQUEST_METHOD'] == 'GET') {
        parse_str($_SERVER["QUERY_STRING"], $form_data);

        if (isset($form_data['role1'])) {
            $role = $form_data['role1'];

            if ($role === 'pracownik') {
                echo "<h2>Witaj pracowniku!</h2>";
                echo '<form action="login.cgi" method="GET">
                    <h3>Logowanie</h3>
                    <p>Nazwa użytkownika: <input type="text" name="nazwa" required></p>
                    <p>Hasło: <input type="password" name="haslo" required></p>
                    <input type="submit" value="Zaloguj się">
                </form>';
            } elseif ($role === 'odwiedzający') {
                echo "<h2>Witaj, Odwiedzajacy!</h2>";
                echo '<form action="szukaj.cgi" method="GET">
                    <h3>Wyszukiwarka eksponatów:</h3>
                    Wprowadź tytuł eksponatu: <input type="text" name="tytul" maxlength="50" required><br><br>
                    <input type="submit" value="Szukaj">
                </form>';
            }
        }
    } else {
        echo '<form action="glowna.cgi" method="GET">
            <p>Kim jesteś?</p>
            <input type="radio" name="role1" value="pracownik"> Pracownik muzeum<br>
            <input type="radio" name="role1" value="odwiedzający"> Osoba odwiedzająca muzeum<br><br>
            <input type="submit" name="enter" value="Przejdź dalej">
        </form>';
    }
    ?>

</body>

</html>