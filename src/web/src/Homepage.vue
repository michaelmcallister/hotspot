<template>
  <div class="homepage">
    <h1>Search Suburb</h1>
    <p class="subtitle">
      Discover motorbike theft hotspots in Melbourne suburbs and find the safest places to park your bike.
    </p>

    <!-- Search (centered) -->
    <div class="search-container">
      <svg
        class="search-icon"
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        aria-hidden="true"
      >
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
      <input
        v-model="searchQuery"
        class="search-input"
        type="text"
        placeholder="Enter suburb (e.g., Toorak)"
        @keyup.enter="showStaticReport"
        aria-label="Search suburb"
      />
    </div>

    <!-- CARD 1: Safety / Risk -->
    <section class="card score-card" aria-labelledby="score-title">
      <div id="score-title" class="suburb-name">{{ shownSuburb }}</div>
      <div class="safety-score">{{ safetyScore }}</div>
      <div class="score-label">Safety Score</div>

      <div class="risk-chip" :class="riskClass">{{ riskLabel }}</div>

      <p class="description">
        Premium suburb with top-tier security and surveillance. Minimal theft risk.
      </p>
    </section>

    <!-- CARD 2: Accuracy feedback (black text) -->
    <section class="card accuracy-card" aria-labelledby="accuracy-title">
      <p id="accuracy-title" class="feedback-question">
        <strong>Is this score accurate?</strong> Help improve our data:
      </p>

    <div class="feedback-buttons">
  <button
    type="button"
    @click="submitFeedback('safer')"
    :class="['feedback-btn','feels-safer', { active: userFeedback === 'safer' }]"
    :aria-pressed="userFeedback === 'safer' ? 'true' : 'false'"
  >
    👍 Feels Safer
  </button>

  <button
    type="button"
    @click="submitFeedback('less-safe')"
    :class="['feedback-btn','feels-less-safe', { active: userFeedback === 'less-safe' }]"
    :aria-pressed="userFeedback === 'less-safe' ? 'true' : 'false'"
  >
    👎 Less Safe
  </button>
</div>


      <p v-if="feedbackSubmitted" class="feedback-thankyou" aria-live="polite">
        Thank you for your feedback! ✓
      </p>
    </section>

    <!-- CARD 3: Actions (side-by-side) -->
    <section class="card actions-card" aria-labelledby="actions-title">
      <h2 id="actions-title" class="sr-only">Actions</h2>
      <div class="actions-row">
        <button @click="findSafeParking" class="btn-primary">
          Find Safe Parking
        </button>
        <button @click="viewHeatMap" class="btn-outline">
          View Heat Map
        </button>
      </div>
    </section>

    <!-- CARD 4: Resources -->
    <section class="card resources-card" aria-labelledby="resources-title">
      <h2 id="resources-title" class="sr-only">Resources</h2>
      <button @click="showResources = true" class="btn-resources">
        Resources & Contacts
      </button>
    </section>

    <!-- Resources Modal -->
    <div
      v-if="showResources"
      class="modal-overlay"
      @click="showResources = false"
      aria-modal="true"
      role="dialog"
      aria-labelledby="resources-modal-title"
    >
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="showResources = false" aria-label="Close resources">×</button>

        <h1 id="resources-modal-title">Safety Resources</h1>

        <div class="resources-section">
          <h2>Emergency Contacts</h2>

          <div class="contact-card">
            <div class="contact-info">
              <h3>Police Emergency</h3>
              <p>For immediate emergencies</p>
            </div>
            <div class="contact-number">000</div>
          </div>

          <div class="contact-card">
            <div class="contact-info">
              <h3>Crime Stoppers</h3>
              <p>Report crimes anonymously</p>
            </div>
            <div class="contact-number">1800 333 000</div>
          </div>

          <div class="contact-card">
            <div class="contact-info">
              <h3>Victoria Police Non-Emergency</h3>
              <p>Non-urgent police matters</p>
            </div>
            <div class="contact-number">03 9247 6666</div>
          </div>
        </div>

        <div class="divider"></div>

        <div class="resources-section">
          <h2>Helpful Resources</h2>
          <div class="resource-links">
            <a href="#" @click.prevent class="resource-link">
              <span class="link-title">Melbourne Bike Theft Prevention Guide</span>
              <span class="link-desc">Learn how to protect your motorbike from theft</span>
            </a>
            <a href="#" @click.prevent class="resource-link">
              <span class="link-title">VicRoads Motorcycle Security Tips</span>
              <span class="link-desc">Official government advice on motorcycle security</span>
            </a>
            <a href="#" @click.prevent class="resource-link">
              <span class="link-title">Recent Theft Reports — {{ shownSuburb }}</span>
              <span class="link-desc">Latest reports in your area</span>
            </a>
            <a href="#" @click.prevent class="resource-link">
              <span class="link-title">Insurance Claims for Stolen Bikes</span>
              <span class="link-desc">What to do if your motorcycle is stolen</span>
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- HeatMap -->
    <HeatMap
      v-if="showHeatMap"
      :selectedSuburb="shownSuburb"
      @close="showHeatMap = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// --- State ---
