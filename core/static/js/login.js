function refreshCaptcha() {
    const hiddenInput = document.getElementById('id_captcha_0');
    const textInput = document.getElementById('id_captcha_1');

    fetch(
        `/captcha/refresh/`,
        {
            method: "GET",
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        }
    ).then(response => {
            // Check if the response is actually successful (status 200-299)
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.status}`);
            }
            return response.json(); // Only parse as JSON if it's a real response
        })
        .then(data => {
            hiddenInput.value = data.key;
            textInput.value = '';
            const captchaImg = document.querySelector('img.captcha');
            if (captchaImg) {
                captchaImg.src = data.image_url;
            }
        })
        .catch(error => {
            console.error('Error refreshing captcha:', error);
            alert('Could not refresh captcha. Please try again.');
        });
}