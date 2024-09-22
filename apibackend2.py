const express = require('express');
const bodyParser = require('body-parser');
const mime = require('mime-types');
const atob = require('atob');  

const app = express();

app.use(bodyParser.json());

const handleFile = (fileB64) => {
    try {
        const fileBuffer = Buffer.from(fileB64, 'base64'); 
        const fileSizeKb = fileBuffer.length / 1024; 
        const mimeType = mime.lookup(fileB64);  

        if (mimeType) {
            return { isValid: true, mimeType, fileSizeKb };
        } else {
            return { isValid: false };
        }
    } catch (error) {
        console.error("File handling error:", error);
        return { isValid: false };
    }
};

app.post('/bfhl', (req, res) => {
    try {
        const { data = [], file_b64 } = req.body;

        // Hardcoded user details
        const fullName = "john_doe";
        const dob = "17091999";
        const email = "john@xyz.com";
        const rollNumber = "ABCD123";
        const userId = `${fullName}_${dob}`;

        // Separate numbers and alphabets from the data array
        const numbers = data.filter(item => /^\d+$/.test(item));
        const alphabets = data.filter(item => /^[A-Za-z]$/.test(item));

        // Find the highest lowercase alphabet
        const lowercaseAlphabets = alphabets.filter(char => char === char.toLowerCase());
        const highestLowercaseAlphabet = lowercaseAlphabets.length > 0 ? [Math.max(...lowercaseAlphabets)] : [];

        // Handle file if provided
        let fileDetails = { isValid: false };
        if (file_b64) {
            fileDetails = handleFile(file_b64);
        }

        const response = {
            is_success: true,
            user_id: userId,
            email: email,
            roll_number: rollNumber,
            numbers: numbers,
            alphabets: alphabets,
            highest_lowercase_alphabet: highestLowercaseAlphabet,
            file_valid: fileDetails.isValid,
            file_mime_type: fileDetails.isValid ? fileDetails.mimeType : null,
            file_size_kb: fileDetails.isValid ? fileDetails.fileSizeKb : null
        };

        res.status(200).json(response);
    } catch (error) {
        console.error("Error processing request:", error);
        res.status(400).json({ is_success: false, error: error.message });
    }
});

app.get('/bfhl', (req, res) => {
    res.status(200).json({ operation_code: 1 });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

