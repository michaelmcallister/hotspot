<template>
  <v-container fluid class="pa-0">
    <v-container class="pt-0 pb-4 pb-sm-8 pb-md-12 px-3 px-sm-4">
      <PageHero
        title="Find Safe Spots"
        subtitle="Simple, rider‑friendly safety scores and trusted places to park around Melbourne"
        icon="mdi-map-search"
      >
        <v-row justify="center">
          <v-col cols="12" sm="11" md="10" lg="8">
            <SearchBar
              ref="searchBarRef"
              v-model="searchQuery"
              @search="showStaticReport"
              @select="handleSuburbSelect"
              @clear="handleSearchClear"
              style="font-size: 1rem;"
            />
          </v-col>
        </v-row>
      </PageHero>

      <v-fade-transition>
        <div v-if="!selectedSuburb">
          <v-row class="mt-4 mt-sm-6 mt-md-8" justify="center">
            <v-col cols="12" sm="11" md="10" lg="8" xl="6">
              <HomeCtaCard @start-tutorial="handleStartTutorial" />
            </v-col>
          </v-row>

          <v-row class="mt-4 mt-sm-6 mt-md-8" justify="center">
            <v-col cols="12" sm="11" md="10" lg="8">
              <StatsStrip
                :total-postcodes="statsDisplay.total_postcodes"
                :total-lgas="statsDisplay.total_lgas"
                :formatted-addresses="formattedAddresses"
                :total-submissions="statsDisplay.total_submissions"
              />
            </v-col>
          </v-row>
        </div>
      </v-fade-transition>
    </v-container>

    <v-fade-transition>
      <v-container
        v-if="selectedSuburb"
        fluid
        class="pa-3 pa-sm-4 pa-md-6"
        :class="{ 'grey lighten-5': $vuetify.display.mdAndUp }"
      >
        <v-row class="mx-auto" :style="{ maxWidth: $vuetify.display.xlAndUp ? '1680px' : '100%' }">
          <v-col cols="12" md="4" lg="3" class="mb-3 mb-md-0">
            <ScoreCard :suburb="selectedSuburb.suburb" :score="safetyScore" />
          </v-col>
          <v-col cols="12" md="8" lg="9">
            <ParkingFeed
              ref="parkingFeedRef"
              :postcode="selectedSuburb.postcode"
              :suburb="selectedSuburb.suburb"
              @parking-submit="handleParkingSubmit"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-fade-transition>

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
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import SearchBar from './components/SearchBar.vue';
import ScoreCard from './components/ScoreCard.vue';
import ParkingFeed from './components/ParkingFeed.vue';
import PageHero from './components/PageHero.vue';
import StatusDialog from './components/StatusDialog.vue';
import HomeCtaCard from './components/HomeCtaCard.vue';
import StatsStrip from './components/StatsStrip.vue';
import { searchService, parkingService } from './services';
import { statsService } from './services/statsService';
import { createSlug, lookupSuburbBySlug, riskToSafetyScore, formatCompactCount } from './utils';
import { useTutorial } from './composables/useTutorial';
import type { SearchResult } from './services/searchService';

const props = defineProps<{
  slug?: string;
}>();

const router = useRouter();
const route = useRoute();
const { startTutorial } = useTutorial();

type Suburb = SearchResult;

const searchQuery = ref('');
const selectedSuburb = ref<Suburb | null>(null);
const showSuccessDialog = ref(false);
const showErrorDialog = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const parkingFeedRef = ref<any>(null);
const searchBarRef = ref<any>(null);
const stats = ref<any | null>(null);

const safetyScore = computed(() => {
  if (!selectedSuburb.value) return 0;
  return riskToSafetyScore(selectedSuburb.value.risk_score);
});

const statsDisplay = computed(() => ({
  total_postcodes: stats.value?.total_postcodes ?? '—',
  total_lgas: stats.value?.total_lgas ?? '—',
  total_addresses: stats.value?.total_addresses ?? 0,
  total_submissions: stats.value?.total_submissions ?? '—',
}));

const formattedAddresses = computed(() => formatCompactCount(statsDisplay.value.total_addresses));

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
    } catch (error) { }
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
      // ignore tutorial search errors in production console
    }
  };

  startTutorial(performSearch);
};

watch(() => [props.slug, route.params.slug], handleRouteChange);
watch(() => route.name, handleRouteChange);

onMounted(() => {
  handleRouteChange();
  statsService.getSummary().then((s) => {
    stats.value = s;
  }).catch(() => {
    stats.value = null;
  });
});
</script>