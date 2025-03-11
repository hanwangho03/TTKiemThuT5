<?php
include 'db.php';

$result = $conn->query("SELECT * FROM todos");
?>

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>To-Do List</title>
</head>
<body>
    <h2>To-Do List</h2>
    <form action="add.php" method="POST">
        <input type="text" name="task" required>
        <button type="submit">Thêm</button>
    </form>
    
    <ul>
        <?php while ($row = $result->fetch_assoc()): ?>
            <li>
                <?php echo $row['task']; ?> 
                (<?php echo $row['status']; ?>)
                <a href="delete.php?id=<?php echo $row['id']; ?>">Xóa</a>
                <a href="update.php?id=<?php echo $row['id']; ?>">Hoàn thành</a>
            </li>
        <?php endwhile; ?>
    </ul>
</body>
</html>
