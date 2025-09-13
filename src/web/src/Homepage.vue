<template>
  <div class="homepage">
    <h1>Search Suburb</h1>
    <p class="subtitle">
      Discover motorbike theft hotspots in Melbourne suburbs and find the safest places to park your bike.
    </p>
    
    <div class="search-container">
      <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
      <input 
        v-model="searchQuery"
        @keyup.enter="searchSuburb"
        class="search-input" 
        type="text" 
        placeholder="Enter suburb"
      >
    </div>

    <!-- Safety Report Card -->
    <div v-if="showReport" class="report-card">
      <div class="suburb-name">{{ searchQuery }}</div>
      <div class="safety-score">92</div>
      <div class="risk-level">Low Risk</div>
      
      <p class="description">
        Premium suburb with top-tier security and surveillance. Minimal theft risk.
      </p>

      <!-- NEW BUTTONS -->
      <div class="button-group">
        <button @click="findSafeParking" class="btn-primary">
          Find Safe Parking
        </button>
        <button @click="viewHeatMap" class="btn-outline">
          View Heat Map
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const searchQuery = ref('Toorak');
const showReport = ref(true);

const searchSuburb = () => {
  if (searchQuery.value.trim()) {
    showReport.value = true;
  }
};

// NEW FUNCTIONS FOR BUTTONS
const findSafeParking = () => {
  console.log('Finding safe parking for:', searchQuery.value);
  // You'll add navigation here later
  alert(`Finding safe parking in ${searchQuery.value}`);
};

const viewHeatMap = () => {
  console.log('Viewing heat map for:', searchQuery.value);
  // You'll add navigation here later
  alert(`Showing heat map for ${searchQuery.value}`);
};
</script>

<style scoped>
.homepage {
  max-width: 480px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

h1 {
  color: #1f2937;
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 1.5rem;
}

.subtitle {
  color: #6b7280;
  text-align: center;
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.search-container {
  position: relative;
  margin-bottom: 2rem;
}

.search-input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1.1rem;
  transition: border-color 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #42b883;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

.report-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
}

.suburb-name {
  color: #1f2937;
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.safety-score {
  color: #059669;
  font-size: 3.5rem;
  font-weight: 700;
  margin: 0.5rem 0;
}

.risk-level {
  color: #059669;
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.description {
  color: #6b7280;
  line-height: 1.6;
  margin: 1.5rem 0;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
  border-left: 4px solid #42b883;
}

/* NEW BUTTON STYLES */
.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-primary {
  flex: 1;
  background: #42b883;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background: #359f72;
}

.btn-outline {
  flex: 1;
  background: transparent;
  color: #42b883;
  border: 2px solid #42b883;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-outline:hover {
  background: #42b883;
  color: white;
}
</style>