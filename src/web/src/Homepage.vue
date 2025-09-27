<template>
  <v-main>
    <v-container class="py-2 py-md-8">

    <PageHero
      title="Search Suburb"
      subtitle="Discover motorbike theft hotspots in Melbourne suburbs and find the safest places to park your bike"
      icon="mdi-map-search"
    >
      <SearchBar
        ref="searchBarRef"
        v-model="searchQuery"
        @search="showStaticReport"
        @select="handleSuburbSelect"
        class="hero-search-bar"
      />
    </PageHero>


      <v-row v-if="selectedSuburb">
        <v-col cols="12" md="3">
          <v-sheet rounded="lg" class="pa-4" color="white">
            <ScoreCard :suburb="selectedSuburb.suburb" :score="safetyScore" />
          </v-sheet>
        </v-col>

        <v-col cols="12" md="6">
          <v-sheet rounded="lg" class="pa-4" color="white">
            <ParkingFeed
              ref="parkingFeedRef"
              :postcode="selectedSuburb.postcode"
              :suburb="selectedSuburb.suburb"
            />
          </v-sheet>
        </v-col>

        <v-col cols="12" md="3">
          <v-sheet rounded="lg" class="pa-4 mb-4" color="white">
            <ParkingLocationForm
              :postcode="selectedSuburb.postcode"
              :suburb="selectedSuburb.suburb"
              @submit="handleParkingSubmit"
            />
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
  </v-main>

  <v-dialog v-model="showSuccessDialog" max-width="500" persistent>
    <v-card>
      <v-card-text class="text-center pa-6">
        <v-icon color="success" size="80" class="mb-4">mdi-check-circle</v-icon>
        <h3 class="text-h5 mb-2">Thank you!</h3>
        <p class="text-body-1 mb-0">{{ successMessage }}</p>
      </v-card-text>
      <v-card-actions class="justify-center pb-4">
        <v-btn color="primary" variant="flat" rounded="lg" @click="showSuccessDialog = false">
          Got it
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog v-model="showErrorDialog" max-width="500" persistent>
    <v-card>
      <v-card-text class="text-center pa-6">
        <v-icon color="error" size="80" class="mb-4">mdi-alert-circle</v-icon>
        <h3 class="text-h5 mb-2">Error</h3>
        <p class="text-body-1 mb-0">{{ errorMessage }}</p>
      </v-card-text>
      <v-card-actions class="justify-center pb-4">
        <v-btn color="primary" variant="flat" rounded="lg" @click="showErrorDialog = false">
          OK
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import SearchBar from './components/SearchBar.vue';
import ScoreCard from './components/ScoreCard.vue';
import ParkingLocationForm from './components/ParkingLocationForm.vue';
import ParkingFeed from './components/ParkingFeed.vue';
import PageHero from './components/PageHero.vue';
import { searchService, parkingService } from './services';
import { createSlug, lookupSuburbBySlug, riskToSafetyScore } from './utils';

const props = defineProps<{
  slug?: string;
}>();

const router = useRouter();
const route = useRoute();

interface Suburb {
  label: string;
  suburb: string;
  postcode: string;
  lga: string;
  risk_score: number;
}

const searchQuery = ref('');
const selectedSuburb = ref<Suburb | null>(null);
const showSuccessDialog = ref(false);
const showErrorDialog = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const parkingFeedRef = ref<any>(null);
const searchBarRef = ref<any>(null);

const safetyScore = computed(() => {
  if (!selectedSuburb.value) return 0;
  return riskToSafetyScore(selectedSuburb.value.risk_score);
});



const handleSuburbSelect = (suburb: Suburb) => {
  selectedSuburb.value = suburb;
  const slug = createSlug(suburb.suburb, suburb.postcode);
  router.push({ name: 'suburb', params: { slug } });
};

const showStaticReport = async () => {
  if (searchQuery.value.trim() && !selectedSuburb.value) {
    try {
      const results = await searchService.search(searchQuery.value);
      if (results.length > 0) {
        selectedSuburb.value = results[0];
      }
    } catch (error) {
      console.error('Search error:', error);
    }
  }
};

const handleParkingSubmit = async (data: any) => {
  try {
    await parkingService.submitParking(data);
    successMessage.value = `Parking location successfully added: ${data.address}`;
    showSuccessDialog.value = true;
    if (parkingFeedRef.value) {
      parkingFeedRef.value.fetchSubmissions();
    }
  } catch (error: any) {
    console.error('Network error:', error);
    errorMessage.value = error.message || 'Failed to submit parking location. Please check your connection and try again.';
    showErrorDialog.value = true;
  }
};

const handleRouteChange = async () => {
  const slug = (props.slug || route.params.slug) as string;

  if (slug && slug !== 'undefined') {
    const suburb = await lookupSuburbBySlug(slug);
    if (suburb) {
      selectedSuburb.value = suburb;
      searchQuery.value = suburb.label;
      if (searchBarRef.value) {
        searchBarRef.value.updateSelection(suburb);
      }
    }
  } else if (route.name === 'home') {
    selectedSuburb.value = null;
    searchQuery.value = '';
    if (searchBarRef.value) {
      searchBarRef.value.updateSelection(null);
    }
  }
};

watch(() => [props.slug, route.params.slug], handleRouteChange);
watch(() => route.name, handleRouteChange);

onMounted(() => {
  handleRouteChange();
});

</script>

<style scoped>
.hero-search-bar {
  max-width: 600px;
  margin: 0 auto;
}

.hero-search-bar :deep(.v-field) {
  font-size: 1.1rem;
}
</style>
