var closeButton = document.getElementById('close');
closeButton.addEventListener('click', function() {
    var errorBox = this.closest('.error-box');
    if (errorBox) {
        errorBox.style.display = 'none';
    }
});
