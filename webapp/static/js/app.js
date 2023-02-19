const csrf_token = "{{ csrf_token() }}";

window.onload = function() {
    const hamburger = document.querySelector('.hamburger-menu');
    const navigation = document.querySelector('.navigation');
    hamburger.addEventListener('click', function() {
      navigation.classList.toggle('active');
    });
};

