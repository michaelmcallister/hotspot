<template>
  <v-dialog :model-value="show" @update:model-value="onUpdate" max-width="600">
    <v-card>
      <v-card-title class="text-h6 d-flex align-center justify-space-between">
        <span id="resources-modal-title">Safety Resources</span>
        <v-btn icon="mdi-close" variant="text" @click="$emit('close')" aria-label="Close resources" />
      </v-card-title>
      <v-card-text>
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
              href="https://bikefinder.com/en/articles/how-to-avoid-bike-thieves-common-bike-theft-hotspots-and-prevention-tips/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <v-list-item-title>Motorcycle Theft Prevention Guide</v-list-item-title>
              <v-list-item-subtitle>Learn how to protect your motorbike from theft</v-list-item-subtitle>
              <template #append>
                <v-icon icon="mdi-open-in-new" size="small" />
              </template>
            </v-list-item>
            
            <v-list-item 
              clickable
              href="https://edge.sitecorecloud.io/stategovernc45d-cftw-production-c9ca/media/Project/TransportWebsite/Forms/discover-safe-riding.pdf"
              target="_blank"
              rel="noopener noreferrer"
            >
              <v-list-item-title>VicRoads Motorcycle Safety Guide (PDF)</v-list-item-title>
              <v-list-item-subtitle>Official government advice on motorcycle security</v-list-item-subtitle>
              <template #append>
                <v-icon icon="mdi-open-in-new" size="small" />
              </template>
            </v-list-item>
            
            <v-list-item clickable>
              <v-list-item-title>Recent Theft Reports — {{ suburb }}</v-list-item-title>
              <v-list-item-subtitle>Latest reports in your area</v-list-item-subtitle>
            </v-list-item>
            
            <v-list-item 
              clickable
              href="https://www.nationalmotorcycleinsurance.com.au/claims/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <v-list-item-title>Insurance Claims for Stolen Motorcycles</v-list-item-title>
              <v-list-item-subtitle>What to do if your motorcycle is stolen</v-list-item-subtitle>
              <template #append>
                <v-icon icon="mdi-open-in-new" size="small" />
              </template>
            </v-list-item>
          </v-list>
        </div>
      </v-card-text>
      <v-card-actions class="justify-end">
        <v-btn color="primary" @click="$emit('close')">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
const props = defineProps<{
  show: boolean
  suburb: string
}>();

const emit = defineEmits<{
  close: []
}>();

const onUpdate = (val: boolean) => {
  // When dialog requests to close
  if (!val) emit('close');
};
</script>
