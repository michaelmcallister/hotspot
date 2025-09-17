<template>
  <v-card class="parking-feed">
    <v-card-title class="d-flex align-center">
      <v-icon size="20" class="mr-2">mdi-parking</v-icon>
      <span>Suggested Parking Feed</span>
      <v-chip size="small" class="ml-auto">{{ submissions.length }}</v-chip>
    </v-card-title>

    <v-divider></v-divider>

    <v-card-text v-if="loading" class="text-center py-4">
      <v-progress-circular indeterminate size="32"></v-progress-circular>
    </v-card-text>

    <v-card-text v-else-if="submissions.length === 0" class="text-center py-4">
      <p class="text-grey text-body-2">No parking suggestions yet for this area</p>
    </v-card-text>

    <v-card-text v-else class="submissions-list pa-2 pa-sm-4">
      <v-timeline side="end" density="compact" class="custom-timeline">
        <v-timeline-item
          v-for="submission in submissions"
          :key="submission.parking_id"
          dot-color="success"
          size="small"
        >
          <v-card elevation="0" class="mb-3 submission-card" color="grey-lighten-3">
            <v-card-text class="pa-2 pa-sm-3">

              <div class="d-flex align-center mb-2">
                <v-icon size="18" class="mr-2">mdi-map-marker</v-icon>
                <span class="font-weight-medium text-truncate">{{ submission.address }}</span>
              </div>

              <div class="mb-2 chips-container">
                <v-chip
                  size="small"
                  :color="getTypeColor(submission.type)"
                  class="mr-1 mb-1"
                >
                  <v-icon start size="14">{{ getTypeIcon(submission.type) }}</v-icon>
                  {{ formatType(submission.type) }}
                </v-chip>

                <v-chip
                  v-if="submission.lighting"
                  size="small"
                  color="success"
                  class="mr-1 mb-1"
                >
                  <v-icon start size="14">mdi-lightbulb</v-icon>
                  {{ getLightingLabel(submission.lighting) }}
                </v-chip>

                <v-chip
                  v-if="submission.cctv === true || submission.cctv === 1"
                  size="small"
                  variant="outlined"
                  class="mr-1 mb-1"
                >
                  <v-icon start size="14">mdi-cctv</v-icon>
                  CCTV: Yes
                </v-chip>

                <v-chip
                  v-if="submission.cctv === false || submission.cctv === 0"
                  size="small"
                  variant="outlined"
                  class="mr-1 mb-1"
                >
                  <v-icon start size="14">mdi-cctv</v-icon>
                  CCTV: No
                </v-chip>

                <v-chip
                  v-if="submission.cctv === null || submission.cctv === undefined"
                  size="small"
                  variant="outlined"
                  class="mr-1 mb-1"
                >
                  <v-icon start size="14">mdi-cctv</v-icon>
                  CCTV: Unknown
                </v-chip>
              </div>

              <div v-if="submission.facilities && submission.facilities.length > 0" class="chips-container">
                <v-chip
                  v-for="facility in submission.facilities"
                  :key="facility.facility_id"
                  size="small"
                  variant="outlined"
                  class="mr-1 mb-1"
                >
                  <v-icon start size="14">{{ getFacilityIcon(facility.facility_name) }}</v-icon>
                  {{ facility.facility_name }}
                </v-chip>
              </div>
            </v-card-text>
          </v-card>
        </v-timeline-item>
      </v-timeline>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';

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
  userVote?: string;
}

const props = defineProps<{
  postcode: string;
  suburb?: string;
}>();

const submissions = ref<ParkingSubmission[]>([]);
const loading = ref(false);

const fetchSubmissions = async () => {
  if (!props.postcode) return;

  loading.value = true;
  try {
    const response = await fetch(`/api/v1/parking/${props.postcode}`);
    if (response.ok) {
      submissions.value = await response.json();
    } else {
      submissions.value = [];
    }
  } catch (error) {
    submissions.value = [];
  } finally {
    loading.value = false;
  }
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

watch(() => props.postcode, () => {
  fetchSubmissions();
});

onMounted(() => {
  fetchSubmissions();
});

defineExpose({
  fetchSubmissions
});
</script>

<style scoped>

.custom-timeline :deep(.v-timeline-item__body) {
  padding-bottom: 0;
}

.submission-card {
  min-height: 140px;
  width: 100%;
}

/* Our persona is probably using a mobile device tbh */
@media (max-width: 600px) {
  .submission-card {
    min-height: auto;
  }

  .chips-container {
    display: flex;
    flex-wrap: wrap;
  }

  .custom-timeline :deep(.v-timeline-divider__before),
  .custom-timeline :deep(.v-timeline-divider__after) {
    display: none;
  }

  .custom-timeline :deep(.v-timeline-divider) {
    min-width: 40px;
  }
}

/* Desktop styles */
@media (min-width: 960px) {
  .submission-card {
    min-width: 500px;
  }
}
</style>
