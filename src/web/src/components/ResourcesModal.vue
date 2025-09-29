<template>
  <BaseModal
    :show="show"
    title="Safety Resources"
    max-width="600"
    title-id="resources-modal-title"
    close-aria-label="Close resources"
    @close="$emit('close')"
  >
        <div class="mb-4">
          <div class="text-subtitle-1 font-weight-medium mb-2">Emergency Contacts</div>
          <v-list density="comfortable" lines="one">
            <v-list-item>
              <v-list-item-title>Police Emergency</v-list-item-title>
              <v-list-item-subtitle>For immediate emergencies</v-list-item-subtitle>
              <template #append>
                <v-chip color="error" class="font-weight-bold">000</v-chip>
              </template>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Crime Stoppers</v-list-item-title>
              <v-list-item-subtitle>Report crimes anonymously</v-list-item-subtitle>
              <template #append>
                <v-chip color="primary" variant="tonal" class="font-weight-bold">1800 333 000</v-chip>
              </template>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Victoria Police Non-Emergency</v-list-item-title>
              <v-list-item-subtitle>Non-urgent police matters</v-list-item-subtitle>
              <template #append>
                <v-chip color="primary" variant="tonal" class="font-weight-bold">03 9247 6666</v-chip>
              </template>
            </v-list-item>
          </v-list>
        </div>

        <v-divider class="my-4" />

        <div>
          <div class="text-subtitle-1 font-weight-medium mb-2">Helpful Resources</div>
          <v-list density="comfortable">
            <v-list-item 
              clickable
              href="https://nhw.com.au/cars-and-vehicles/prevent-your-motorbike-from-being-stolen/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <v-list-item-title>Theft Prevention Guide (Neighbourhood Watch)</v-list-item-title>
              <v-list-item-subtitle>Practical tips on how to prevent your motorcycle from theft</v-list-item-subtitle>
              <template #append>
                <v-icon icon="mdi-open-in-new" size="small" />
              </template>
            </v-list-item>
            
            <v-list-item 
              clickable
              href="https://www.propertyvault.com.au/motorbikevault/ "
              target="_blank"
              rel="noopener noreferrer"
            >
              <v-list-item-title>Motorbike Property Vault</v-list-item-title>
              <v-list-item-subtitle>Register your motorcycle for free and report if it's stolen</v-list-item-subtitle>
              <template #append>
                <v-icon icon="mdi-open-in-new" size="small" />
              </template>
            </v-list-item>
            
            <v-list-item 
              clickable
              href="https://www.facebook.com/groups/stolen.motorcycles.australia"
              target="_blank"
              rel="noopener noreferrer"
            >
              <v-list-item-title>Stolen Motorcycles Australia (Facebook Group)</v-list-item-title>
              <v-list-item-subtitle>Engage with other riders about stolen motorcycles</v-list-item-subtitle>
              <template #append>
                <v-icon icon="mdi-open-in-new" size="small" />
              </template>
            </v-list-item>
          </v-list>
        </div>
  </BaseModal>
</template>

<script setup lang="ts">
import BaseModal from './BaseModal.vue';

const props = defineProps<{
  show: boolean
  suburb?: string
}>();

const emit = defineEmits<{
  close: []
}>();
</script>
