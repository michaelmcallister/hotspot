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

    <section v-if="selectedSuburb" class="actions-card" aria-labelledby="actions-title">
      <h2 id="actions-title" class="sr-only">Actions</h2>
      <div class="actions-row">
        <v-btn color="primary" variant="flat" size="large" rounded="lg" @click="findSafeParking">
          Find Safe Parking
        </v-btn>
      </div>
    </section>

    <section v-if="selectedSuburb" class="resources-card" aria-labelledby="resources-title">
      <h2 id="resources-title" class="sr-only">Resources</h2>
      <v-btn color="primary" variant="flat" size="large" rounded="lg" @click="showResources = true">
        Resources & Contacts
      </v-btn>
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 1rem 2rem;
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

.actions-card { padding: 1.25rem; }
.actions-row {
  display: flex;
  gap: 1rem;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}
.resources-card { padding: 1.25rem; }

.sr-only {
  position: absolute !important;
  height: 1px; width: 1px;
  overflow: hidden; clip: rect(1px, 1px, 1px, 1px);
  white-space: nowrap; border: 0; padding: 0; margin: -1px;
}
</style>
