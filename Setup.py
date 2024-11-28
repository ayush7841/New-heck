import os

# Define the base directory for the site
base_dir = '/storage/emulated/0/Documents/site'

# Define the folder structure to be created
folders = [
    os.path.join(base_dir, 'frontend'),
    os.path.join(base_dir, 'backend', 'functions')
]

# Files to be created with their content
files = {
    os.path.join(base_dir, 'index.html'): """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MS32</title>
    <link href="https://fonts.googleapis.com/css2?family=Silkscreen&display=swap" rel="stylesheet">
</head>
<style>
/* Styling remains the same */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body, html {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: "Silkscreen", monospace;
    background-color: #0a0a0a;
    color: #00ff00;
    overflow: hidden;
}

.container {
    text-align: center;
    width: 100%;
    max-width: 400px;
}

.text {
    width: 100%;
    height: 70px;
    padding: 10px;
    font-family: "Silkscreen", monospace;
    font-size: 18px;
    color: #00ff00;
    background-color: #1a1a1a;
    border: 2px solid #00ff00;
    border-radius: 8px;
    outline: none;
    resize: none;
    box-shadow: 0 0 5px rgba(0, 255, 0, 0.5);
    margin-bottom: 20px;
}

.btn {
    padding: 10px 20px;
    font-size: 16px;
    font-family: "Silkscreen", monospace;
    background-color: #222222;
    color: #00ff00;
    border: 2px solid #00ff00;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-bottom: 10px;
}

.btn:hover {
    background-color: #326132;
    color: #dfd5d5;
}

.file-label {
    display: inline-block;
    padding: 10px 20px;
    font-size: 14px;
    font-family: "Silkscreen", monospace;
    background-color: #1a1a1a;
    color: #00ff00;
    border: 2px solid #00ff00;
    border-radius: 8px;
    cursor: pointer;
    margin-bottom: 10px;
    box-shadow: 0 0 5px rgba(0, 255, 0, 0.5);
    transition: background-color 0.3s ease;
}

.file-label:hover {
    background-color: #326132;
    color: #dfd5d5;
}

.file-input {
    display: none;
}

.extra-gap {
    margin-top: 30px;
}

.status {
    position: absolute;
    font-family: "Silkscreen", monospace;
    top: 10px;
    right: 10px;
    font-size: 16px;
    font-weight: bold;
    color: #ff0000;
    text-shadow: 0 0 5px #ff0000;
}

.file-name {
    color: #00ff00;
    margin-top: 10px;
    font-size: 14px;
}
</style>
<body>
    <div class="container">
        <textarea placeholder="Type something..." class="text" name="text"></textarea>

        <button class="btn" type="submit" onclick="edit()">Send</button>

        <div class="extra-gap">
            <label for="fileInput" class="file-label">Choose File</label>
            <input type="file" class="file-input" id="fileInput">
            <button class="btn" onclick="readFile()">Play</button>
            <div id="fileName" class="file-name"></div> <!-- To display the file name -->
        </div>
    </div>
    <div class="status">Offline</div>

    <script>
        function edit(file=null) {
            fetch('/.netlify/functions/edit-message', {  // Updated path for edit-message function
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: file ? file : document.querySelector(".text").value })
            })
            .then(response => response.json())
            .then(data => {
                // You can handle any response here if needed, but no need to display the response now
            })
            .catch(error => {
                // Handle any errors here
                console.log('Error occurred while saving the message.');
            });
        }

        function status() {
            requestAnimationFrame(status);
            fetch('/status.json')  // Path to fetch status.json file
                .then(response => response.json())
                .then(data => {
                    let prev = data["prevTime"];
                    let end = data["endTime"];
                    if (end - prev > 4 || (prev === 0 && end === 0)) {
                        document.querySelector(".status").textContent = "Offline";
                        document.querySelector(".status").style.color = "red";
                    } else {
                        document.querySelector(".status").textContent = "Online";
                        document.querySelector(".status").style.color = "green";
                    }
                });
        }

        function readFile() {
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    const binaryData = new Uint8Array(event.target.result);
                    edit(binaryData);

                    // Clear the file input and hide the file name after playing
                    fileInput.value = "";
                    document.getElementById('fileName').textContent = ''; // Clear the file name display
                };
                reader.readAsArrayBuffer(file);
            } else {
                console.log("No file selected.");
            }
        }

        // Display file name once a file is selected
        document.getElementById('fileInput').addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                document.getElementById('fileName').textContent = `Selected File: ${file.name}`;
            } else {
                document.getElementById('fileName').textContent = '';
            }
        });

        status()
    </script>
</body>
</html>


    """,
    os.path.join(base_dir, 'backend', 'functions', 'edit-message.js'): """
const fs = require('fs');
const path = require('path');

const messageFilePath = path.join(__dirname, '../../message.txt');
const statusFilePath = path.join(__dirname, '../../status.json');

exports.handler = async function(event, context) {
    const { text } = JSON.parse(event.body);

    if (!text) {
        return { statusCode: 400, body: JSON.stringify({ status: 'error', message: 'No text provided' }) };
    }

    // Write the new content to message.txt
    fs.writeFileSync(messageFilePath, text, 'utf8');

    return { statusCode: 200, body: JSON.stringify({ status: 'success', message: 'Message updated' }) };
};
    """,
    os.path.join(base_dir, 'backend', 'functions', 'fetch-message.js'): """
const fs = require('fs');
const path = require('path');

const messageFilePath = path.join(__dirname, '../../message.txt');

exports.handler = async function(event, context) {
    try {
        const data = fs.readFileSync(messageFilePath, 'utf8');
        return { statusCode: 200, body: JSON.stringify({ status: 'success', data }) };
    } catch (err) {
        return { statusCode: 500, body: JSON.stringify({ status: 'error', message: 'File not found' }) };
    }
};
    """,
    os.path.join(base_dir, 'backend', 'functions', 'update-status.js'): """
const fs = require('fs');
const path = require('path');

const statusFilePath = path.join(__dirname, '../../status.json');

exports.handler = async function(event, context) {
    try {
        const statusData = fs.readFileSync(statusFilePath, 'utf8');
        const jsonData = JSON.parse(statusData);
        jsonData.endTime = Math.floor(Date.now() / 1000);  // Current time in seconds
        fs.writeFileSync(statusFilePath, JSON.stringify(jsonData, null, 2), 'utf8');
        return { statusCode: 200, body: JSON.stringify({ status: 'success', message: 'status.json updated successfully' }) };
    } catch (err) {
        return { statusCode: 500, body: JSON.stringify({ status: 'error', message: 'Failed to update status.json' }) };
    }
};
    """,
    os.path.join(base_dir, 'status.json'): """
{
    "preTime": 0,
    "endTime": 0
}
    """,
    os.path.join(base_dir, 'message.txt'): "",  # Empty file for the message
    os.path.join(base_dir, 'netlify.toml'): """
[build]
  publish = "site"
  functions = "backend/functions"

[[redirects]]
  from = "/edit-message"
  to = "/.netlify/functions/edit-message"
  status = 200

[[redirects]]
  from = "/fetch-message"
  to = "/.netlify/functions/fetch-message"
  status = 200

[[redirects]]
  from = "/update-status"
  to = "/.netlify/functions/update-status"
  status = 200
"""
}

# Create the folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create the files and write their content
for file_path, content in files.items():
    with open(file_path, 'w') as file:
        file.write(content.strip())

print(f"Folder structure and files created in {base_dir}")
