<?php
use PHPUnit\Framework\TestCase;

class TodoTest extends TestCase {
    private $conn;

    protected function setUp(): void {
        $this->conn = new mysqli("localhost", "root", "", "todolist_db");
    }

    public function testAddTask() {
        $task = "Test Task";
        $this->conn->query("INSERT INTO todos (task) VALUES ('$task')");
        $result = $this->conn->query("SELECT * FROM todos WHERE task='$task'");
        $this->assertEquals(1, $result->num_rows);
    }

    public function testDeleteTask() {
        $this->conn->query("DELETE FROM todos WHERE task='Test Task'");
        $result = $this->conn->query("SELECT * FROM todos WHERE task='Test Task'");
        $this->assertEquals(0, $result->num_rows);
    }
}
?>
