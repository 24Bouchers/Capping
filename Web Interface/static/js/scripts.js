/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

// retrieves the last part of the current URL (index.html, devices.html, ...)
document.addEventListener("DOMContentLoaded", function() {
    var currentPage = window.location.pathname.split('/').pop();
    var links = document.querySelectorAll('.nav-link');

    links.forEach(function(link) {
        // check if the current page is addDevice.html and the link's href is devices.html
        // if on addDevice.html, still have "devices" highlighted in sidebar
        if (currentPage === 'addDevice.html' && link.getAttribute('href') === 'devices.html') {
            link.classList.add('active');
        } else if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});