const searchQuery = ref('Toorak');
const shownSuburb = ref('Toorak');   // what the report shows
const safetyScore = ref(92);

const showResources = ref(false);
const showHeatMap = ref(false);

const userFeedback = ref<null | 'safer' | 'less-safe'>(null);
const feedbackSubmitted = ref(false);

// --- Derived Risk label/class from score ---
const riskLabel = computed(() => {
  const s = safetyScore.value;
  if (s >= 80) return 'Low Risk';
  if (s >= 50) return 'Medium Risk';
  return 'High Risk';
});
const riskClass = computed(() => {
  const s = safetyScore.value;
  if (s >= 80) return 'low';
  if (s >= 50) return 'med';
  return 'high';
});

// --- Methods ---
const showStaticReport = () => {
  // Demo: always show Toorak; in real app, fetch & update score/risk here
  shownSuburb.value = searchQuery.value.trim() || 'Toorak';
  // Example of changing score if needed:
  // safetyScore.value = 92
};

const submitFeedback = (feedbackType: 'safer' | 'less-safe') => {
  userFeedback.value = feedbackType;
  feedbackSubmitted.value = true;

  // send to analytics/backend here
  console.log(`User feedback: ${feedbackType} for ${shownSuburb.value}`);

  setTimeout(() => {
    feedbackSubmitted.value = false;
    userFeedback.value = null;
  }, 3000);
};

const findSafeParking = () => {
  console.log(`Finding safe parking for: ${shownSuburb.value}`);
  alert(`Finding safe parking in ${shownSuburb.value}`);
};

const viewHeatMap = () => {
  showHeatMap.value = true;
};
</script>

