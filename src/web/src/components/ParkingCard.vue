<template>
  <v-card class="mb-3" elevation="1">
    <v-card-item>
      <template v-slot:prepend>
        <v-icon color="primary">mdi-map-marker</v-icon>
      </template>

      <v-card-title class="text-body-1">
        {{ submission.address }}
      </v-card-title>

      <template v-slot:append>
        <v-btn
          icon
          variant="plain"
          size="small"
          @click="toggleFavourite"
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
          {{ formatType(submission.type) }}
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
      <div v-if="submission.facilities && submission.facilities.length > 0" class="d-flex flex-wrap gap-1">
        <v-chip
          v-for="facility in submission.facilities"
          :key="facility.facility_id"
          size="small"
          variant="text"
          class="px-2"
        >
          <v-icon start size="14">{{ getFacilityIcon(facility.facility_name) }}</v-icon>
          {{ facility.facility_name }}
        </v-chip>
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

const loadFavourites = () => {
  const storedFavourites = localStorage.getItem('parkingFavourites');
  if (storedFavourites) {
    favourites.value = new Set(JSON.parse(storedFavourites));
  }
};

onMounted(() => {
  loadFavourites();
  window.addEventListener('storage', loadFavourites);
});

const isFavourite = computed(() => {
  return favourites.value.has(props.submission.parking_id);
});

const toggleFavourite = () => {
  if (isFavourite.value) {
    favourites.value.delete(props.submission.parking_id);
  } else {
    favourites.value.add(props.submission.parking_id);

    const cachedData = localStorage.getItem('parkingDataCache');
    let cache: Record<number, ParkingSubmission> = {};
    if (cachedData) {
      try {
        cache = JSON.parse(cachedData);
      } catch (e) {
        console.error('Failed to parse cache:', e);
      }
    }
    cache[props.submission.parking_id] = props.submission;
    localStorage.setItem('parkingDataCache', JSON.stringify(cache));
  }

  localStorage.setItem('parkingFavourites', JSON.stringify([...favourites.value]));
  emit('update:favourite');
  window.dispatchEvent(new Event('storage'));
};

const formatType = (type: string) => {
  const types: Record<string, string> = {
    'on-street': 'On Street',
    'off-street': 'Off Street',
    'secure': 'Secure'
  };
  return types[type] || type;
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

const getLightingLabel = (lighting: number) => {
  const labels: Record<number, string> = {
    1: 'Poor',
    2: 'Fair',
    3: 'Good',
    4: 'Excellent'
  };
  return labels[lighting] || 'Unknown';
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

//  This works surprisingly well, Google will fill in the blanks on your current location 
const openDirections = () => {
  const fullAddress = `${props.submission.address}, ${props.submission.suburb}, ${props.submission.postcode}`;
  const encodedAddress = encodeURIComponent(fullAddress);
  const googleMapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${encodedAddress}`;
  window.open(googleMapsUrl, '_blank');
};
</script>

<style scoped>
.gap-1 {
  gap: 0.25rem;
}
</style>
