$(function () {

  /* ---- Sticky navbar shrink on scroll ---- */
  var $navbar = $('.navbar-portfolio');
  $(window).on('scroll', function () {
    if ($(window).scrollTop() > 40) {
      $navbar.addClass('is-scrolled');
    } else {
      $navbar.removeClass('is-scrolled');
    }
  });

  /* ---- Active nav link highlight on scroll ---- */
  var $sections = $('section[id]');
  $(window).on('scroll', function () {
    var scrollPos = $(window).scrollTop() + 120;
    $sections.each(function () {
      var top = $(this).offset().top;
      var bottom = top + $(this).outerHeight();
      var id = $(this).attr('id');
      if (scrollPos >= top && scrollPos < bottom) {
        $('.navbar-portfolio .nav-link').removeClass('active');
        $('.navbar-portfolio .nav-link[href="#' + id + '"]').addClass('active');
      }
    });
  });

  /* ---- Scroll-reveal fade-in-up (IntersectionObserver, falls back gracefully) ---- */
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(function (el) { observer.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---- Hero typed tagline effect ---- */
  var taglineText = '# Full Stack Web Developer | Python & Django';
  var $target = $('#heroTyped');
  if ($target.length) {
    var i = 0;
    function typeChar() {
      if (i <= taglineText.length) {
        $target.text(taglineText.slice(0, i));
        i++;
        setTimeout(typeChar, 28);
      }
    }
    typeChar();
  }

  /* ---- Smooth scroll for in-page anchors (native CSS already handles most,
          this closes the mobile menu after a link is tapped) ---- */
  $('.navbar-portfolio .nav-link').on('click', function () {
    var $collapse = $('.navbar-collapse');
    if ($collapse.hasClass('show')) {
      $collapse.collapse('hide');
    }
  });

  /* ---- Footer year ---- */
  $('#year').text(new Date().getFullYear());

  /* ---- Back to top button ---- */
  var $backToTop = $('#backToTop');
  $(window).on('scroll', function () {
    if ($(window).scrollTop() > 500) {
      $backToTop.addClass('show');
    } else {
      $backToTop.removeClass('show');
    }
  });

  /* ---- Contact form -> Django REST endpoint (Ajax) ----
     Backend route: POST /api/contact/  (see core/urls.py)
     Falls back to a mailto link if the API is not reachable
     (e.g. when this page is opened as a static file). */
  $('#contactForm').on('submit', function (e) {
    e.preventDefault();
    var $form = $(this);
    var $btn = $('#contactSubmitBtn');
    var $status = $('#formStatus');

    var payload = {
      name: $form.find('[name="name"]').val().trim(),
      email: $form.find('[name="email"]').val().trim(),
      message: $form.find('[name="message"]').val().trim()
    };

    if (!payload.name || !payload.email || !payload.message) {
      $status.removeClass('ok').addClass('err').text('Please fill in all fields.');
      return;
    }

    $btn.prop('disabled', true).html('<i class="bi bi-hourglass-split"></i> Sending...');
    $status.removeClass('ok err').text('');

    $.ajax({
      url: '/api/contact/',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(payload),
      headers: { 'X-CSRFToken': getCookie('csrftoken') }
    })
      .done(function () {
        $status.removeClass('err').addClass('ok').text('Message sent — thank you! I will get back to you soon.');
        $form[0].reset();
      })
      .fail(function () {
        var mailto = 'mailto:rajatverma8855@gmail.com?subject=Portfolio%20Contact%20from%20' +
          encodeURIComponent(payload.name) + '&body=' + encodeURIComponent(payload.message + '\n\nReply to: ' + payload.email);
        window.location.href = mailto;
        $status.removeClass('ok').addClass('err').text('Backend not reachable — opening your email app instead.');
      })
      .always(function () {
        $btn.prop('disabled', false).html('<i class="bi bi-send-fill"></i> Send message');
      });
  });

  function getCookie(name) {
    var value = '; ' + document.cookie;
    var parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
  }

});
