<template>
  <v-card class="parking-feed" color="white" elevation="1">
    <v-tabs
      v-model="tab"
      color="primary"
      grow
    >
      <v-tab value="Parking Feed">
        <v-icon size="20" class="mr-2">mdi-parking</v-icon>
        Parking Feed
        <div class="d-flex align-center pa-4">
          <v-chip size="small" class="ml-auto">{{ submissions.length }}</v-chip>
        </div>
      </v-tab>
      <v-tab value="Nearest Suburbs">
        <v-icon size="20" class="mr-2">mdi-map-marker-multiple</v-icon>
        Nearest Suburbs
      </v-tab>
    </v-tabs>

    <v-tabs-window v-model="tab">
      <v-tabs-window-item value="Parking Feed">
        <v-card
          color="white"
          flat
        >

          <v-card-text v-if="loading" class="text-center py-4">
            <v-progress-circular indeterminate size="32"></v-progress-circular>
          </v-card-text>

          <v-empty-state v-else-if="submissions.length === 0">
            <template v-slot:media>
              <v-icon size="64" color="grey-lighten-1">mdi-parking</v-icon>
            </template>
            <template v-slot:title>
              <h3 class="text-grey">No parking suggestions yet</h3>
            </template>
          </v-empty-state>

          <v-card-text v-else class="pa-3">
            <ParkingCard
              v-for="submission in submissions"
              :key="submission.parking_id"
              :submission="submission"
            />
          </v-card-text>
        </v-card>
      </v-tabs-window-item>

      <v-tabs-window-item value="Nearest Suburbs">
        <v-card
          color="white"
          flat
        >

          <v-card-text v-if="nearestLoading" class="text-center py-4">
            <v-progress-circular indeterminate size="32"></v-progress-circular>
          </v-card-text>

          <v-card-text v-else-if="nearestSuburbs.length === 0" class="text-center py-8">
            <p class="text-grey text-body-1">No nearby suburbs found</p>
          </v-card-text>

          <v-card-text v-else class="pa-0">
            <div
              class="suburb-scroll-container pa-3"
              style="max-height: 500px; overflow-y: auto;"
              @scroll="handleScroll"
            >
              <SuburbCard
                v-for="suburb in displayedSuburbs"
                :key="`${suburb.postcode}-${suburb.suburb}`"
                :suburb="suburb"
              />
              <div
                v-if="displayedSuburbs.length < nearestSuburbs.length"
                class="text-center py-2"
              >
                <v-btn
                  variant="text"
                  color="primary"
                  @click="loadMoreSuburbs"
                >
                  Load More
                </v-btn>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-tabs-window-item>
    </v-tabs-window>
  </v-card>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import ParkingCard from './ParkingCard.vue';
import SuburbCard from './SuburbCard.vue';
import { parkingService, postcodeService, riskService } from '../services';

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
const nearestSuburbs = ref<NearestSuburb[]>([]);
const displayedSuburbs = ref<NearestSuburb[]>([]);
const loading = ref(false);
const nearestLoading = ref(false);
const tab = ref('Parking Feed');
const currentDisplayCount = ref(3);

const fetchSubmissions = async () => {
  if (!props.postcode) return;

  loading.value = true;
  try {
    submissions.value = await parkingService.getParkingByPostcode(props.postcode);
  } catch (error) {
    submissions.value = [];
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
          const riskData = await riskService.compareRisk(suburb.postcode);
          if (riskData && riskData.base && riskData.base.risk_score !== undefined) {
            risk_score = riskData.base.risk_score;
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
    displayedSuburbs.value = suburbsWithData.slice(0, 3);
    currentDisplayCount.value = 3;
  } catch (error) {
    nearestSuburbs.value = [];
    displayedSuburbs.value = [];
  } finally {
    nearestLoading.value = false;
  }
};

const loadMoreSuburbs = () => {
  const nextCount = Math.min(currentDisplayCount.value + 3, nearestSuburbs.value.length);

  if (nextCount > currentDisplayCount.value) {
    displayedSuburbs.value = nearestSuburbs.value.slice(0, nextCount);
    currentDisplayCount.value = nextCount;
  }
};

const handleScroll = (event: Event) => {
  const target = event.target as HTMLElement;
  const { scrollTop, scrollHeight, clientHeight } = target;

  if (scrollTop + clientHeight >= scrollHeight - 10) {
    loadMoreSuburbs();
  }
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
</style>
