<template>
  <div class="top-suburbs">
    <h1 class="text-h3 font-weight-bold text-primary mb-2">Top Suburbs</h1>
    <p class="subtitle text-body-1 text-grey-darken-1 mb-6">Explore suburbs and LGAs ranked by safety score.</p>

    <v-toolbar class="mb-4 bg-transparent" density="comfortable" elevation="0" rounded="lg">
      <v-spacer />
      <v-toolbar-items>
        <div class="d-flex align-center flex-wrap">
          <v-select
            class="mx-2"
            label="Scope"
            :items="scopes"
            v-model="scope"
            density="comfortable"
            variant="outlined"
            hide-details="auto"
          />
          <v-select
            class="mx-2"
            label="Order"
            :items="orders"
            v-model="order"
            density="comfortable"
            variant="outlined"
            hide-details="auto"
          />
          <v-text-field
            class="mx-2"
            label="Limit"
            type="number"
            v-model.number="limit"
            :min="1"
            :max="200"
            density="comfortable"
            variant="outlined"
            hide-details="auto"
          />
        </div>
      </v-toolbar-items>
    </v-toolbar>

    <v-alert v-if="error" type="error" class="mb-3" density="compact">
      {{ error }}
    </v-alert>

    <v-data-table
      :headers="headers"
      :items="items"
      :loading="loading"
      loading-text="Loading data..."
      class="elevation-1"
      hover
      density="comfortable"
    >
      <template #item.safety_score="{ item }">
        <div class="d-inline-flex align-center">
          <span class="mr-2">{{ item.safety_score }}</span>
          <v-chip :color="safetyColor(item.safety_score)" variant="tonal" size="small" label>
            {{ safetyLabel(item.safety_score) }}
          </v-chip>
        </div>
      </template>
      <template #item.avg_safety="{ item }">
        <div class="d-inline-flex align-center">
          <span class="mr-2">{{ item.avg_safety }}</span>
          <v-chip :color="safetyColor(item.avg_safety)" variant="tonal" size="small" label>
            {{ safetyLabel(item.avg_safety) }}
          </v-chip>
        </div>
      </template>
    </v-data-table>
  </div>
  
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { safetyLabel, safetyColor } from './utils/safety'

type Scope = 'postcode' | 'lga'
type Order = 'asc' | 'desc'

const scopes = [
  { title: 'Postcode', value: 'postcode' },
  { title: 'LGA', value: 'lga' },
]
const orders = [
  { title: 'Descending', value: 'desc' },
  { title: 'Ascending', value: 'asc' },
]

const scope = ref<Scope>('postcode')
const order = ref<Order>('desc')
const limit = ref<number>(20)

const headers = computed(() => {
  return scope.value === 'postcode'
    ? [
        { title: 'Postcode', key: 'postcode' },
        { title: 'Suburb', key: 'suburb' },
        { title: 'LGA', key: 'lga' },
        { title: 'Safety Score', key: 'safety_score' },
      ]
    : [
        { title: 'LGA', key: 'lga' },
        { title: 'Average Safety', key: 'avg_safety' },
        { title: 'Postcodes', key: 'postcode_count' },
      ]
})

const items = ref<any[]>([])
const loading = ref(false)
const error = ref('')

async function fetchData() {
  loading.value = true
  error.value = ''
  try {
    const params = new URLSearchParams({
      scope: scope.value,
      order: order.value,
      limit: String(limit.value ?? 20),
    })
    const res = await fetch(`/api/v1/risk/top?${params.toString()}`)
    if (!res.ok) throw new Error(`Failed to load data (${res.status})`)
    const data = await res.json()
    const rows = Array.isArray(data) ? data : []
    if (scope.value === 'postcode') {
      items.value = rows.map(r => ({
        ...r,
        safety_score: Math.round((1 - Number(r.risk_score)) * 100),
      }))
    } else {
      items.value = rows.map(r => ({
        ...r,
        avg_safety: Math.round((1 - Number(r.avg_risk)) * 100),
      }))
    }
  } catch (e: any) {
    error.value = e?.message ?? 'Unexpected error fetching data'
  } finally {
    loading.value = false
  }
}

watch([scope, order, limit], fetchData, { immediate: true })
</script>

<style scoped>
.top-suburbs {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 1rem 2rem;
}



</style>
