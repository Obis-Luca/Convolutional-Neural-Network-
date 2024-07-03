<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
header("Access-Control-Allow-Credentials: true");

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['image'])) {
    $uploadDir = 'uploads/';
    $uploadFile = $uploadDir . basename($_FILES['image']['name']);
    # e.g. uploads/airplane1.png

    if (move_uploaded_file($_FILES['image']['tmp_name'], $uploadFile)) {
        $output = shell_exec("python classify.py " . escapeshellarg($uploadFile));
        echo json_encode(['result' => $output]);
    } else {
        echo json_encode(['result' => 'Failed to upload image.']);
    }
} else {
    echo json_encode(['result' => 'Invalid request.']);
}
