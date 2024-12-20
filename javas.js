async function uploadImage() {
    const input = document.getElementById('imageUpload');
    const file = input.files[0];
    if (!file) {
        alert('Please select an image file.');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (response.ok) {
            document.getElementById('message').innerText = result.message;
            const faceImage = document.getElementById('faceImage');
            faceImage.src = `http://127.0.0.1:5000/${result.image_url}`;
            faceImage.style.display = 'block';
        } else {
            document.getElementById('message').innerText = result.error;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('message').innerText = 'An error occurred.';
    }
}

async function compareImage() {
    const input = document.getElementById('imageUpload');
    const file = input.files[0];
    if (!file) {
        alert('Please select an image file.');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch('http://127.0.0.1:5000/compare', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (response.ok) {
            document.getElementById('results').innerText = `Matches: ${result.matches.join(', ')}`;
        } else {
            document.getElementById('results').innerText = result.error;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('results').innerText = 'An error occurred.';
    }
}

async function get_faces(){
    const input = document.getElementById('imageUpload');
    const file = input.files[0];
    if (!file) {
        alert('Please select an image file.');
        return;
    }
    const formData = new FormData();
    formData.append('image', file);
    try{
        const response = await fetch('http://127.0.0.1:5000/faces',{
            method:'POST',
            body:formData
        });

        const result = await response.json();
        if (response.ok){
            document.getElementById('results').innerText = `Matches: ${faces}`;
        } else{
            document.getElementById('results').innerText = result.error;
        }
    
    }catch(error){
        console.error('Error:',error);
        document.getElementById('results').innerText = 'An error occurred.';
    }
}
