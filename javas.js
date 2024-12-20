// 异步函数，用于上传图像
async function uploadImage() {
    // 获取文件输入元素
    const input = document.getElementById('imageUpload');
    // 获取用户选择的文件
    const file = input.files[0];
    // 如果没有选择文件，弹出提示并返回
    if (!file) {
        alert('Please select an image file.');
        return;
    }

    // 创建一个 FormData 对象，用于存储文件数据
    const formData = new FormData();
    formData.append('image', file);

    try {
        // 使用 fetch API 发送 POST 请求，将文件上传到服务器
        const response = await fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData
        });

        // 解析服务器返回的 JSON 数据
        const result = await response.json();
        // 如果响应成功，更新页面内容
        if (response.ok) {
            document.getElementById('message').innerText = result.message;
            

            // 清空之前的图像
            const imagesContainer = document.getElementById('imagesContainer');
            imagesContainer.innerHTML = '';

            // 遍历返回的图像 URL 列表，并将每个图像添加到容器中
            result.image_urls.forEach(image_url => {
                const faceImage = document.createElement('img');
                faceImage.src = `http://127.0.0.1:5000/${image_url}`;
                faceImage.style.display = 'block';
                faceImage.style.width = '100px'; // 设置图像宽度
                faceImage.style.height = '100px'; // 设置图像高度
                imagesContainer.appendChild(faceImage); // 将图像添加到容器中
            });

        } else {
            // 如果响应失败，显示错误信息
            document.getElementById('message').innerText = result.error;
        }
    } catch (error) {
        // 捕获并显示错误信息
        console.error('Error:', error);
        document.getElementById('message').innerText = 'An error occurred.';
    }
}

// 异步函数，用于比较图像
async function compareImage() {
    // 获取文件输入元素
    const input = document.getElementById('imageUpload');
    // 获取用户选择的文件
    const file = input.files[0];
    // 如果没有选择文件，弹出提示并返回
    if (!file) {
        alert('Please select an image file.');
        return;
    }

    // 创建一个 FormData 对象，用于存储文件数据
    const formData = new FormData();
    formData.append('image', file);

    try {
        // 使用 fetch API 发送 POST 请求，将文件上传到服务器进行比较
        const response = await fetch('http://127.0.0.1:5000/compare', {
            method: 'POST',
            body: formData
        });

        // 解析服务器返回的 JSON 数据
        const result = await response.json();
        // 如果响应成功，显示匹配结果
        if (response.ok) {
            document.getElementById('results').innerText = `Matches: ${result.matches.join(', ')}`;
        } else {
            // 如果响应失败，显示错误信息
            document.getElementById('results').innerText = result.error;
        }
    } catch (error) {
        // 捕获并显示错误信息
        console.error('Error:', error);
        document.getElementById('results').innerText = 'An error occurred.';
    }
}

// 异步函数，用于获取所有面部信息
async function get_faces(){
    // 获取文件输入元素
    const input = document.getElementById('imageUpload');
    // 获取用户选择的文件
    const file = input.files[0];
    // 如果没有选择文件，弹出提示并返回
    if (!file) {
        alert('Please select an image file.');
        return;
    }

    // 创建一个 FormData 对象，用于存储文件数据
    const formData = new FormData();
    formData.append('image', file);

    try {
        // 使用 fetch API 发送 POST 请求，获取所有面部信息
        const response = await fetch('http://127.0.0.1:5000/faces', {
            method: 'POST',
            body: formData
        });

        // 解析服务器返回的 JSON 数据
        const result = await response.json();
        // 如果响应成功，显示面部信息
        if (response.ok) {
            document.getElementById('results').innerText = `Matches: ${faces}`;
        } else {
            // 如果响应失败，显示错误信息
            document.getElementById('results').innerText = result.error;
        }
    } catch (error) {
        // 捕获并显示错误信息
        console.error('Error:', error);
        document.getElementById('results').innerText = 'An error occurred.';
    }
}
