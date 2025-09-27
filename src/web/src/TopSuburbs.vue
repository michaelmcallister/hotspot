<template>
  <v-main>
    <v-container class="py-2 py-md-8">
      <PageHero
        title="Top Suburbs"
        subtitle="Explore suburbs and LGAs ranked by safety score"
        icon="mdi-trophy"
      />

      <v-row class="mb-4">
        <v-col
          cols="12"
          sm="4"
          md="4"
        >
          <v-select
            label="Scope"
            :items="scopes"
            v-model="scope"
            density="comfortable"
            variant="outlined"
            hide-details="auto"
          />
        </v-col>
        <v-col
          cols="12"
          sm="4"
          md="4"
        >
          <v-select
            label="Order"
            :items="orders"
            v-model="order"
            density="comfortable"
            variant="outlined"
            hide-details="auto"
          />
        </v-col>
        <v-col
          cols="12"
          sm="4"
          md="4"
        >
          <v-text-field
            label="Limit"
            type="number"
            v-model.number="limit"
            :min="1"
            :max="200"
            density="comfortable"
            variant="outlined"
            hide-details="auto"
          />
        </v-col>
      </v-row>

      <v-row v-if="error">
        <v-col cols="12">
          <v-alert type="error" density="compact">
            {{ error }}
          </v-alert>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <v-card elevation="1">
            <v-data-table
              :headers="headers"
              :items="items"
              :loading="loading"
              loading-text="Loading data..."
              hover
              density="comfortable"
              mobile-breakpoint="sm"
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
              <template #item.actions="{ item }">
                <v-btn
                  color="primary"
                  variant="outlined"
                  size="small"
                  @click="viewSuburbDetails(item)"
                >
                  View Details
                </v-btn>
              </template>
            </v-data-table>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
  
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import PageHero from './components/PageHero.vue'
import { safetyLabel, safetyColor } from './utils/safety'
import { riskService } from './services'
import { createSlug, riskToSafetyScore } from './utils'

const router = useRouter()

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
        { title: '', key: 'actions', sortable: false },
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
    const data = await riskService.getTopRisk({
      scope: scope.value,
      order: order.value,
      limit: String(limit.value ?? 20),
    })
    const rows = Array.isArray(data) ? data : []
    if (scope.value === 'postcode') {
      items.value = rows.map(r => ({
        ...r,
        safety_score: riskToSafetyScore(Number(r.risk_score)),
      }))
    } else {
      items.value = rows.map(r => ({
        ...r,
        avg_safety: riskToSafetyScore(Number(r.avg_risk)),
      }))
    }
  } catch (e: any) {
    error.value = e?.message ?? 'Unexpected error fetching data'
  } finally {
    loading.value = false
  }
}


const viewSuburbDetails = (item: any) => {
  const slug = createSlug(item.suburb, item.postcode);
  router.push({ name: 'suburb', params: { slug } });
}

watch([scope, order, limit], fetchData, { immediate: true })
</script>

<style scoped>
</style>
