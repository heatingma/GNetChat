var closeButton = document.getElementById('close');
if (closeButton != null){
    closeButton.addEventListener('click', function() {
        var errorBox = this.closest('.error-box');
        if (errorBox) {
            errorBox.style.display = 'none';
        }
    });
}

