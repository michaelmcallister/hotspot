<template>
  <v-card class="mx-auto pa-6" max-width="600" elevation="6">
    <h3 class="mb-4">
      <v-icon start>mdi-plus</v-icon>
      Add Parking Location
    </h3>

    <v-form @submit.prevent="handleSubmit">
      <v-autocomplete
        v-model="selectedAddress"
        :items="addressSuggestions"
        :loading="addressLoading"
        :search="addressSearch"
        @update:search="onAddressSearchUpdate"
        variant="outlined"
        density="compact"
        label="Address"
        placeholder="Search for an address..."
        hide-details="auto"
        class="mb-4"
        clearable
        return-object
        item-title="display"
        item-value="value"
      />

      <v-select
        v-model="parkingType"
        :items="parkingTypes"
        variant="outlined"
        density="compact"
        label="Parking Type"
        hide-details="auto"
        class="mb-4"
      />

      <v-select
        v-model="quality"
        :items="qualityOptions"
        variant="outlined"
        density="compact"
        label="Lighting"
        hide-details="auto"
        class="mb-4"
      />

      <v-select
        v-model="cctvStatus"
        :items="cctvOptions"
        variant="outlined"
        density="compact"
        label="CCTV Nearby"
        hide-details="auto"
        class="mb-4"
      />

      <v-autocomplete
        v-model="nearbyFacilities"
        :items="facilityOptions"
        variant="outlined"
        density="compact"
        label="Nearby Facilities (optional)"
        hide-details="auto"
        class="mb-6"
        multiple
        chips
        closable-chips
      />

      <v-btn
        type="submit"
        color="primary"
        variant="flat"
        block
        size="large"
        rounded="lg"
        :loading="submitting"
      >
        Submit
      </v-btn>
    </v-form>
  </v-card>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

interface AddressSuggestion {
  display: string;
  value: string;
}

const props = defineProps<{
  postcode: string;
}>();

const emit = defineEmits<{
  'submit': [data: {
    address: string;
    parkingType: string;
    quality: string;
    cctvStatus: string;
    nearbyFacilities: string[];
  }]
}>();

const selectedAddress = ref<AddressSuggestion | null>(null);
const addressSearch = ref('');
const addressSuggestions = ref<AddressSuggestion[]>([]);
const addressLoading = ref(false);
const parkingType = ref('Kerbside');
const quality = ref('Good');
const cctvStatus = ref('Unknown');
const nearbyFacilities = ref<string[]>([]);
const submitting = ref(false);


// These are just hardcoded for now
const parkingTypes = [
  'On-Street',
  'Off-street',
  'Secure'
];

const qualityOptions = [
  'Excellent',
  'Good',
  'Fair',
  'Poor'
];

const cctvOptions = [
  'Yes',
  'No',
  'Unknown'
];

const facilityOptions = [
  'Toilet',
  'Cafe',
  'Lockers',
  'Covered parking',
  'Security guard',
  'Accessible'
];

let debounceTimer: ReturnType<typeof setTimeout> | undefined;

const onAddressSearchUpdate = (value: string) => {
  addressSearch.value = value;
  if (debounceTimer) clearTimeout(debounceTimer);

  if (!value || value.length < 2) {
    // Show some default addresses when the field is empty/short
    if (props.postcode) {
      fetchAddressSuggestions('');
    } else {
      addressSuggestions.value = [];
    }
    return;
  }

  debounceTimer = setTimeout(() => {
    fetchAddressSuggestions(value);
  }, 300);
};

const fetchAddressSuggestions = async (query: string) => {
  if (!props.postcode) {
    addressSuggestions.value = [];
    return;
  }

  addressLoading.value = true;
  try {
    // Build URL based on whether we have a query
    const url = query
      ? `/api/v1/addresses/${props.postcode}?q=${encodeURIComponent(query)}`
      : `/api/v1/addresses/${props.postcode}`;

    const response = await fetch(url);
    if (response.ok) {
      const results = await response.json();
      addressSuggestions.value = results.map((item: any) => ({
        display: `${item.address}, ${item.suburb} ${item.postcode}`,
        value: item.address
      }));
    } else {
      addressSuggestions.value = [];
    }
  } catch (error) {
    console.error('Address search error:', error);
    addressSuggestions.value = [];
  } finally {
    addressLoading.value = false;
  }
};

const handleSubmit = () => {
  if (!selectedAddress.value) {
    return;
  }

  submitting.value = true;

  const data = {
    address: selectedAddress.value.value,
    parkingType: parkingType.value,
    quality: quality.value,
    cctvStatus: cctvStatus.value,
    nearbyFacilities: nearbyFacilities.value
  };

  emit('submit', data);

  setTimeout(() => {
    submitting.value = false;
  }, 1000);
};
</script>

<style scoped>
h3 {
  color: #111827;
  font-size: 1.125rem;
  font-weight: 600;
  display: flex;
  align-items: center;
}
</style>
