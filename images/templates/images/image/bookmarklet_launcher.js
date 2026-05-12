(function(){
    // Check if the script has already been loaded
    if(!window.bookmarklet) {
        // Create a script element
        var js = document.body.appendChild(document.createElement('script'));
        // Load the external script
        js.src = '//127.0.0.1:8000/static/js/bookmarklet.js';
        // Set flag to prevent reloading
        window.bookmarklet = true;
    } else {
        // Launch the script if already loaded
        bookmarkletLaunch();
    }
})();
