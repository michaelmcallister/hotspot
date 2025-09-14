<template>
  <div class="homepage">
    <h1>Search Suburb</h1>
    <p class="subtitle">
      Discover motorbike theft hotspots in Melbourne suburbs and find the safest places to park your bike.
    </p>

    <SearchBar
      v-model="searchQuery"
      @search="showStaticReport"
      @select="handleSuburbSelect"
    />

    <ScoreCard
      v-if="selectedSuburb"
      :suburb="selectedSuburb.suburb"
      :score="safetyScore"
    />

    <FeedbackCard v-if="selectedSuburb" :suburb="selectedSuburb.suburb" />

    <section v-if="selectedSuburb" class="card actions-card" aria-labelledby="actions-title">
      <h2 id="actions-title" class="sr-only">Actions</h2>
      <div class="actions-row">
        <button @click="findSafeParking" class="btn-primary">
          Find Safe Parking
        </button>
      </div>
    </section>

    <section v-if="selectedSuburb" class="card resources-card" aria-labelledby="resources-title">
      <h2 id="resources-title" class="sr-only">Resources</h2>
      <button @click="showResources = true" class="btn-resources">
        Resources & Contacts
      </button>
    </section>

    <ResourcesModal
      v-if="selectedSuburb"
      :show="showResources"
      :suburb="selectedSuburb.suburb"
      @close="showResources = false"
    />

  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import SearchBar from './components/SearchBar.vue';
import ScoreCard from './components/ScoreCard.vue';
import FeedbackCard from './components/FeedbackCard.vue';
import ResourcesModal from './components/ResourcesModal.vue';

interface Suburb {
  label: string;
  suburb: string;
  postcode: string;
  lga: string;
  risk_score: number;
}

const searchQuery = ref('');
const selectedSuburb = ref<Suburb | null>(null);
const showResources = ref(false);

const safetyScore = computed(() => {
  if (!selectedSuburb.value) return 0;
  // Convert risk_score (0-1) to safety score (0-100)
  // Lower risk = higher safety
  return Math.round((1 - selectedSuburb.value.risk_score) * 100);
});

const handleSuburbSelect = (suburb: Suburb) => {
  selectedSuburb.value = suburb;
};

const showStaticReport = async () => {
  // If user presses enter without selecting from dropdown, search for exact match
  if (searchQuery.value.trim() && !selectedSuburb.value) {
    try {
      const response = await fetch(`/api/v1/search?q=${encodeURIComponent(searchQuery.value)}`);
      if (response.ok) {
        const results = await response.json();
        if (results.length > 0) {
          // Select the first match
          selectedSuburb.value = results[0];
        }
      }
    } catch (error) {
      console.error('Search error:', error);
    }
  }
};

const findSafeParking = () => {
  if (selectedSuburb.value) {
    console.log(`Finding safe parking for: ${selectedSuburb.value.suburb}`);
    alert(`Finding safe parking in ${selectedSuburb.value.suburb}`);
  }
};

</script>

<style scoped>
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

.card {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 25px -10px rgba(2, 8, 23, 0.15);
  padding: 1.6rem;
  margin: 1.25rem auto 0;
  max-width: 720px;
}

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

.resources-card { padding: 1.25rem; }
.btn-resources {
  background: #07a377; color: #fff; border: 2px solid #46e5b0;
}
.btn-resources:hover { background: #46e5b0; }

.sr-only {
  position: absolute !important;
  height: 1px; width: 1px;
  overflow: hidden; clip: rect(1px, 1px, 1px, 1px);
  white-space: nowrap; border: 0; padding: 0; margin: -1px;
}
</style>
