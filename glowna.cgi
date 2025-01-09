#!/usr/bin/php
<?php
echo ("Content-type: text/html\n\n");
?>

<!doctype html>
<html>

<head>
    <meta charset="utf-8">
    <title>Strona główna muzeum sztuki</title>
</head>

<body>

    <h2> Strona logowania </h2>

    <form action="glowna.cgi" method="get">
        <p>Kim jesteś?</p>
        <input type="radio" name="role1" value="pracownik"> Pracownik muzeum<br>
        <input type="radio" name="role1" value="odwiedzający"> Osoba odwiedzająca muzeum<br><br>
        <input type="submit" name="enter" value="przejdź dalej">
    </form>

    <?php
    if (isset($_GET['role1']) && $_GET['role1'] == 'pracownik') {
        echo "<h2>Dzień dobry!</h2>";
        echo "<p>Aby kontynuować wprowadź swoje dane logowania.</p>";
        echo '<form action="login.cgi" method="get">
            <p>Nazwa uytkownika: <input type="text" name="nazwa" required></p>
            <p>Hasło: <input type="password" name="hasło" required></p>
            <input type="submit" value="Zaloguj się">
          </form>';
    } elseif (isset($_GET['role1']) && $_GET['role1'] == 'odwiedzający') {
        echo "<h2>Witaj, Odwiedzający!</h2>";
        echo "<p>Cieszymy się, że chcesz odwiedzić nasze muzeum. Życzymy miłego zwiedzania!</p>";
    }
    ?>

</body>

</html>