<?php
include 'db.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $task = $_POST['task'];
    $conn->query("INSERT INTO todos (task) VALUES ('$task')");
}

header("Location: index.php");
?>