<style scoped>
/* ===== Layout & Base ===== */
.homepage {
  max-width: 880px;         /* desktop-friendly centered column */
  margin: 0 auto;
  padding: 2.5rem 1rem 4rem;
  text-align: center;
  line-height: 1.25;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

h1 {
  color: #111827;
  font-size: 2.75rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}
.subtitle {
  color: #6b7280;
  font-size: 1.05rem;
  line-height: 1.6;
  margin-bottom: 1.75rem;
}

/* ===== Search ===== */
.search-container {
  position: relative;
  margin: 0 auto 2rem;
  max-width: 720px;
}
.search-input {
  width: 80%;
  padding: 1rem 1rem 1rem 3rem;
  border: 2px solid #e5e7eb;
  border-radius: 14px;
  font-size: 1.05rem;
  background: #67686b;
  transition: border-color .2s, box-shadow .2s;
}
.search-input:focus {
  outline: none;
  border-color: #0b1541;
  box-shadow: 0 0 0 4px rgba(37,99,235,.12);
}
.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

/* ===== Card base ===== */
.card {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 25px -10px rgba(2, 8, 23, 0.15);
  padding: 1.6rem;
  margin: 1.25rem auto 0;
  max-width: 720px;
}

/* ===== Card 1: Score ===== */
.score-card .suburb-name {
  color: #111827;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: .25rem;
}
.safety-score {
  color: #059669;
  font-size: 3.25rem;
  font-weight: 800;
  margin: .25rem 0 0;
}
.score-label {
  color: #6b7280;
  margin-bottom: .6rem;
}
.risk-chip {
  display: inline-block;
  padding: .35rem .7rem;
  border-radius: 999px;
  font-size: .85rem;
  font-weight: 700;
  margin: .25rem 0 .9rem;
  border: 1px solid transparent;
}
.risk-chip.low { background:#ecfdf5; color:#047857; border-color:#a7f3d0; }
.risk-chip.med { background:#fff7ed; color:#9a3412; border-color:#fed7aa; }
.risk-chip.high { background:#fef2f2; color:#dc2626; border-color:#fecaca; }

.description {
  color: #4b5563;
  line-height: 1.6;
  margin: 0 auto;
  max-width: 560px;
  background: #f9fafb;
  border-radius: 10px;
  padding: 1rem 1.25rem;
  border-left: 4px solid #10b981;
}

/* ===== Card 2: Accuracy (black text) ===== */
.accuracy-card { padding: 1.25rem; }
.accuracy-card .feedback-question {
  color: #111827; /* black-ish per request */
  margin-bottom: .9rem;
  font-size: 1rem;
}
.feedback-buttons {
  display: flex;
  gap: .75rem;
  justify-content: center;
  flex-wrap: wrap;
}
.feedback-btn {
  min-width: 190px;
  padding: .65rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  background: #fff;
  cursor: pointer;
  transition: all .2s;
  font-weight: 700;
  color: #111827;
}
.feedback-btn:hover { transform: translateY(-1px); }
.feedback-btn.active { border-color: #111827; }

.feels-safer.active { border-color:#10b981; background:#ecfdf5; color:#047857; }
.feels-less-safe.active { border-color:#ef4444; background:#fef2f2; color:#dc2626; }

.feedback-thankyou {
  margin-top: .6rem; color: #10b981; font-weight: 700; font-size: .95rem;
}

/* ===== Card 3: Actions ===== */
.actions-card { padding: 1.25rem; }
.actions-row {
  display: flex;
  gap: 1rem;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}
.btn-primary, .btn-outline, .btn-resources {
  border-radius: 12px;
  font-size: 1.05rem;
  font-weight: 700;
  padding: .9rem 1.4rem;
}
.btn-primary {
  background: #07a377; color: #040d35; border: 2px solid #3cc799;;
}
.btn-primary:hover { background: #46e5b0; }
.btn-outline {
  background: transparent; color: #07a377; border: 2px solid #07a377;
}
.btn-outline:hover { background: #dffff4; color: #07a377; }

/* ===== Card 4: Resources ===== */
.resources-card { padding: 1.25rem; }
.btn-resources {
  background: #07a377; color: #fff; border: 2px solid #46e5b0;
}
.btn-resources:hover { background: #46e5b0; }

/* ===== Modal ===== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}
.modal-content {
  background: #fff;
  padding: 2.2rem;
  border-radius: 12px;
  max-width: 560px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 25px -5px rgba(0,0,0,.15);
  text-align: left;
}
.modal-close {
  position: absolute;
  top: .75rem;
  right: .75rem;
  background: none;
  border: none;
  font-size: 1.6rem;
  cursor: pointer;
  color: #6b7280;
  padding: .25rem .5rem;
}
.modal-content h1 {
  color: #111827;
  font-size: 1.8rem;
  margin-bottom: 1.2rem;
  text-align: center;
}
.modal-content h2 {
  color: #374151;
  font-size: 1.2rem;
  margin: 1.2rem 0 .75rem;
  padding-bottom: .5rem;
  border-bottom: 2px solid #e5e7eb;
}

/* Contact Cards */
.contact-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
  margin-bottom: .75rem;
  border-left: 4px solid #ef4444;
}
.contact-info { flex: 1; }
.contact-info h3 {
  color: #111827;
  font-size: 1rem;
  margin: 0 0 .25rem;
  font-weight: 700;
}
.contact-info p { color:#6b7280; font-size:.9rem; margin:0; }
.contact-number {
  background: #ef4444; color:#fff; padding:.5rem 1rem; border-radius: 20px;
  font-weight: 700; font-size: .95rem; min-width: 80px; text-align: center;
}

/* Resource Links */
.resource-links { display: flex; flex-direction: column; gap: .75rem; }
.resource-link {
  display: block; padding: 1rem; background:#f8fafc; border-radius: 8px;
  text-decoration: none; color: inherit; transition: background-color .2s;
  border-left: 4px solid #3b82f6;
}
.resource-link:hover { background:#eef2ff; }
.link-title { display:block; color:#111827; font-weight:700; font-size:.98rem; margin-bottom:.25rem; }
.link-desc { display:block; color:#6b7280; font-size:.9rem; }

/* Divider */
.divider { height: 1px; background:#e5e7eb; margin: 1.25rem 0; }

/* A11y helper */
.sr-only {
  position: absolute !important;
  height: 1px; width: 1px;
  overflow: hidden; clip: rect(1px, 1px, 1px, 1px);
  white-space: nowrap; border: 0; padding: 0; margin: -1px;
}

/* Responsive tweaks */
@media (max-width: 520px) {
  .safety-score { font-size: 2.6rem; }
  .feedback-btn { min-width: 150px; }
}
</style>
