<?php
session_start();
$db_username = 'root';
$db_password = '';

try {
    $conn = new PDO('mysql:host=localhost;dbname=forum', $db_username, $db_password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    $error_message = "Fatal Error: Connection Failed! " . $e->getMessage();
}
if (isset($conn)) {
} else { 
    echo json_encode(array("error" => $error_message));
    exit(); 
}
?>
