<template>
  <v-card class="parking-feed" color="white" elevation="1">
    <v-tabs
      v-model="tab"
      color="primary"
      grow
    >
      <v-tab value="Parking Feed">
        <v-icon size="20">mdi-parking</v-icon>
        <span class="d-none d-sm-inline ml-2">Parking Feed</span>
        <v-spacer class="d-none d-sm-flex" />
        <v-chip size="small" class="d-none d-sm-flex ml-2">{{ submissions.length }}</v-chip>
      </v-tab>
      <v-tab value="Nearest Suburbs">
        <v-icon size="20">mdi-map-marker-multiple</v-icon>
        <span class="d-none d-sm-inline ml-2">Nearest Suburbs</span>
      </v-tab>
      <v-tab value="Trends">
        <v-icon size="20">mdi-chart-line</v-icon>
        <span class="d-none d-sm-inline ml-2">Trends</span>
      </v-tab>
    </v-tabs>

    <v-tabs-window v-model="tab">
      <v-tabs-window-item value="Parking Feed">
        <v-card-text v-if="loading" class="pa-0">
          <div class="scroll-container pa-3">
            <v-skeleton-loader
              v-for="n in 3"
              :key="n"
              type="list-item-two-line"
              class="mb-2"
            />
          </div>
        </v-card-text>

        <v-card-text v-else-if="submissions.length === 0" class="pa-0">
          <div class="scroll-container pa-3">
            <v-empty-state>
              <template v-slot:media>
                <v-icon size="64" color="grey-lighten-1">mdi-parking</v-icon>
              </template>
              <template v-slot:title>
                <h3 class="text-grey">No parking suggestions yet</h3>
              </template>
              <template v-slot:text>
                <div class="text-center mt-4">
                  <v-btn
                    color="primary"
                    variant="elevated"
                    @click="showAddParkingModal = true"
                    size="large"
                  >
                    <v-icon start>mdi-plus</v-icon>
                    Add First Location
                  </v-btn>
                </div>
              </template>
            </v-empty-state>
          </div>
        </v-card-text>

        <v-card-text v-else class="pa-0">
          <div class="scroll-container pa-3" @scroll="handleSubmissionScroll">
            <div class="d-flex justify-end align-center mb-3">
              <v-btn
                color="primary"
                variant="tonal"
                size="small"
                @click="showAddParkingModal = true"
              >
                <v-icon start size="18">mdi-plus</v-icon>
                Add Location
              </v-btn>
            </div>

            <ParkingCard
              v-for="submission in displayedSubmissions"
              :key="submission.parking_id"
              :submission="submission"
            />

            <div v-if="displayedSubmissions.length < submissions.length" class="text-center py-2">
              <v-btn variant="text" color="primary" @click="loadMoreSubmissions">
                Load More
              </v-btn>
            </div>
          </div>
        </v-card-text>
      </v-tabs-window-item>

      <v-tabs-window-item value="Nearest Suburbs">
        <v-card-text v-if="nearestLoading" class="pa-0">
          <div class="scroll-container pa-3">
            <v-skeleton-loader
              v-for="n in 3"
              :key="n"
              type="list-item-two-line"
              class="mb-2"
            />
          </div>
        </v-card-text>

        <v-card-text v-else-if="nearestSuburbs.length === 0" class="pa-0">
          <div class="scroll-container pa-3 d-flex align-center justify-center">
            <p class="text-grey text-body-1">No nearby suburbs found</p>
          </div>
        </v-card-text>

        <v-card-text v-else class="pa-0">
          <div class="scroll-container pa-3" @scroll="handleScroll">
            <SuburbCard
              v-for="suburb in displayedSuburbs"
              :key="`${suburb.postcode}-${suburb.suburb}`"
              :suburb="suburb"
            />

            <div v-if="displayedSuburbs.length < nearestSuburbs.length" class="text-center py-2">
              <v-btn variant="text" color="primary" @click="loadMoreSuburbs">
                Load More
              </v-btn>
            </div>
          </div>
        </v-card-text>
      </v-tabs-window-item>

      <v-tabs-window-item value="Trends">
        <v-card-text class="pa-0">
          <TrendsCard
            ref="trendsCardRef"
            :postcode="props.postcode"
          />
        </v-card-text>
      </v-tabs-window-item>
    </v-tabs-window>

    <ParkingLocationModal
      :show="showAddParkingModal"
      :postcode="props.postcode"
      :suburb="props.suburb"
      @close="showAddParkingModal = false"
      @submit="handleParkingSubmit"
    />
  </v-card>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import ParkingCard from './ParkingCard.vue';
import SuburbCard from './SuburbCard.vue';
import TrendsCard from './TrendsCard.vue';
import ParkingLocationModal from './ParkingLocationModal.vue';
import { parkingService, postcodeService, searchService } from '../services';

interface Facility {
  facility_id: number;
  facility_name: string;
}

interface ParkingSubmission {
  parking_id: number;
  address: string;
  suburb: string;
  postcode: string;
  type: string;
  lighting: number | null;
  cctv: boolean | null;
  created_at: string;
  facilities: Facility[];
}

