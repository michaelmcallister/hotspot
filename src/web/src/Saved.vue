<template>
  <v-container class="pt-0 pb-16 pb-md-20" style="padding-bottom: 200px;">
    <PageHero
      title="Your Spots"
      subtitle="Bookmark trusted places to park and get there fast"
      icon="mdi-bookmark-outline"
    />

    <v-row class="mb-2" justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-toolbar density="comfortable" color="transparent" class="px-0">
          <v-spacer></v-spacer>
          <v-chip-group v-model="selectedFilters" multiple filter class="mr-1">
            <v-chip value="wellLit" variant="outlined" pill size="small">
              <v-icon start size="16">mdi-lightbulb</v-icon>
              Well‑lit
            </v-chip>
            <v-chip value="cctv" variant="outlined" pill size="small">
              <v-icon start size="16">mdi-cctv</v-icon>
              CCTV
            </v-chip>
            <v-chip value="secure" variant="outlined" pill size="small">
              <v-icon start size="16">mdi-shield-lock</v-icon>
              Secure/Off‑street
            </v-chip>
          </v-chip-group>
          <v-btn v-if="selectedFilters.length" size="small" variant="text" @click="selectedFilters = []">Clear</v-btn>
        </v-toolbar>
        <v-divider></v-divider>
      </v-col>
    </v-row>

    <div v-if="loading" class="parking-feed-container mt-8">
      <v-card class="parking-feed mx-auto">
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
        <v-icon size="64" color="grey-lighten-1">mdi-bookmark-outline</v-icon>
      </template>
      <template v-slot:title>
        <h3 class="text-grey">No spots yet</h3>
      </template>
      <template v-slot:text>
        <p class="text-grey">Find a safe place, then tap the star to save it here</p>
      </template>
      <template v-slot:actions>
        <div class="d-flex justify-center">
          <v-btn color="primary" variant="outlined" to="/explore" prepend-icon="mdi-map-search">
            Explore Spots
          </v-btn>
        </div>
      </template>
    </v-empty-state> 

    <div v-else class="parking-feed-container mt-4" style="padding-bottom:200px;">
      <v-card class="parking-feed mx-auto">
        <v-card-title class="d-flex align-center">
          <v-icon size="20" class="mr-2">mdi-bookmark</v-icon>
          <span>Your Spots</span>
          <v-chip size="small" class="ml-auto">{{ filteredSpots.length }}</v-chip>
        </v-card-title>

        <v-divider></v-divider>

        <v-card-text class="pa-3">
          <ParkingCard
            v-for="parking in filteredSpots"
            :key="parking.parking_id"
            :submission="parking"
            @update:favourite="handleFavouriteUpdate"
          />
        </v-card-text>
      </v-card>
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
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
const selectedFilters = ref<string[]>([]);

const filteredSpots = computed(() => {
  if (!selectedFilters.value.length) return savedParkingData.value;
  return savedParkingData.value.filter(p => {
    return selectedFilters.value.every(f => {
      if (f === 'wellLit') return p.lighting !== null && Number(p.lighting) > 0;
      if (f === 'cctv') return p.cctv === true || (p.cctv as any) === 1;
      if (f === 'secure') {
        const hasGuard = Array.isArray(p.facilities) && p.facilities.some(
          (fac: any) => String(fac?.facility_name || '').toLowerCase() === 'security guard'
        );
        return p.type === 'secure' || p.type === 'off-street' || hasGuard;
      }
      return true;
    });
  });
});

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
.parking-feed {
  max-width: 800px;
}
</style>
