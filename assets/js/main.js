// Force scroll restoration to top of page on reload
if (history.scrollRestoration) {
  history.scrollRestoration = "manual";
}
window.scrollTo(0, 0);

/* ==========================================================================
   Lambodar Motors - Main JavaScript Interactivity
   ========================================================================== */

// Utility Focus Trap for Screen Readers and Keyboard users
function trapFocus(modal) {
  const focusableElements = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex="0"]');
  if (focusableElements.length === 0) return;
  const firstFocusableElement = focusableElements[0];
  const lastFocusableElement = focusableElements[focusableElements.length - 1];

  // Remove existing listener to prevent duplicates
  modal.removeEventListener('keydown', modal._focusTrapListener);

  modal._focusTrapListener = function(e) {
    if (e.key !== 'Tab') return;

    if (e.shiftKey) {
      if (document.activeElement === firstFocusableElement) {
        lastFocusableElement.focus();
        e.preventDefault();
      }
    } else {
      if (document.activeElement === lastFocusableElement) {
        firstFocusableElement.focus();
        e.preventDefault();
      }
    }
  };

  modal.addEventListener('keydown', modal._focusTrapListener);
}

document.addEventListener('DOMContentLoaded', () => {
  // Dynamically load Lucide icons
  const lucideScript = document.createElement('script');
  lucideScript.src = 'https://unpkg.com/lucide@0.344.0/dist/umd/lucide.min.js';
  lucideScript.onload = () => {
    if (window.lucide) {
      window.lucide.createIcons();
    }
  };
  document.head.appendChild(lucideScript);
  
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
      const isActive = mobileBtn.classList.toggle('active');
      mobileOverlay.classList.toggle('active');
      document.body.classList.toggle('no-scroll');
      
      mobileBtn.setAttribute('aria-expanded', isActive ? 'true' : 'false');
      
      if (isActive) {
        trapFocus(mobileOverlay);
        const firstLink = mobileOverlay.querySelector('a');
        if (firstLink) firstLink.focus();
      }
    });

    // Close menu when clicking link
    mobileOverlay.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileBtn.classList.remove('active');
        mobileOverlay.classList.remove('active');
        document.body.classList.remove('no-scroll');
        mobileBtn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // 2. BEFORE/AFTER SLIDER INTERACTIVITY
  const sliderWrapper = document.querySelector('.slider-wrapper');
  const beforeImg = document.querySelector('.slider-img-before');
  const handle = document.querySelector('.slider-handle');

  if (sliderWrapper && beforeImg && handle) {
    let isDragging = false;
    const beforeImgEl = beforeImg.querySelector('img');

    const updateImageWidth = () => {
      const rect = sliderWrapper.getBoundingClientRect();
      if (beforeImgEl) {
        beforeImgEl.style.width = `${rect.width}px`;
      }
    };

    // Initialize and bind resize
    updateImageWidth();
    window.addEventListener('resize', updateImageWidth);
    
    // Also trigger on window load to ensure accurate measurements after images load
    window.addEventListener('load', updateImageWidth);

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

    // Keyboard support for Before/After Slider
    const handleButton = handle.querySelector('.slider-handle-button') || handle;
    handleButton.addEventListener('keydown', (e) => {
      let percentage = parseFloat(handle.style.left);
      if (isNaN(percentage)) {
        percentage = 70; // default in HTML
      }

      if (e.key === 'ArrowLeft') {
        e.preventDefault();
        percentage = Math.max(0, percentage - 5);
        beforeImg.style.width = `${percentage}%`;
        handle.style.left = `${percentage}%`;
        handleButton.setAttribute('aria-valuenow', Math.round(percentage));
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        percentage = Math.min(100, percentage + 5);
        beforeImg.style.width = `${percentage}%`;
        handle.style.left = `${percentage}%`;
        handleButton.setAttribute('aria-valuenow', Math.round(percentage));
      }
    });
  }

  // 3. LIGHTBOX MODAL FOR GALLERY (OPTION 2: LOGO-STYLE GRID POPUP & ZOOM)
  const galleryItems = document.querySelectorAll('.gallery-item');
  const galleryLightbox = document.getElementById('galleryLightbox');
  const galleryLightboxTitle = document.getElementById('galleryLightboxTitle');
  const galleryLightboxGrid = document.getElementById('galleryLightboxGrid');
  const closeGalleryLightbox = document.getElementById('closeGalleryLightbox');

  const zoomLightbox = document.getElementById('imageZoomLightbox');
  const zoomLightboxImg = document.getElementById('zoomLightboxImg');
  const closeZoomLightbox = document.getElementById('closeZoomLightbox');

  if (galleryItems.length > 0 && galleryLightbox && galleryLightboxGrid) {
    let lastActiveElement = null;

    galleryItems.forEach(item => {
      const openLightbox = () => {
        lastActiveElement = document.activeElement;
        const title = item.getAttribute('data-gallery-title') || 'Workshop Gallery';
        const imagesStr = item.getAttribute('data-gallery-images') || '';
        const captionsStr = item.getAttribute('data-gallery-captions') || '';

        if (!imagesStr) return;

        const images = imagesStr.split(',');
        const captions = captionsStr.split(',');

        // Set Title
        galleryLightboxTitle.textContent = title;

        // Clear and Populate Grid
        galleryLightboxGrid.innerHTML = '';
        images.forEach((imgSrc, idx) => {
          const caption = captions[idx] || '';
          
          const wrapper = document.createElement('div');
          wrapper.className = 'gallery-lightbox-img-wrapper';
          wrapper.setAttribute('tabindex', '0');
          wrapper.setAttribute('role', 'button');
          wrapper.setAttribute('aria-label', `View image of ${caption.trim()}`);
          wrapper.innerHTML = `
            <img src="${imgSrc.trim()}" alt="${caption.trim()}" loading="lazy" />
            <div class="gallery-lightbox-img-caption">${caption.trim()}</div>
          `;

          // Handle click/enter to zoom image
          const triggerZoom = () => {
            if (zoomLightbox && zoomLightboxImg) {
              zoomLightboxImg.src = imgSrc.trim();
              zoomLightboxImg.alt = caption.trim();
              zoomLightbox.classList.add('active');
              trapFocus(zoomLightbox);
              if (closeZoomLightbox) closeZoomLightbox.focus();
              
              // Zoom Content animation
              const zoomContent = zoomLightbox.querySelector('.zoom-lightbox-content');
              if (zoomContent) {
                setTimeout(() => {
                  zoomContent.style.transform = 'scale(1)';
                  zoomContent.style.opacity = '1';
                }, 10);
              }
            }
          };

          wrapper.addEventListener('click', (e) => {
            e.stopPropagation();
            triggerZoom();
          });

          wrapper.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              triggerZoom();
            }
          });

          galleryLightboxGrid.appendChild(wrapper);
        });

        // Open Gallery Lightbox
        galleryLightbox.classList.add('active');
        document.body.classList.add('no-scroll');
        trapFocus(galleryLightbox);
        if (closeGalleryLightbox) closeGalleryLightbox.focus();

        // Animation classes
        const contentEl = document.getElementById('galleryLightboxContent');
        if (contentEl) {
          setTimeout(() => {
            contentEl.style.transform = 'scale(1)';
            contentEl.style.opacity = '1';
          }, 10);
        }
      };

      item.addEventListener('click', openLightbox);

      item.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openLightbox();
        }
      });
    });

    const hideGalleryLightbox = () => {
      const contentEl = document.getElementById('galleryLightboxContent');
      if (contentEl) {
        contentEl.style.transform = 'scale(0.9)';
        contentEl.style.opacity = '0';
      }
      setTimeout(() => {
        galleryLightbox.classList.remove('active');
        document.body.classList.remove('no-scroll');
        if (lastActiveElement) lastActiveElement.focus();
      }, 150);
    };

    if (closeGalleryLightbox) {
      closeGalleryLightbox.addEventListener('click', hideGalleryLightbox);
    }

    galleryLightbox.addEventListener('click', (e) => {
      if (e.target === galleryLightbox) {
        hideGalleryLightbox();
      }
    });

    // Zoom Lightbox Close Handlers
    const hideZoomLightbox = () => {
      const zoomContent = zoomLightbox.querySelector('.zoom-lightbox-content');
      if (zoomContent) {
        zoomContent.style.transform = 'scale(0.9)';
        zoomContent.style.opacity = '0';
      }
      setTimeout(() => {
        zoomLightbox.classList.remove('active');
        zoomLightboxImg.src = '';
        trapFocus(galleryLightbox); // Restore focus trap to parent gallery lightbox
        if (closeGalleryLightbox) closeGalleryLightbox.focus();
      }, 150);
    };

    if (closeZoomLightbox) {
      closeZoomLightbox.addEventListener('click', hideZoomLightbox);
    }

    zoomLightbox.addEventListener('click', (e) => {
      if (e.target === zoomLightbox) {
        hideZoomLightbox();
      }
    });

    // Escape Key to close either modal
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        if (zoomLightbox && zoomLightbox.classList.contains('active')) {
          hideZoomLightbox();
        } else if (galleryLightbox && galleryLightbox.classList.contains('active')) {
          hideGalleryLightbox();
        }
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

  // 4.5. BRAND LOGO LIGHTBOX MODAL (RESTORED WITH ACCESSIBILITY SUPPORTS)
  const logoLinks = document.querySelectorAll('.logo-img-link');
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
              <button id="closeLogoLightbox" style="position: absolute; top: -65px; left: 50%; transform: translateX(-50%); background: #16161a; border: 1.5px solid rgba(255,255,255,0.15); color: #fff; padding: 10px 24px; border-radius: 30px; font-size: 14px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 8px; font-family: var(--font-headings); box-shadow: 0 4px 20px rgba(0,0,0,0.5); transition: all 0.2s ease; outline: none; white-space: nowrap;">
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
            closeBtn.style.borderColor = 'var(--accent-red)';
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
        trapFocus(logoModal);
        
        const closeBtn = document.getElementById('closeLogoLightbox');
        if (closeBtn) closeBtn.focus();
        
        const contentEl = document.getElementById('logoLightboxContent');
        setTimeout(() => {
          contentEl.style.transform = 'scale(1)';
          contentEl.style.opacity = '1';
        }, 10);
      });
    });
  }

  // 6. LIVE GOOGLE REVIEWS COUNTER
  async function updateLiveReviewCount() {
    const reviewEl = document.getElementById('live-review-count');
    if (!reviewEl) return;
    
    try {
      const placeId = 'ChIJc5Cv4o-DXjkRpJpGY9eUkuA';
      const proxyUrl = 'https://api.allorigins.win/get?url=';
      const targetUrl = encodeURIComponent(`https://www.google.com/search?q=Lambodar+Motors+Gota+Ahmedabad`);
      
      const response = await fetch(`${proxyUrl}${targetUrl}`);
      if (response.ok) {
        const data = await response.json();
        const html = data.contents;
        
        const match = html.match(/(\d+)\s+Google\s+reviews/i) || html.match(/(\d+)\s+reviews/i);
        if (match && match[1]) {
          const count = parseInt(match[1], 10);
          if (count > 29) {
            reviewEl.textContent = count;
            return;
          }
        }
      }
    } catch (e) {
      console.warn('Live review count fetch failed, using fallback:', e);
    }
  }
  
  // Active nav link detection
  const currentPath = window.location.pathname;
  const currentFile = currentPath.substring(currentPath.lastIndexOf('/') + 1);
  const desktopNavLinks = document.querySelectorAll('.nav-menu a');
  desktopNavLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && (href === currentFile || href === currentPath)) {
      link.classList.add('nav-active');
    }
  });

  // Back to top button logic
  const backToTopBtn = document.querySelector('.back-to-top');
  if (backToTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 400) {
        backToTopBtn.classList.add('visible');
      } else {
        backToTopBtn.classList.remove('visible');
      }
    });

    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  updateLiveReviewCount();
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

