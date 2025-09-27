<template>
  <v-card class="mx-auto pa-6" max-width="600" elevation="1">
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
        @update:search="onAddressSearchUpdate"
      />

      <v-select
        v-model="parkingType"
        :items="parkingTypes"
        item-title="title"
        item-value="value"
        variant="outlined"
        density="compact"
        label="Parking Type"
        hide-details="auto"
        class="mb-4"
      />

      <v-select
        v-model="quality"
        :items="qualityOptions"
        item-title="title"
        item-value="value"
        variant="outlined"
        density="compact"
        label="Lighting"
        hide-details="auto"
        class="mb-4"
      />

      <v-select
        v-model="cctvStatus"
        :items="cctvOptions"
        item-title="title"
        item-value="value"
        variant="outlined"
        density="compact"
        label="CCTV Nearby"
        hide-details="auto"
        class="mb-4"
      />

      <v-autocomplete
        v-model="nearbyFacilities"
        :items="facilityOptions"
        item-title="title"
        item-value="value"
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
  import { ref } from 'vue';

  import { addressService } from '../services';

  interface AddressSuggestion {
    display: string;
    value: string;
    address: string;
    suburb: string;
    postcode: string;
  }

  const props = defineProps<{
    postcode: string;
    suburb: string;
  }>();

  const emit = defineEmits<{
    submit: [
      data: {
        address: string;
        suburb: string;
        postcode: string;
        type: string;
        lighting: number | null;
        cctv: boolean | null;
        facilities: number[];
      },
    ];
  }>();

  const selectedAddress = ref<AddressSuggestion | null>(null);
  const addressSearch = ref('');
  const addressSuggestions = ref<AddressSuggestion[]>([]);
  const addressLoading = ref(false);
  const parkingType = ref('on-street');
  const quality = ref<number | null>(3);
  const cctvStatus = ref<boolean | null>(null);
  const nearbyFacilities = ref<number[]>([]);
  const submitting = ref(false);

  // Parking types matching API requirements, these are stored as strings in the backend
  const parkingTypes = [
    { title: 'On-Street', value: 'on-street' },
    { title: 'Off-Street', value: 'off-street' },
    { title: 'Secure', value: 'secure' },
  ];

  const qualityOptions = [
    { title: 'Excellent', value: 4 },
    { title: 'Good', value: 3 },
    { title: 'Fair', value: 2 },
    { title: 'Poor', value: 1 },
  ];

  const cctvOptions = [
    { title: 'Yes', value: true },
    { title: 'No', value: false },
    { title: 'Unknown', value: null },
  ];

  // These map with integers in the backend, check create_tables.txt
  const facilityOptions = [
    { title: 'Toilet', value: 1 },
    { title: 'Cafe', value: 2 },
    { title: 'Lockers', value: 3 },
    { title: 'Covered parking', value: 4 },
    { title: 'Security guard', value: 5 },
    { title: 'Accessible', value: 6 },
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
      const results = await addressService.getAddresses(
        props.postcode,
        query || undefined
      );
      addressSuggestions.value = results.map((item) => ({
        display: `${item.address}, ${item.suburb} ${item.postcode}`,
        value: item.address,
        address: item.address,
        suburb: item.suburb,
        postcode: item.postcode,
      }));
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
      address: selectedAddress.value.address,
      suburb: selectedAddress.value.suburb,
      postcode: selectedAddress.value.postcode,
      type: parkingType.value,
      lighting: quality.value,
      cctv: cctvStatus.value,
      facilities: nearbyFacilities.value,
    };

    emit('submit', data);

    setTimeout(() => {
      submitting.value = false;
    }, 1000);
  };
</script>

<style scoped>
  h3 {
    color: rgb(var(--v-theme-on-surface));
    font-size: 1.125rem;
    font-weight: 600;
    display: flex;
    align-items: center;
  }
</style>
