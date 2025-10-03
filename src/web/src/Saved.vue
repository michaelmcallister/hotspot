<template>
  <v-main>
    <v-container class="pt-1 pt-md-3 pb-2 pb-md-8">
    <PageHero
      title="Saved Parking"
      subtitle="Your favourite parking locations"
      icon="mdi-star"
    />

    <div v-if="loading" class="parking-feed-container">
      <v-card class="parking-feed">
        <v-card-title class="d-flex align-center">
          <v-icon size="20" class="mr-2">mdi-star</v-icon>
          <span>Saved Parking Locations</span>
          <v-chip size="small" class="ml-auto">0</v-chip>
        </v-card-title>

        <v-divider />

        <v-card-text class="pa-3">
          <v-skeleton-loader
            v-for="n in 2"
            :key="n"
            type="list-item-three-line"
            class="mb-2"
          />
        </v-card-text>
      </v-card>
    </div>


   <v-empty-state v-else-if="savedParkingData.length === 0">
      <template v-slot:media>
        <v-icon size="64" color="grey-lighten-1">mdi-star-outline</v-icon>
      </template>
      <template v-slot:title>
        <h3 class="text-grey">No saved parking locations yet</h3>
      </template>
      <template v-slot:text>
        <p class="text-grey">Star parking locations to save them here</p>
      </template>
    </v-empty-state> 

    <div v-else class="parking-feed-container">
      <v-card class="parking-feed">
        <v-card-title class="d-flex align-center">
          <v-icon size="20" class="mr-2">mdi-star</v-icon>
          <span>Saved Parking Locations</span>
          <v-chip size="small" class="ml-auto">{{ savedParkingData.length }}</v-chip>
        </v-card-title>

        <v-divider></v-divider>

        <v-card-text class="pa-3">
          <ParkingCard
            v-for="parking in savedParkingData"
            :key="parking.parking_id"
            :submission="parking"
            @update:favourite="handleFavouriteUpdate"
          />
        </v-card-text>
      </v-card>
    </div>
    </v-container>
  </v-main>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import ParkingCard from './components/ParkingCard.vue';
import PageHero from './components/PageHero.vue';
import { parkingService } from './services';
import { getFavouriteIds, getCachedParkingData, setCachedParkingData } from './utils';

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

const savedParkingData = ref<ParkingSubmission[]>([]);
const loading = ref(false);

const fetchSavedParking = async () => {
  loading.value = true;

  try {
    const favouriteIds = getFavouriteIds();
    if (favouriteIds.length > 0) {
        const allPostcodes = new Set<string>();
        const parkingByPostcode: Map<string, ParkingSubmission[]> = new Map();

        let cachedData = getCachedParkingData();

        for (const id of favouriteIds) {
          if (cachedData[id]) {
            const parking = cachedData[id];
            if (parking.postcode) {
              allPostcodes.add(parking.postcode);
              if (!parkingByPostcode.has(parking.postcode)) {
                parkingByPostcode.set(parking.postcode, []);
              }
              parkingByPostcode.get(parking.postcode)?.push(parking);
            }
          }
        }

        const allParkingData: ParkingSubmission[] = [];

        for (const postcode of allPostcodes) {
          try {
            const postcodeParking = await parkingService.getParkingByPostcode(postcode);
            for (const parking of postcodeParking) {
              if (favouriteIds.includes(parking.parking_id)) {
                allParkingData.push(parking);
                if (!cachedData[parking.parking_id]) {
                  cachedData[parking.parking_id] = parking;
                }
              }
            }
          } catch (error) {
            console.error(`Failed to fetch parking for postcode ${postcode}:`, error);
            const cachedPostcodeData = parkingByPostcode.get(postcode);
            if (cachedPostcodeData) {
              allParkingData.push(...cachedPostcodeData);
            }
          }
        }

        setCachedParkingData(cachedData);
        savedParkingData.value = allParkingData;
      }
  } catch (error) {
    // Fine for now, TODO: proper error handling (show a popup?)
    console.error('Failed to fetch saved parking:', error);
  } finally {
    loading.value = false;
  }
};

const handleFavouriteUpdate = () => {
  const favouriteIds = new Set(getFavouriteIds());
  if (favouriteIds.size > 0) {
    savedParkingData.value = savedParkingData.value.filter(
      parking => favouriteIds.has(parking.parking_id)
    );
  } else {
    savedParkingData.value = [];
  }
};

onMounted(() => {
  fetchSavedParking();
});

watch(() => localStorage.getItem('parkingFavourites'), () => {
  fetchSavedParking();
});
</script>

<style scoped>
.saved-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.parking-feed-container {
  margin-top: 2rem;
}

.parking-feed {
  max-width: 800px;
  margin: 0 auto;
}
</style>
