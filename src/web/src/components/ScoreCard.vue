<template>
  <v-card class="mx-auto pa-6" max-width="720" elevation="6" aria-labelledby="score-title">
    <div id="score-title" class="suburb-name">{{ suburb }}</div>
    <div class="safety-score">{{ score }}</div>
    <div class="score-label">Safety Score</div>

    <v-chip :color="chipColor" variant="tonal" size="small" class="mb-4 font-weight-bold">
      {{ riskLabel }}
    </v-chip>

    <p class="description">
      <template v-if="avgReady && trend !== 'same'">
        Risk is <strong class="delta" :class="trendClass">{{ signedPercent }}</strong> {{ trendWord }} than the average.
      </template>
      <template v-else-if="avgReady && trend === 'same'">
        Risk level is about the same as the average.
      </template>
    </p>
  </v-card>
  
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { safetyLabel, safetyColor } from '../utils/safety'

const props = defineProps<{
  suburb: string
  score: number
}>();

const riskLabel = computed(() => safetyLabel(props.score))
const chipColor = computed(() => safetyColor(props.score))

// Fetch average postcode risk from the API and compute delta
const avgRisk = ref<number | null>(null)
const suburbRisk = computed(() => 1 - props.score / 100)

onMounted(async () => {
  try {
    const res = await fetch('/api/v1/stats/summary')
    if (res.ok) {
      const data = await res.json()
      avgRisk.value = Number(data.avg_postcode_risk)
    }
  } catch (e) {
    console.error('Failed to load stats summary', e)
  }
})

const avgReady = computed(() => avgRisk.value != null && avgRisk.value > 0)
const deltaPct = computed(() => {
  if (!avgReady.value) return 0
  // percentage difference relative to average
  return ((suburbRisk.value - (avgRisk.value as number)) / (avgRisk.value as number)) * 100
})
const trend = computed(() => (deltaPct.value > 0 ? 'higher' : deltaPct.value < 0 ? 'lower' : 'same'))
const trendWord = computed(() => (trend.value === 'higher' ? 'higher' : trend.value === 'lower' ? 'lower' : 'the same as'))
const trendClass = computed(() => (trend.value === 'higher' ? 'is-higher' : trend.value === 'lower' ? 'is-lower' : ''))
const signedPercent = computed(() => {
  const sign = deltaPct.value > 0 ? '+' : deltaPct.value < 0 ? '-' : ''
  const absRounded = Math.round(Math.abs(deltaPct.value) * 10) / 10
  return `${sign}${absRounded}%`
})
</script>

<style scoped>
.score-card .suburb-name {
  color: #111827;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: .25rem;
}
.safety-score {
  color: #059669;
  font-size: 3.25rem;
  font-weight: 800;
  margin: .25rem 0 0;
}
.score-label {
  color: #6b7280;
  margin-bottom: .6rem;
}

.description {
  color: #4b5563;
  line-height: 1.6;
  margin: 0 auto;
  max-width: 560px;
  background: #f9fafb;
  border-radius: 10px;
  padding: 1rem 1.25rem;
  border-left: 4px solid #10b981;
}
.delta.is-higher { color: #dc2626; }
.delta.is-lower { color: #059669; }
</style>
