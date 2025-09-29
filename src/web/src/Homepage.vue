<template>
  <v-main>
    <v-container class="pt-1 pt-md-3 pb-2 pb-md-8">

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
        @clear="handleSearchClear"
        class="hero-search-bar"
      />
    </PageHero>

    <div v-if="!selectedSuburb" class="illustration-section">
      <v-container>
        <v-row class="justify-center align-center">
          <v-col cols="12" lg="5" xl="4" class="text-center">
            <div class="d-inline-block">
              <img
                src="/dude.png"
                alt="Rider with motorbike"
                class="dude-illustration"
              />
            </div>
          </v-col>
          <v-col cols="12" md="8" lg="6" xl="6" class="mx-auto">
            <v-sheet rounded="lg" class="pa-4" color="primary-lighten-5" border>
              <h3 class="text-h5 text-primary font-weight-bold mb-3 text-center text-lg-left">Find Safe Parking Spots</h3>
              <p class="text-body-1 mb-3 text-center text-lg-left">
                Discover the safest places to park your motorbike in Melbourne.
                Get safety scores based on real data and contribute to the community
                by sharing your favourite secure parking locations
              </p>
              <div class="text-center text-lg-right">
                <v-btn
                  @click="handleStartTutorial"
                  color="primary"
                  variant="outlined"
                  prepend-icon="mdi-help-circle"
                  size="large"
                >
                  Take a Tour
                </v-btn>
              </div>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </div>

    <v-row v-if="selectedSuburb">
        <v-col cols="12" lg="6" xl="3">
          <v-sheet rounded="lg" class="pa-4" color="white">
            <ScoreCard :suburb="selectedSuburb.suburb" :score="safetyScore" />
          </v-sheet>
        </v-col>

        <v-col cols="12" lg="6" xl="6">
          <v-sheet rounded="lg" class="pa-4" color="white">
            <ParkingFeed
              ref="parkingFeedRef"
              :postcode="selectedSuburb.postcode"
              :suburb="selectedSuburb.suburb"
            />
          </v-sheet>
        </v-col>

        <v-col cols="12" xl="3">
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

  <StatusDialog
    :show="showSuccessDialog"
    type="success"
    title="Thank you!"
    :message="successMessage"
    button-text="Got it"
    @close="showSuccessDialog = false"
  />

  <StatusDialog
    :show="showErrorDialog"
    type="error"
    title="Error"
    :message="errorMessage"
    button-text="OK"
    @close="showErrorDialog = false"
  />
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import SearchBar from './components/SearchBar.vue';
import ScoreCard from './components/ScoreCard.vue';
import ParkingLocationForm from './components/ParkingLocationForm.vue';
import ParkingFeed from './components/ParkingFeed.vue';
import PageHero from './components/PageHero.vue';
import StatusDialog from './components/StatusDialog.vue';
import { searchService, parkingService } from './services';
import { createSlug, lookupSuburbBySlug, riskToSafetyScore } from './utils';
import { useTutorial } from './composables/useTutorial';

const props = defineProps<{
  slug?: string;
}>();

const router = useRouter();
const route = useRoute();
const { startTutorial } = useTutorial();

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

const handleSearchClear = () => {
  selectedSuburb.value = null;
  searchQuery.value = '';
  router.push({ name: 'home' });
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

const handleStartTutorial = () => {
  const performSearch = async (query: string) => {
    selectedSuburb.value = null;
    searchQuery.value = '';
    await router.push({ name: 'home' });

    await new Promise(resolve => setTimeout(resolve, 200));

    searchQuery.value = query;

    try {
      const results = await searchService.search(query);

      if (results.length > 0) {
        selectedSuburb.value = results[0];

        const slug = createSlug(results[0].suburb, results[0].postcode);
        await router.push({ name: 'suburb', params: { slug } });
      }
    } catch (error) {
      console.error('Search error:', error);
    }
  };

  startTutorial(performSearch);
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

.illustration-section {
  margin-top: 3rem;
  margin-bottom: 2rem;
}

.dude-illustration {
  max-width: 300px;
  height: auto;
  object-fit: contain;
}

@media (max-width: 768px) {
  .dude-illustration {
    max-width: 250px;
  }
}

</style>
