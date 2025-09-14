<template>
  <div class="homepage">
    <h1>Search Suburb</h1>
    <p class="subtitle">
      Discover motorbike theft hotspots in Melbourne suburbs and find the safest places to park your bike.
    </p>

    <SearchBar v-model="searchQuery" @search="showStaticReport" />

    <ScoreCard :suburb="shownSuburb" :score="safetyScore" />

    <FeedbackCard :suburb="shownSuburb" />

    <section class="card actions-card" aria-labelledby="actions-title">
      <h2 id="actions-title" class="sr-only">Actions</h2>
      <div class="actions-row">
        <button @click="findSafeParking" class="btn-primary">
          Find Safe Parking
        </button>
      </div>
    </section>

    <section class="card resources-card" aria-labelledby="resources-title">
      <h2 id="resources-title" class="sr-only">Resources</h2>
      <button @click="showResources = true" class="btn-resources">
        Resources & Contacts
      </button>
    </section>

    <ResourcesModal :show="showResources" :suburb="shownSuburb" @close="showResources = false" />

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import SearchBar from './components/SearchBar.vue';
import ScoreCard from './components/ScoreCard.vue';
import FeedbackCard from './components/FeedbackCard.vue';
import ResourcesModal from './components/ResourcesModal.vue';

const searchQuery = ref('Toorak');
const shownSuburb = ref('Toorak');
const safetyScore = ref(92);

const showResources = ref(false);


const showStaticReport = () => {
  // Demo: always show Toorak; in real app, fetch & update score/risk here
  shownSuburb.value = searchQuery.value.trim() || 'Toorak';
  // Example of changing score if needed:
  // safetyScore.value = 92
};

const findSafeParking = () => {
  console.log(`Finding safe parking for: ${shownSuburb.value}`);
  alert(`Finding safe parking in ${shownSuburb.value}`);
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
