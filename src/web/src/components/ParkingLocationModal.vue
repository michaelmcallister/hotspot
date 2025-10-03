<template>
  <BaseModal
    :show="show"
    title="Add Parking Location"
    max-width="600"
    title-id="parking-modal-title"
    close-aria-label="Close parking form"
    @close="$emit('close')"
  >
    <ParkingLocationForm
      :postcode="postcode"
      :suburb="suburb"
      @submit="handleSubmit"
    />
  </BaseModal>
</template>

<script setup lang="ts">
import BaseModal from './BaseModal.vue';
import ParkingLocationForm from './ParkingLocationForm.vue';

const props = defineProps<{
  show: boolean
  postcode: string
  suburb?: string
}>();

const emit = defineEmits<{
  close: []
  submit: [data: any]
}>();

const handleSubmit = (data: any) => {
  emit('submit', data);
  emit('close');
};
</script>
