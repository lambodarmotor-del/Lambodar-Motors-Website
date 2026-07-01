/* ==========================================================================
   Lambodar Motors - Admin Reviews Portal Controller
   ========================================================================== */

const PASSCODE = "lambodar2026";

// 1. LOGIN CONTROLLER
window.handleLogin = function() {
  const input = document.getElementById("passcode-input");
  if (!input) return;
  
  if (input.value === PASSCODE) {
    document.getElementById("login-panel").style.display = "none";
    document.getElementById("dashboard-panel").style.display = "block";
    
    // Initialize Dashboard
    loadReviews(); // Defined in reviews.js
    populateAdminList();
    generateAdminExportCode();
    
    // Re-initialize Lucide Icons for dashboard elements
    if (window.lucide) {
      lucide.createIcons();
    }
  } else {
    alert("Incorrect security passcode. Access Denied.");
    input.value = "";
    input.focus();
  }
};

// 2. RENDER ADMIN LIST
function populateAdminList() {
  const container = document.getElementById("reviews-list-container");
  if (!container) return;
  
  container.innerHTML = "";
  
  if (reviewsList.length === 0) {
    container.innerHTML = `<div style="padding: 16px; text-align: center; color: #a0aec0; font-size: 13px;">No reviews found. Add a review to get started!</div>`;
    return;
  }
  
  reviewsList.forEach((review, index) => {
    const item = document.createElement("div");
    item.className = "review-list-item";
    
    const rankLabel = index < 9 
      ? `<strong style="color: #2ecc71; margin-right: 6px;">[#${index + 1} Visible]</strong>` 
      : `<span style="color: #e74c3c; margin-right: 6px;">[#${index + 1} Hidden]</span>`;
      
    item.innerHTML = `
      <div style="flex: 1; padding-right: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
        ${rankLabel} <strong>${review.name}</strong> - "${review.text}"
      </div>
      <button class="btn-delete" onclick="deleteAdminReview('${review.id}')">Delete</button>
    `;
    container.appendChild(item);
  });
}

// 3. CODE EXPORTER
function generateAdminExportCode() {
  const box = document.getElementById("export-box");
  if (!box) return;
  
  box.value = "const DEFAULT_REVIEWS = " + JSON.stringify(reviewsList, null, 2) + ";";
}

// 4. ADD REVIEW
document.getElementById("add-btn").addEventListener("click", () => {
  const nameEl = document.getElementById("new-name");
  const badgeEl = document.getElementById("new-badge");
  const starsEl = document.getElementById("new-stars");
  const textEl = document.getElementById("new-text");
  
  if (!nameEl.value.trim() || !textEl.value.trim()) {
    alert("Please fill in Customer Name and Review Content!");
    return;
  }
  
  const newReview = {
    id: "r_" + Date.now(),
    name: nameEl.value.trim(),
    badge: badgeEl.value.trim() || "Verified Client",
    stars: parseInt(starsEl.value, 10),
    text: textEl.value.trim()
  };
  
  // Unshift to the top of list
  reviewsList.unshift(newReview);
  
  // Save to storage
  localStorage.setItem("lambodar_custom_reviews", JSON.stringify(reviewsList));
  
  // Reset fields
  nameEl.value = "";
  badgeEl.value = "";
  textEl.value = "";
  starsEl.value = "5";
  
  // Refresh view
  populateAdminList();
  generateAdminExportCode();
  
  alert("Review successfully added! It has been set to rank #1.");
});

// 5. DELETE REVIEW
window.deleteAdminReview = function(id) {
  if (!confirm("Are you sure you want to delete this review?")) return;
  
  reviewsList = reviewsList.filter(rev => rev.id !== id);
  localStorage.setItem("lambodar_custom_reviews", JSON.stringify(reviewsList));
  
  populateAdminList();
  generateAdminExportCode();
};

// 6. COPY CODE
document.getElementById("copy-btn").addEventListener("click", () => {
  const box = document.getElementById("export-box");
  if (!box) return;
  
  box.select();
  box.setSelectionRange(0, 99999);
  
  navigator.clipboard.writeText(box.value)
    .then(() => {
      alert("Deploy code copied! Paste inside assets/js/reviews.js to save permanently.");
    })
    .catch(err => {
      console.error("Failed to copy text: ", err);
    });
});

// Load Lucide Icons initially for login screen
document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) {
    lucide.createIcons();
  }
});
