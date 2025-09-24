<template>
  <v-main>
    <v-container>
      <v-row>
        <v-col cols="12" class="text-center">
          <h1 class="text-h3 font-weight-bold text-primary mb-2">Search Suburb</h1>
          <p class="subtitle text-body-1 text-grey-darken-1 mb-6">
            Discover motorbike theft hotspots in Melbourne suburbs and find the safest places to park your bike.
          </p>

          <SearchBar
            v-model="searchQuery"
            @search="showStaticReport"
            @select="handleSuburbSelect"
          />
        </v-col>
      </v-row>

      <v-row v-if="selectedSuburb">
        <v-col
          cols="12"
          md="3"
        >
          <v-sheet
            rounded="lg"
            class="pa-4"
            color="white"
          >
            <ScoreCard
              :suburb="selectedSuburb.suburb"
              :score="safetyScore"
            />
          </v-sheet>
        </v-col>

        <v-col
          cols="12"
          md="6"
        >
          <v-sheet
            rounded="lg"
            class="pa-4"
            color="white"
          >
            <ParkingFeed
              ref="parkingFeedRef"
              :postcode="selectedSuburb.postcode"
              :suburb="selectedSuburb.suburb"
            />
          </v-sheet>
        </v-col>

        <v-col
          cols="12"
          md="3"
        >
          <v-sheet
            rounded="lg"
            class="pa-4 mb-4"
            color="white"
          >
            <ParkingLocationForm
              :postcode="selectedSuburb.postcode"
              :suburb="selectedSuburb.suburb"
              @submit="handleParkingSubmit"
            />
          </v-sheet>

          <v-sheet
            rounded="lg"
            class="pa-4 text-center"
            color="white"
          >
            <v-btn color="primary" variant="flat" size="large" rounded="lg" @click="showResources = true">
              Resources & Contacts
            </v-btn>
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
  </v-main>

    <ResourcesModal
      v-if="selectedSuburb"
      :show="showResources"
      :suburb="selectedSuburb.suburb"
      @close="showResources = false"
    />

    <v-dialog v-model="showSuccessDialog" max-width="500" persistent>
      <v-card>
        <v-card-text class="text-center pa-6">
          <v-icon
            color="success"
            size="80"
            class="mb-4"
          >
            mdi-check-circle
          </v-icon>
          <h3 class="text-h5 mb-2">Thank you!</h3>
          <p class="text-body-1 mb-0">
            {{ successMessage }}
          </p>
        </v-card-text>
        <v-card-actions class="justify-center pb-4">
          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            @click="showSuccessDialog = false"
          >
            Got it
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showErrorDialog" max-width="500" persistent>
      <v-card>
        <v-card-text class="text-center pa-6">
          <v-icon
            color="error"
            size="80"
            class="mb-4"
          >
            mdi-alert-circle
          </v-icon>
          <h3 class="text-h5 mb-2">Error</h3>
          <p class="text-body-1 mb-0">
            {{ errorMessage }}
          </p>
        </v-card-text>
        <v-card-actions class="justify-center pb-4">
          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            @click="showErrorDialog = false"
          >
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import SearchBar from './components/SearchBar.vue';
import ScoreCard from './components/ScoreCard.vue';
import ResourcesModal from './components/ResourcesModal.vue';
import ParkingLocationForm from './components/ParkingLocationForm.vue';
import ParkingFeed from './components/ParkingFeed.vue';

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
const showSuccessDialog = ref(false);
const showErrorDialog = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const parkingFeedRef = ref<any>(null);

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

const handleParkingSubmit = async (data: any) => {
  try {
    const response = await fetch('/api/v1/parking', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const result = await response.json();
      console.log('Parking location submitted:', result);
      successMessage.value = `Parking location successfully added: ${data.address}`;
      showSuccessDialog.value = true;

      // Refresh the parking feed
      if (parkingFeedRef.value) {
        parkingFeedRef.value.fetchSubmissions();
      }
    } else {
      const error = await response.json();
      console.error('Submission error:', error);
      errorMessage.value = error.detail || 'Failed to add parking location. Please try again.';
      showErrorDialog.value = true;
    }
  } catch (error) {
    console.error('Network error:', error);
    errorMessage.value = 'Failed to submit parking location. Please check your connection and try again.';
    showErrorDialog.value = true;
  }
};

</script>

<style scoped>
.sr-only {
  position: absolute !important;
  height: 1px; width: 1px;
  overflow: hidden; clip: rect(1px, 1px, 1px, 1px);
  white-space: nowrap; border: 0; padding: 0; margin: -1px;
}
</style>