interface NearestSuburb {
  postcode: string;
  suburb: string;
  lga: string;
  distance_in_meters: number;
  parking_count?: number;
  risk_score?: number;
}

const route = useRoute();

const props = defineProps<{
  postcode: string;
  suburb?: string;
}>();

const submissions = ref<ParkingSubmission[]>([]);
const displayedSubmissions = ref<ParkingSubmission[]>([]);
const nearestSuburbs = ref<NearestSuburb[]>([]);
const displayedSuburbs = ref<NearestSuburb[]>([]);

const trendsCardRef = ref<any>(null);

const loading = ref(false);
const nearestLoading = ref(false);

const tab = ref('Parking Feed');
const showAddParkingModal = ref(false);

const ITEMS_PER_PAGE = 3;
const currentDisplayCount = ref(ITEMS_PER_PAGE);
const currentSubmissionDisplayCount = ref(ITEMS_PER_PAGE);

const fetchSubmissions = async () => {
  if (!props.postcode) return;

  loading.value = true;
  try {
    submissions.value = await parkingService.getParkingByPostcode(props.postcode);
    displayedSubmissions.value = submissions.value.slice(0, ITEMS_PER_PAGE);
    currentSubmissionDisplayCount.value = ITEMS_PER_PAGE;
  } catch (error) {
    submissions.value = [];
    displayedSubmissions.value = [];
  } finally {
    loading.value = false;
  }
};

const fetchNearestSuburbs = async () => {
  if (!props.postcode) return;

  nearestLoading.value = true;
  try {
    const suburbs = await postcodeService.getNearestSuburbs(props.postcode);

    const suburbsWithData = await Promise.all(
      suburbs.map(async (suburb: NearestSuburb) => {
        let parking_count = 0;
        let risk_score: number | undefined = undefined;

        try {
          const parkingData = await parkingService.getParkingByPostcode(suburb.postcode);
          parking_count = Array.isArray(parkingData) ? parkingData.length : 0;
        } catch (error) {
          console.warn(`Failed to fetch parking count for ${suburb.postcode}:`, error);
        }

        try {
          const searchResults = await searchService.search(suburb.postcode);
          if (searchResults && searchResults.length > 0 && searchResults[0].risk_score !== undefined) {
            risk_score = searchResults[0].risk_score;
          }
        } catch (error) {
          console.warn(`Failed to fetch risk score for ${suburb.suburb}:`, error);
        }

        return {
          ...suburb,
          parking_count,
          risk_score
        };
      })
    );

    nearestSuburbs.value = suburbsWithData;
    displayedSuburbs.value = suburbsWithData.slice(0, ITEMS_PER_PAGE);
    currentDisplayCount.value = ITEMS_PER_PAGE;
  } catch (error) {
    nearestSuburbs.value = [];
    displayedSuburbs.value = [];
  } finally {
    nearestLoading.value = false;
  }
};

const loadMoreSuburbs = () => {
  const nextCount = Math.min(currentDisplayCount.value + ITEMS_PER_PAGE, nearestSuburbs.value.length);

  if (nextCount > currentDisplayCount.value) {
    displayedSuburbs.value = nearestSuburbs.value.slice(0, nextCount);
    currentDisplayCount.value = nextCount;
  }
};

const loadMoreSubmissions = () => {
  const nextCount = Math.min(currentSubmissionDisplayCount.value + ITEMS_PER_PAGE, submissions.value.length);

  if (nextCount > currentSubmissionDisplayCount.value) {
    displayedSubmissions.value = submissions.value.slice(0, nextCount);
    currentSubmissionDisplayCount.value = nextCount;
  }
};

const createScrollHandler = (loadMoreFn: () => void) => (event: Event) => {
  const target = event.target as HTMLElement;
  const { scrollTop, scrollHeight, clientHeight } = target;
  const SCROLL_THRESHOLD = 10;

  if (scrollTop + clientHeight >= scrollHeight - SCROLL_THRESHOLD) {
    loadMoreFn();
  }
};

const handleScroll = createScrollHandler(loadMoreSuburbs);
const handleSubmissionScroll = createScrollHandler(loadMoreSubmissions);

const emit = defineEmits<{
  'parking-submit': [data: any]
}>();

const handleParkingSubmit = (data: any) => {
  emit('parking-submit', data);
  fetchSubmissions(); // Refresh the parking feed
};

watch(() => props.postcode, () => {
  fetchSubmissions();
  fetchNearestSuburbs();
});

watch(() => route.query.tab, (newTab) => {
  if (newTab === 'parking-feed') {
    tab.value = 'Parking Feed';
  }
}, { immediate: true });

onMounted(() => {
  fetchSubmissions();
  fetchNearestSuburbs();
});

defineExpose({
  fetchSubmissions,
  fetchNearestSuburbs
});
</script>

<style scoped>
.parking-feed {
  max-width: 800px;
  margin: 0 auto;
}


.scroll-container {
  height: 500px;
  overflow-y: auto;
}
</style>
