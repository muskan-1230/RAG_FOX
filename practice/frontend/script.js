console.log("SCRIPT LOADED SUCCESSFULLY");

let documentId = null;


async function uploadPDF() {

    console.log("UPLOAD BUTTON CLICKED");

    try {

        const fileInput =
            document.getElementById("pdfFile");

        console.log("File Input:", fileInput);

        const file =
            fileInput.files[0];

        console.log("Selected File:", file);

        if (!file) {

            alert("Select a PDF first");

            return;
        }

        const formData = new FormData();

        formData.append(
            "file",
            file
        );

        console.log("Sending upload request...");

        const response =
            await fetch(
                "http://127.0.0.1:8000/upload",
                {
                    method: "POST",
                    body: formData
                }
            );

        console.log("Upload response received");

        const data =
            await response.json();

        console.log(
            "Backend Response:",
            data
        );

        documentId =
            data.document_id;

        console.log(
            "Document ID Saved:",
            documentId
        );

        document.getElementById(
            "status"
        ).innerText =
            `Uploaded: ${data.filename}`;

    }
    catch(error){

        console.error(
            "UPLOAD ERROR:",
            error
        );

    }
}


async function askQuestion() {

    console.log(
        "Current Document ID:",
        documentId
    );

    if (!documentId) {

        alert(
            "Upload a PDF first"
        );

        return;
    }

    const question =
        document.getElementById(
            "question"
        ).value;

    if (!question.trim()) {

        alert(
            "Enter a question"
        );

        return;
    }

    document.getElementById(
        "answer"
    ).innerHTML =
        "<p>Thinking...</p>";

    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                        "application/json"
                    },

                    body: JSON.stringify({
                        document_id:
                        documentId,

                        question:
                        question
                    })
                }
            );

        const data =
            await response.json();

        console.log(
            "Chat Response:",
            data
        );

        document.getElementById(
            "answer"
        ).innerHTML =
            `
            <h3>Answer</h3>
            <p>${data.answer}</p>
            `;

    }
    catch(error){

        console.error(
            "CHAT ERROR:",
            error
        );

    }
}