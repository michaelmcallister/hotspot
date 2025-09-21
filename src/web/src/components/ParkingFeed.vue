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

    <v-card-text v-else class="pa-3">
      <ParkingCard
        v-for="submission in submissions"
        :key="submission.parking_id"
        :submission="submission"
      />
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import ParkingCard from './ParkingCard.vue';

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
.parking-feed {
  max-width: 800px;
  margin: 0 auto;
}
</style>
