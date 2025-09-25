<template>
  <v-main>
    <v-container>

      <!-- Hero header -->
    <v-row>
      <v-col cols="12">
        <v-sheet
          rounded="xl"
          elevation="1"
          class="px-6 py-10 mb-8 text-center bg-grey-lighten-5"
          style="border: 1px solid rgba(0,0,0,0.08);"
        >
          <div class="d-flex align-center justify-center mb-4">
            <v-avatar size="48" class="mr-3" color="primary" variant="tonal">
              <v-icon size="28" color="primary">mdi-map-search</v-icon>
            </v-avatar>
            <h1 class="text-h3 font-weight-bold text-high-emphasis m-0">
              Search Suburb
            </h1>
          </div>

          <div class="text-subtitle-1 text-medium-emphasis mx-auto" style="max-width: 720px;">
            Discover motorbike theft hotspots in Melbourne suburbs and find the safest places to park your bike.
          </div>

          <!-- Green accent divider -->
          <v-divider
            class="my-6 mx-auto"
            thickness="3"
            color="primary"
            style="max-width: 140px; border-radius: 999px;"
          />

          <!-- Search bar scaled up -->
          <SearchBar
            ref="searchBarRef"
            v-model="searchQuery"
            @search="showStaticReport"
            @select="handleSuburbSelect"
            class="text-h6 py-3 px-4"
          />
        </v-sheet>
      </v-col>
    </v-row>


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
import { searchService, parkingService } from './services';
import { createSlug, parseSlug, riskToSafetyScore } from './utils';

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


const lookupSuburbBySlug = async (slug: string): Promise<Suburb | null> => {
  try {
    // First try to parse the slug to get suburb and postcode
    const parsed = parseSlug(slug);
    if (parsed) {
      // Search using the parsed suburb name
      const results = await searchService.search(parsed.suburb);

      if (results.length > 0) {
        // Try to find exact match by postcode
        const exactMatch = results.find((suburb: Suburb) =>
          suburb.postcode === parsed.postcode
        );
        if (exactMatch) return exactMatch;

        // Fallback to first result if no exact postcode match
        return results[0];
      }
    }

    // Fallback: try searching with the full slug converted to search term
    const searchTerm = slug.replace(/-/g, ' ');
    const results = await searchService.search(searchTerm);
    return results.length > 0 ? results[0] : null;
  } catch (error) {
    console.error('Error looking up suburb by slug:', error);
    return null;
  }
};

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
/* Subtle, brand-leaning gradient block with soft glow */
.hero {
  /* Light green → light cyan; tweak to your palette */
 /* background: linear-gradient(135deg, #e8fff4 0%, #f2fbff 100%); */
  border: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow:
    0 8px 24px rgba(0, 0, 0, 0.06),
    0 12px 32px rgba(16, 185, 129, 0.12); /* primary-tinted glow */
}

/* Circular icon badge matching the header */
.hero-avatar {
  background: white;
  color: var(--v-theme-primary);
  border: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.hero-sub {
  max-width: 760px;
}

.hero-divider {
  max-width: 160px;
  border-radius: 999px;
  background: linear-gradient(90deg, var(--v-theme-primary), transparent);
}
</style>
