document.addEventListener('DOMContentLoaded', () => {
    const uploadBtn = document.getElementById('uploadBtn');
    const imageUpload = document.getElementById('imageUpload');
    const resultDiv = document.getElementById('result');
    const solutionResultDiv = document.getElementById('solution-result');


    uploadBtn.addEventListener('click', () => {
        const file = imageUpload.files[0];

        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            fetch('http://127.0.0.1:8000/predict/', {  // Make sure to point to the correct FastAPI URL
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const predictedClass = data.predicted_class;
                resultDiv.innerHTML = `<p><strong>Predicted Class:</strong> ${predictedClass}</p>`;

                // Clear previous recommendations
                solutionResultDiv.innerHTML = '';

                // Display recommendations based on the predicted class
                if (predictedClass === 'Brown Spots') {
                    solutionResultDiv.innerHTML = `
                        <ul>
                            <li>Avoid overhead irrigation.</li>
                        </ul>`;
                } else if (predictedClass === 'White Scale') {
                    solutionResultDiv.innerHTML = `
                        <ul>
                            <li>Remove and destroy infected palms.</li>
                            <li>Use copper-based fungicides on healthy palms.</li>
                        </ul>`;
                } else if (predictedClass === 'Healthy') {
                    solutionResultDiv.innerHTML = '<p>No specific recommendations. The palm tree is healthy.</p>';
                }
            })
            .catch(error => console.error('Error:', error));
        } else {
            alert('Please upload an image first.');
        }
    });
});