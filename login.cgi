#!/usr/bin/php
<?php
echo ("Content-type: text/html\n\n");

if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    $nazwa = $_GET['nazwa'];
    $hasło = $_GET['hasło'];

    $poprawna_nazwa = "fajnanazwa";
    $poprawne_hasło = "tajnehaslouuu8";

    if ($login == $poprawny_login && $haslo == $poprawne_haslo) {
        echo "<h2>Zalogowano pomyślnie!</h2>";
        echo "<p>Witaj w sekcji pracowników muzeum!</p>";
    } else {
        echo "<h2>Niepoprawny login lub hasło!</h2>";
        echo "<p>Spróbuj ponownie.</p>";
    }
} else {
    echo '<h2>Strona logowania</h2>';
    echo '<form action="login.cgi" method="post">
            <p>Nazwa uytkownika: <input type="text" name="nazwa" required></p>
            <p>Hasło: <input type="password" name="hasło" required></p>
            <input type="submit" value="Zaloguj się">
            </form>';
}
?>