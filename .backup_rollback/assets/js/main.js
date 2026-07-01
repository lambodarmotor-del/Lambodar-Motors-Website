/* ==========================================================================
   Lambodar Motors - Main JavaScript Interactivity
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  
  // 1. STICKY HEADER EFFECT & MOBILE NAVIGATION
  const header = document.querySelector('.main-header');
  const mobileBtn = document.querySelector('.mobile-menu-btn');
  const mobileOverlay = document.querySelector('.mobile-nav-overlay');

  if (header) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        header.classList.add('sticky');
      } else {
        header.classList.remove('sticky');
      }
    });
  }

  if (mobileBtn && mobileOverlay) {
    mobileBtn.addEventListener('click', () => {
      mobileBtn.classList.toggle('active');
      mobileOverlay.classList.toggle('active');
      document.body.classList.toggle('no-scroll');
    });

    // Close menu when clicking link
    mobileOverlay.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileBtn.classList.remove('active');
        mobileOverlay.classList.remove('active');
        document.body.classList.remove('no-scroll');
      });
    });
  }

  // 2. BEFORE/AFTER SLIDER INTERACTIVITY
  const sliderWrapper = document.querySelector('.slider-wrapper');
  const beforeImg = document.querySelector('.slider-img-before');
  const handle = document.querySelector('.slider-handle');

  if (sliderWrapper && beforeImg && handle) {
    let isDragging = false;

    const moveSlider = (clientX) => {
      const rect = sliderWrapper.getBoundingClientRect();
      const position = clientX - rect.left;
      let percentage = (position / rect.width) * 100;

      // Bound between 0% and 100%
      if (percentage < 0) percentage = 0;
      if (percentage > 100) percentage = 100;

      beforeImg.style.width = `${percentage}%`;
      handle.style.left = `${percentage}%`;
    };

    // Mouse Events
    sliderWrapper.addEventListener('mousedown', (e) => {
      isDragging = true;
      moveSlider(e.clientX);
    });

    window.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      moveSlider(e.clientX);
    });

    window.addEventListener('mouseup', () => {
      isDragging = false;
    });

    // Touch Events (Mobile friendly)
    sliderWrapper.addEventListener('touchstart', (e) => {
      isDragging = true;
      moveSlider(e.touches[0].clientX);
    }, { passive: true });

    window.addEventListener('touchmove', (e) => {
      if (!isDragging) return;
      moveSlider(e.touches[0].clientX);
    }, { passive: true });

    window.addEventListener('touchend', () => {
      isDragging = false;
    });
  }

  // 3. LIGHTBOX MODAL FOR GALLERY
  const galleryItems = document.querySelectorAll('.gallery-item');
  const lightbox = document.getElementById('lightboxModal');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxClose = document.querySelector('.lightbox-close');

  if (galleryItems.length > 0 && lightbox && lightboxImg) {
    galleryItems.forEach(item => {
      item.addEventListener('click', () => {
        const img = item.querySelector('img');
        if (img) {
          lightboxImg.src = img.src;
          lightboxImg.alt = img.alt;
          lightbox.classList.add('active');
          document.body.classList.add('no-scroll');
        }
      });
    });

    const closeLightbox = () => {
      lightbox.classList.remove('active');
      document.body.classList.remove('no-scroll');
      lightboxImg.src = '';
    };

    if (lightboxClose) {
      lightboxClose.addEventListener('click', closeLightbox);
    }

    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) {
        closeLightbox();
      }
    });

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && lightbox.classList.contains('active')) {
        closeLightbox();
      }
    });
  }

  // 4. FAQ ACCORDION TOGGLE
  const faqQuestions = document.querySelectorAll('.faq-question');
  
  if (faqQuestions.length > 0) {
    faqQuestions.forEach(question => {
      question.addEventListener('click', () => {
        const item = question.parentElement;
        const isActive = item.classList.contains('active');
        
        // Close all other open items
        document.querySelectorAll('.faq-item').forEach(faqItem => {
          faqItem.classList.remove('active');
        });

        // Toggle current item
        if (!isActive) {
          item.classList.add('active');
        }
      });
    });
  }
});

// 5. WHATSAPP FORM ACTION PIPELINE
function sendToWhatsApp(e) {
  e.preventDefault();
  const name = document.getElementById('cf-name').value.trim();
  const phone = document.getElementById('cf-phone').value.trim();
  const car = document.getElementById('cf-car').value.trim();
  const service = document.getElementById('cf-service').value;
  const msg = encodeURIComponent(
    "Hi Lambodar Motors! 🙏\n\n" +
    "Name: " + name + "\n" +
    "Phone: " + phone + "\n" +
    "Car: " + car + "\n" +
    "Service Needed: " + service + "\n\n" +
    "Please let me know the availability. Thank you!"
  );
  window.open("https://wa.me/918141282494?text=" + msg, "_blank");
}
