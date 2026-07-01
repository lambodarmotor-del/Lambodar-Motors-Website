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

  // 4.5. BRAND LOGO LIGHTBOX MODAL (POPUP IN THE SAME TAB WITH BACK BUTTON)
  const logoLinks = document.querySelectorAll('.logo');
  if (logoLinks.length > 0) {
    logoLinks.forEach(logoLink => {
      logoLink.addEventListener('click', (e) => {
        e.preventDefault();
        const logoImg = logoLink.querySelector('.logo-img');
        if (!logoImg) return;
        
        let logoModal = document.getElementById('logoLightbox');
        if (!logoModal) {
          logoModal = document.createElement('div');
          logoModal.id = 'logoLightbox';
          logoModal.style.position = 'fixed';
          logoModal.style.top = '0';
          logoModal.style.left = '0';
          logoModal.style.width = '100%';
          logoModal.style.height = '100%';
          logoModal.style.backgroundColor = 'rgba(10, 10, 12, 0.95)';
          logoModal.style.zIndex = '9999';
          logoModal.style.display = 'flex';
          logoModal.style.alignItems = 'center';
          logoModal.style.justifyContent = 'center';
          logoModal.style.opacity = '0';
          logoModal.style.transition = 'opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
          logoModal.style.pointerEvents = 'none';

          logoModal.innerHTML = `
            <div id="logoLightboxContent" style="position: relative; text-align: center; transform: scale(0.9); opacity: 0; transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.3s ease;">
              <button id="closeLogoLightbox" style="position: absolute; top: -65px; left: 50%; transform: translateX(-50%); background: #16161a; border: 1.5px solid rgba(255,255,255,0.15); color: #fff; padding: 10px 24px; border-radius: 30px; font-size: 14px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 8px; font-family: 'Outfit', sans-serif; box-shadow: 0 4px 20px rgba(0,0,0,0.5); transition: all 0.2s ease; outline: none; white-space: nowrap;">
                <span>← Back</span>
              </button>
              <img id="logoLightboxImg" src="" alt="Lambodar Motors Brand Logo" style="width: 380px; height: 380px; max-width: 85vw; max-height: 85vw; border-radius: 16px; box-shadow: 0 15px 40px rgba(0,0,0,0.7); object-fit: cover; border: 2px solid rgba(255,255,255,0.1); background-color: #0b0b0d;" />
            </div>
          `;
          document.body.appendChild(logoModal);

          const closeBtn = document.getElementById('closeLogoLightbox');
          const closeLightbox = () => {
            const contentEl = document.getElementById('logoLightboxContent');
            contentEl.style.transform = 'scale(0.9)';
            contentEl.style.opacity = '0';
            logoModal.style.opacity = '0';
            logoModal.style.pointerEvents = 'none';
            document.body.classList.remove('no-scroll');
          };

          closeBtn.addEventListener('click', closeLightbox);
          logoModal.addEventListener('click', (ev) => {
            if (ev.target === logoModal) {
              closeLightbox();
            }
          });

          // Escape key to close
          window.addEventListener('keydown', (ev) => {
            if (ev.key === 'Escape') {
              closeLightbox();
            }
          });

          // Hover transition for back button
          closeBtn.addEventListener('mouseenter', () => {
            closeBtn.style.borderColor = '#b91c1c';
            closeBtn.style.transform = 'translateX(-50%) scale(1.05)';
            closeBtn.style.boxShadow = '0 6px 24px rgba(185, 28, 28, 0.3)';
          });
          closeBtn.addEventListener('mouseleave', () => {
            closeBtn.style.borderColor = 'rgba(255,255,255,0.15)';
            closeBtn.style.transform = 'translateX(-50%) scale(1)';
            closeBtn.style.boxShadow = '0 4px 20px rgba(0,0,0,0.5)';
          });
        }

        const imgEl = document.getElementById('logoLightboxImg');
        imgEl.src = logoImg.src;
        
        // Open with animation
        logoModal.style.opacity = '1';
        logoModal.style.pointerEvents = 'auto';
        document.body.classList.add('no-scroll');
        
        const contentEl = document.getElementById('logoLightboxContent');
        setTimeout(() => {
          contentEl.style.transform = 'scale(1)';
          contentEl.style.opacity = '1';
        }, 10);
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
