<template>
  <v-card class="mx-auto pa-6 text-center" max-width="400" elevation="1" aria-labelledby="score-title" data-testid="safety-score">
    <div id="score-title" class="suburb-name">{{ suburb }}</div>
    <div class="safety-score" :class="scoreColourClass">
      {{ score }}<span class="score-suffix">/100</span>
    </div>
    
    <!-- Safety Score with Tooltip -->
    <div class="score-label-container">
      <div class="score-label">Safety Score</div>
      <v-tooltip location="top">
        <template v-slot:activator="{ props }">
          <v-btn 
            v-bind="props"
            icon 
            size="x-small"
            variant="text"
            color="grey"
            @click="goToFAQ"
            class="ml-1 info-btn"
          >
            <v-icon size="18">mdi-information</v-icon>
          </v-btn>
        </template>
        <span>Click to learn more about safety scores</span>
      </v-tooltip>
    </div>

    <v-chip :color="chipColour" variant="tonal" size="small" class="mb-4 font-weight-bold">
      {{ riskLabel }}
    </v-chip>
  </v-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { safetyLabel, safetyColour } from '../utils/safety';

const router = useRouter();

const props = defineProps<{
  suburb: string
  score: number
}>();

const riskLabel = computed(() => safetyLabel(props.score))
const chipColour = computed(() => safetyColour(props.score))

const scoreColourClass = computed(() =>
  props.score >= 75 ? 'score-high' :
  props.score >= 50 ? 'score-medium' :
  'score-low'
)

const goToFAQ = () => {
  router.push('/faq');
};
</script>

<style scoped>
.suburb-name {
  color: rgb(var(--v-theme-on-surface));
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: .25rem;
}
.safety-score {
  font-size: 3.25rem;
  font-weight: 800;
  margin: .25rem 0 0;
}

.score-suffix {
  color: rgb(var(--v-theme-on-surface-variant));
  font-size: 1.5rem;
  font-weight: 400;
}

.score-high {
  color: rgb(var(--v-theme-success));
}

.score-medium {
  color: rgb(var(--v-theme-warning));
}

.score-low {
  color: rgb(var(--v-theme-error));
}

.score-label-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  margin-bottom: .6rem;
}

.score-label {
  color: rgb(var(--v-theme-on-surface));
  opacity: 0.6;
}

.info-btn {
  min-width: 24px;
  height: 24px;
}

.info-btn .v-icon {
  font-size: 18px;
}
</style>