var light_dark = document.getElementById('light-dark');
var flag = 0;

function change_style() {
    var styles = document.getElementsByTagName('link');
    if (flag == 0) {
        // change from light to dark
        for (var i = 0; i < styles.length; i++) {
            var style = styles[i];
            var href = style.getAttribute('href');
            if (href.includes('light/'))
                style.disabled = true;
            if (href.includes('dark/'))
                style.disabled = false;
        }
    } 
    else {
        // change from dark to light
        for (var i = 0; i < styles.length; i++) {
            var style = styles[i];
            var href = style.getAttribute('href');
            if (href.includes('light/'))
                style.disabled = false;
            if (href.includes('dark/'))
                style.disabled = true;
        }
    }
    flag = (flag + 1) % 2;
}

light_dark.addEventListener('click', change_style);
