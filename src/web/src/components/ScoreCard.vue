<template>
  <v-card
    class="mx-auto pa-6 text-center"
    max-width="500"
    elevation="1"
    aria-labelledby="score-title"
  >
    <template v-if="isLoading">
      <v-skeleton-loader
        type="heading, subtitle, chip, paragraph"
        class="text-center"
      />
    </template>

    <template v-else>
      <div id="score-title" class="suburb-name">{{ suburb }}</div>
      <div class="safety-score">{{ score }}</div>
      <div class="score-label">Safety Score</div>

      <v-chip
        :color="chipColor"
        variant="tonal"
        size="small"
        class="mb-4 font-weight-bold"
      >
        {{ riskLabel }}
      </v-chip>

      <p class="description">
        <template v-if="avgReady && trend !== 'same'">
          Risk is
          <strong class="delta" :class="trendClass">{{ signedPercent }}</strong>
          {{ trendWord }} than the average.
        </template>
        <template v-else-if="avgReady && trend === 'same'">
          Risk level is about the same as the average.
        </template>
      </p>
    </template>
  </v-card>
</template>

<script setup lang="ts">
  import { computed, onMounted, ref } from 'vue';

  import { statsService } from '../services';
  import { safetyToRiskScore, riskDifferencePercent } from '../utils';
  import { safetyLabel, safetyColor } from '../utils/safety';

  const props = defineProps<{
    suburb: string;
    score: number;
  }>();

  const riskLabel = computed(() => safetyLabel(props.score));
  const chipColor = computed(() => safetyColor(props.score));

  // Loading and data state
  const isLoading = ref(true);
  const avgRisk = ref<number | null>(null);
  const suburbRisk = computed(() => safetyToRiskScore(props.score));

  onMounted(async () => {
    try {
      const data = await statsService.getSummary();
      avgRisk.value = Number(data.avg_postcode_risk);
    } catch (error) {
      console.error('Failed to load stats summary', error);
    } finally {
      isLoading.value = false;
    }
  });

  const avgReady = computed(
    () => avgRisk.value != undefined && avgRisk.value > 0
  );
  const deltaPct = computed(() => {
    if (!avgReady.value) return 0;
    return riskDifferencePercent(suburbRisk.value, avgRisk.value as number);
  });
  const trend = computed(() =>
    deltaPct.value > 0 ? 'higher' : deltaPct.value < 0 ? 'lower' : 'same'
  );
  const trendWord = computed(() =>
    trend.value === 'higher'
      ? 'higher'
      : trend.value === 'lower'
        ? 'lower'
        : 'the same as'
  );
  const trendClass = computed(() =>
    trend.value === 'higher'
      ? 'is-higher'
      : trend.value === 'lower'
        ? 'is-lower'
        : ''
  );
  const signedPercent = computed(() => {
    const sign = deltaPct.value > 0 ? '+' : deltaPct.value < 0 ? '-' : '';
    const absRounded = Math.round(Math.abs(deltaPct.value) * 10) / 10;
    return `${sign}${absRounded}%`;
  });
</script>

<style scoped>
  .suburb-name {
    color: rgb(var(--v-theme-on-surface));
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
  }
  .safety-score {
    color: rgb(var(--v-theme-success));
    font-size: 3.25rem;
    font-weight: 800;
    margin: 0.25rem 0 0;
  }
  .score-label {
    color: rgb(var(--v-theme-on-surface));
    opacity: 0.6;
    margin-bottom: 0.6rem;
  }

  .description {
    color: rgb(var(--v-theme-on-surface));
    opacity: 0.87;
    line-height: 1.6;
    margin: 0 auto;
    max-width: 560px;
    background: rgba(var(--v-theme-on-surface), 0.04);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    border-left: 4px solid rgb(var(--v-theme-success));
  }
  .delta.is-higher {
    color: rgb(var(--v-theme-error));
  }
  .delta.is-lower {
    color: rgb(var(--v-theme-success));
  }
</style>
