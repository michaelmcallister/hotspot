<template>
  <v-card class="mb-3" elevation="1">
    <v-card-item
      class="clickable-header"
      @click="navigateToSuburb"
    >
      <template v-slot:prepend>
        <v-icon color="primary">mdi-map-marker</v-icon>
      </template>

      <v-card-title class="text-body-1">
        {{ submission.address }}
      </v-card-title>

      <v-card-subtitle class="text-body-2">
        {{ submission.postcode }}
      </v-card-subtitle>

      <template v-slot:append>
        <v-btn
          icon
          variant="plain"
          size="small"
          @click.stop="copyAddress"
          :color="copied ? 'success' : 'grey-lighten-1'"
        >
          <v-icon>
            {{ copied ? 'mdi-check' : 'mdi-content-copy' }}
          </v-icon>
        </v-btn>
        <v-btn
          icon
          variant="plain"
          size="small"
          @click.stop="toggleFavouriteHandler"
        >
          <v-icon
            :color="isFavourite ? 'yellow-darken-2' : 'grey-lighten-1'"
          >
            {{ isFavourite ? 'mdi-star' : 'mdi-star-outline' }}
          </v-icon>
        </v-btn>
      </template>
    </v-card-item>

    <v-card-text class="pt-3 pb-2">
      <div class="d-flex flex-wrap gap-1">
        <v-chip
          size="small"
          :color="getTypeColor(submission.type)"
          label
        >
          <v-icon start size="14">{{ getTypeIcon(submission.type) }}</v-icon>
          {{ formatParkingType(submission.type) }}
        </v-chip>

        <v-chip
          v-if="submission.lighting"
          size="small"
          color="success"
          label
        >
          <v-icon start size="14">mdi-lightbulb</v-icon>
          {{ getLightingLabel(submission.lighting) }}
        </v-chip>

        <v-chip
          v-if="submission.cctv !== null && submission.cctv !== undefined"
          size="small"
          variant="outlined"
          label
        >
          <v-icon start size="14">mdi-cctv</v-icon>
          CCTV: {{ submission.cctv === true || submission.cctv === 1 ? 'Yes' : 'No' }}
        </v-chip>
      </div>
    </v-card-text>

    <v-card-actions class="d-flex justify-space-between align-center px-4">
      <div v-if="submission.facilities && submission.facilities.length > 0" class="d-flex flex-wrap gap-1 flex-grow-1">
        <v-chip
          v-for="(facility, index) in visibleFacilities"
          :key="facility.facility_id"
          size="small"
          variant="text"
          class="px-2"
        >
          <v-icon start size="14">{{ getFacilityIcon(facility.facility_name) }}</v-icon>
          {{ facility.facility_name }}
        </v-chip>

        <v-btn
          v-if="submission.facilities.length > 2"
          size="small"
          variant="text"
          color="primary"
          @click="toggleFacilities"
          class="px-2"
        >
          {{ facilitiesExpanded ? 'Show less' : `+${submission.facilities.length - 2} more` }}
          <v-icon end size="14">
            {{ facilitiesExpanded ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
          </v-icon>
        </v-btn>
      </div>
      <v-spacer v-else></v-spacer>
      <v-btn
        size="small"
        variant="text"
        color="grey-darken-1"
        @click="openDirections"
      >
        <v-icon start size="18">mdi-directions</v-icon>
        Directions
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { createSlug, getFavouriteIds, toggleFavourite, getCachedParkingData, setCachedParkingData, formatParkingType, getLightingLabel } from '../utils';

const router = useRouter();

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

const props = defineProps<{
  submission: ParkingSubmission;
}>();

const emit = defineEmits<{
  'update:favourite': [void];
}>();

const favourites = ref<Set<number>>(new Set());
const copied = ref(false);
const facilitiesExpanded = ref(false);

const loadFavourites = () => {
  const favouriteIds = getFavouriteIds();
  favourites.value = new Set(favouriteIds);
};

onMounted(() => {
  loadFavourites();
  window.addEventListener('storage', loadFavourites);
});

const isFavourite = computed(() => {
  return favourites.value.has(props.submission.parking_id);
});

const visibleFacilities = computed(() => {
  if (!props.submission.facilities) return [];
  if (props.submission.facilities.length <= 2 || facilitiesExpanded.value) {
    return props.submission.facilities;
  }
  return props.submission.facilities.slice(0, 2);
});

const toggleFacilities = () => {
  facilitiesExpanded.value = !facilitiesExpanded.value;
};

const copyAddress = async () => {
  const fullAddress = `${props.submission.address}, ${props.submission.suburb} ${props.submission.postcode}`;

  try {
    await navigator.clipboard.writeText(fullAddress);
    copied.value = true;
    setTimeout(() => {
      copied.value = false;
    }, 2000);
  } catch (error) {
    // ignore clipboard copy errors
  }
};

const toggleFavouriteHandler = () => {
  const wasAdded = toggleFavourite(props.submission.parking_id);

  if (wasAdded) {
    // Cache the submission data when adding to favourites
    const cache = getCachedParkingData();
    cache[props.submission.parking_id] = props.submission;
    setCachedParkingData(cache);
    favourites.value.add(props.submission.parking_id);
  } else {
    favourites.value.delete(props.submission.parking_id);
  }

  emit('update:favourite');
  window.dispatchEvent(new Event('storage'));
};


const getTypeColor = (type: string) => {
  const colors: Record<string, string> = {
    'on-street': 'orange',
    'off-street': 'success',
    'secure': 'primary'
  };
  return colors[type] || 'grey';
};

const getTypeIcon = (type: string) => {
  const icons: Record<string, string> = {
    'on-street': 'mdi-road',
    'off-street': 'mdi-parking',
    'secure': 'mdi-shield-check'
  };
  return icons[type] || 'mdi-parking';
};


const getFacilityIcon = (facilityName: string) => {
  const icons: Record<string, string> = {
    'Toilet': 'mdi-toilet',
    'Cafe': 'mdi-coffee',
    'Lockers': 'mdi-locker',
    'Covered parking': 'mdi-home-roof',
    'Security guard': 'mdi-shield-account',
    'Accessible': 'mdi-wheelchair-accessibility'
  };
  return icons[facilityName] || 'mdi-star';
};


const navigateToSuburb = () => {
  const slug = createSlug(props.submission.suburb, props.submission.postcode);
  router.push({ name: 'suburb', params: { slug } });
};

//  This works surprisingly well both providers don't need specifically formatted addresses.
const openDirections = () => {
  const fullAddress = `${props.submission.address}, ${props.submission.suburb}, ${props.submission.postcode}`;
  const encodedAddress = encodeURIComponent(fullAddress);

  const navigationApp = localStorage.getItem('navigationApp') || 'google';

  let directionsUrl: string;

  if (navigationApp === 'waze') {
    directionsUrl = `https://waze.com/ul?q=${encodedAddress}&navigate=yes`;
  } else {
    directionsUrl = `https://www.google.com/maps/dir/?api=1&destination=${encodedAddress}`;
  }

  window.open(directionsUrl, '_blank');
};
</script>

<style scoped>
.gap-1 {
  gap: 0.25rem;
}

.clickable-header {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.clickable-header:hover {
  background-color: rgba(var(--v-theme-primary), 0.05);
}
</style>
