/* ==========================================================================
   Lambodar Motors - Dynamic Reviews Loading & Rendering
   ========================================================================== */

// 1. DEFAULT TOP 9 REVIEWS (Pre-loaded)
const DEFAULT_REVIEWS = [
  {
    id: "r1",
    name: "Ujjaval Patel",
    badge: "Verified Client",
    stars: 5,
    text: "The owner, Shailesh Bhai Prajapati, is incredibly knowledgeable, honest, and professional. Finding a mechanic you can truly trust is tough — but Shailesh Bhai always gives the right advice, never suggests unnecessary repairs, and the job is done perfectly every time. My Honda Jazz has been running incredibly smoothly ever since."
  },
  {
    id: "r2",
    name: "Harshil",
    badge: "Verified Client",
    stars: 5,
    text: "One thing I value most in a garage is honesty — that's why I keep coming back to Lambodar Motors. My Dzire had an AC cooling problem with a faulty fan. The team explained the issue clearly and fixed it properly. No unnecessary repairs, no confusion. Just quality work."
  },
  {
    id: "r3",
    name: "Chavada Pruthvisinh",
    badge: "Verified Client",
    stars: 5,
    text: "Very positive experience. Team carefully inspected the vehicle, explained the issues clearly, and suggested the right solution without any pressure. Work completed within the promised time. Staff were polite, knowledgeable, and answered all my questions. Reliable and reasonably priced."
  },
  {
    id: "r4",
    name: "Prakash Joshi",
    badge: "Verified Client",
    stars: 5,
    text: "Best service, well and good experience, 100% positive. Punctual and professional. Services: Battery, Brake repair, AC filter, Oil change, Transmission."
  },
  {
    id: "r5",
    name: "Rakesh Rakesh",
    badge: "Verified Client",
    stars: 5,
    text: "Parts repaired at affordable price and 100% genuine parts used."
  },
  {
    id: "r6",
    name: "Mahesh Patel",
    badge: "Verified Client",
    stars: 5,
    text: "Great AC work. Now AC works perfectly with excellent cooling."
  },
  {
    id: "r7",
    name: "Vraj Patel",
    badge: "Verified Client",
    stars: 5,
    text: "Good support and affordable price for engine repair."
  },
  {
    id: "r8",
    name: "Luv Patel",
    badge: "Google Local Guide",
    stars: 5,
    text: "Good service provider for car spa."
  },
  {
    id: "r9",
    name: "Sanjay Chavda",
    badge: "Verified Client",
    stars: 5,
    text: "Excellent support for denting and painting. Highly recommended for cashless insurance claim processing."
  }
];

// Initialize reviews list
let reviewsList = [];

// 2. LOAD REVIEWS
function loadReviews() {
  const stored = localStorage.getItem("lambodar_custom_reviews");
  if (stored) {
    try {
      reviewsList = JSON.parse(stored);
    } catch (e) {
      console.error("Failed to parse stored reviews, fallback to defaults:", e);
      reviewsList = [...DEFAULT_REVIEWS];
    }
  } else {
    reviewsList = [...DEFAULT_REVIEWS];
    localStorage.setItem("lambodar_custom_reviews", JSON.stringify(reviewsList));
  }
}

// 3. RENDER REVIEWS GRID (Shows top 9 reviews only)
function renderReviewsGrid() {
  const container = document.getElementById("reviews-container");
  if (!container) return;
  
  container.innerHTML = "";
  
  // Slice to only show the top 9 reviews
  const topReviews = reviewsList.slice(0, 9);
  
  topReviews.forEach(review => {
    const card = document.createElement("div");
    card.className = "review-card";
    
    // Construct star text
    const starString = "★".repeat(review.stars) + "☆".repeat(5 - review.stars);
    
    card.innerHTML = `
      <div>
        <div class="review-stars" style="color: #FFD700; margin-bottom: 8px;">${starString}</div>
        <p class="review-text">"${review.text}"</p>
      </div>
      <div class="review-author" style="margin-top: 15px; font-weight: 700; font-size: 15px; color: var(--text-white);">
        ${review.name}
        <span class="review-badge" style="display: block; font-size: 11px; color: var(--text-gray); font-weight: 500; margin-top: 2px;">${review.badge}</span>
      </div>
    `;
    container.appendChild(card);
  });
}

// 4. DOM READY INITIALIZATION
document.addEventListener("DOMContentLoaded", () => {
  loadReviews();
  renderReviewsGrid();
});
