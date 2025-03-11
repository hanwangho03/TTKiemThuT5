<?php
include 'db.php';

if (isset($_GET['id'])) {
    $id = $_GET['id'];
    $conn->query("UPDATE todos SET status = 'completed' WHERE id = $id");
}

header("Location: index.php");
?>
