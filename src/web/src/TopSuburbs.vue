<template>
  <v-main>
    <v-container class="pt-0 pb-1 pb-md-4">
      <PageHero
        title="Explore"
        subtitle="Find safer parking spots near work, uni, or your favourite ride destinations"
        icon="mdi-map-search"
      />

      <v-row v-if="error">
        <v-col cols="12">
          <v-alert type="error" density="compact">
            {{ error }}
          </v-alert>
        </v-col>
      </v-row>

      <v-row class="mb-3">
        <v-col cols="12">
          <v-alert
            type="info"
            variant="tonal"
            density="comfortable"
            icon="mdi-lightbulb"
            closable
          >
            <strong>Quick tip:</strong> Green zones are your safest bet for overnight parking.
            Check the community submissions in each area to find spots other riders trust.
            Remember, even in safer suburbs, always use a disc lock and park in well-lit areas.
          </v-alert>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <v-card elevation="1">
            <template v-slot:text>
              <v-row class="ma-2">
                <v-col cols="12" sm="8" md="9">
                  <v-text-field
                    v-model="search"
                    :label="searchPlaceholder"
                    prepend-inner-icon="mdi-magnify"
                    variant="outlined"
                    hide-details
                    single-line
                    density="comfortable"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="4" md="3">
                  <v-select
                    label="View by"
                    :items="SCOPE_OPTIONS"
                    v-model="scope"
                    density="comfortable"
                    variant="outlined"
                    hide-details
                  />
                </v-col>
              </v-row>
            </template>
            <v-data-table-server
              :key="tableKey"
              v-model:items-per-page="itemsPerPage"
              :headers="headers"
              :items="serverItems"
              :items-length="totalItems"
              :items-per-page-options="[10, 20, 50, 100]"
              :loading="loading"
              hover
              density="comfortable"
              mobile-breakpoint="sm"
              @update:options="loadItems"
            >
              <template v-slot:loading>
                <v-skeleton-loader :type="`table-row@${itemsPerPage}`"></v-skeleton-loader>
              </template>
              <template v-slot:no-data>
                <v-empty-state>
                  <template v-slot:media>
                    <v-icon size="64" color="grey-lighten-1">mdi-table-search</v-icon>
                  </template>
                  <template v-slot:title>
                    <h3 class="text-grey">No data found</h3>
                  </template>
                  <template v-slot:text>
                    <p class="text-grey">Try adjusting your search criteria</p>
                  </template>
                </v-empty-state>
              </template>
              <template #item.safety_score="{ item }">
                <div class="d-flex align-center justify-center">
                  <div style="width: 140px;">
                    <v-progress-linear
                      :model-value="item.safety_score"
                      :color="safetyColour(item.safety_score)"
                      height="24"
                      rounded
                      :max="100"
                    >
                      <template v-slot:default>
                        <strong :class="progressTextClass(item.safety_score)">{{ item.safety_score }}%</strong>
                      </template>
                    </v-progress-linear>
                  </div>
                </div>
              </template>
              <template #item.avg_safety="{ item }">
                <div class="d-flex align-center justify-center">
                  <div style="width: 140px;">
                    <v-progress-linear
                      :model-value="item.avg_safety"
                      :color="safetyColour(item.avg_safety)"
                      height="24"
                      rounded
                      :max="100"
                    >
                      <template v-slot:default>
                        <strong :class="progressTextClass(item.avg_safety)">{{ item.avg_safety }}%</strong>
                      </template>
                    </v-progress-linear>
                  </div>
                </div>
              </template>
              <template #item.actions="{ item }">
                <v-btn
                  v-if="scope === 'postcode'"
                  color="primary"
                  variant="outlined"
                  size="small"
                  @click="viewSuburbDetails(item)"
                >
                  View Details
                </v-btn>
                <v-btn
                  v-else-if="scope === 'lga'"
                  color="primary"
                  variant="outlined"
                  size="small"
                  @click="searchByLGA(item.lga)"
                >
                  View Postcodes
                </v-btn>
              </template>
            </v-data-table-server>
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
import { safetyLabel, safetyColour } from './utils/safety'
import { riskService } from './services'
import { createSlug, riskToSafetyScore } from './utils'

const router = useRouter()

type Scope = 'postcode' | 'lga'

const SCOPE_OPTIONS = [
  { title: 'Suburbs', value: 'postcode' as Scope },
  { title: 'Councils', value: 'lga' as Scope },
]

const HEADERS_CONFIG = {
  postcode: [
    { title: 'Postcode', key: 'postcode' },
    { title: 'Suburb', key: 'suburb' },
    { title: 'LGA', key: 'lga' },
    { title: 'Safety Score', key: 'safety_score', align: 'center' },
    { title: '', key: 'actions', sortable: false },
  ],
  lga: [
    { title: 'LGA', key: 'lga' },
    { title: 'Average Safety', key: 'avg_safety', align: 'center' },
    { title: 'Postcodes', key: 'postcode_count' },
    { title: '', key: 'actions', sortable: false },
  ]
}

const DEFAULT_SORT = { postcode: 'safety_score', lga: 'avg_safety' }

const scope = ref<Scope>('postcode')
const itemsPerPage = ref(20)
const serverItems = ref<any[]>([])
const totalItems = ref(0)
const loading = ref(false)
const error = ref('')
const search = ref('')
const debouncedSearch = ref('')
const tableKey = ref(0)

let searchTimeout: ReturnType<typeof setTimeout> | null = null

const headers = computed(() => HEADERS_CONFIG[scope.value])
const searchPlaceholder = computed(() =>
  scope.value === 'postcode'
    ? 'Try "Melbourne" or "3000"'
    : 'Try "Melbourne" or "Yarra"'
)

async function loadItems({ page, itemsPerPage: perPage, sortBy }: any) {
  loading.value = true
  error.value = ''

  try {
    const data = await riskService.getTopRisk({
      scope: scope.value,
      page: String(page),
      itemsPerPage: String(perPage),
      sortBy: sortBy?.[0]?.key || DEFAULT_SORT[scope.value],
      sortOrder: sortBy?.[0]?.order || 'desc',
      ...(debouncedSearch.value && { search: debouncedSearch.value })
    })

    const safetyKey = scope.value === 'postcode' ? 'safety_score' : 'avg_safety'
    const riskKey = scope.value === 'postcode' ? 'risk_score' : 'avg_risk'

    serverItems.value = data.items.map(item => ({
      ...item,
      [safetyKey]: riskToSafetyScore(Number(item[riskKey]))
    }))

    totalItems.value = data.total
  } catch (e: any) {
    error.value = e?.message ?? 'Unexpected error fetching data'
    serverItems.value = []
    totalItems.value = 0
  } finally {
    loading.value = false
  }
}

function viewSuburbDetails(item: any) {
  router.push({ name: 'suburb', params: { slug: createSlug(item.suburb, item.postcode) } })
}

function searchByLGA(lgaName: string) {
  scope.value = 'postcode'
  search.value = lgaName
}

watch(scope, () => {
  serverItems.value = []
  totalItems.value = 0
  debouncedSearch.value = search.value
  tableKey.value++
})

watch(search, (newValue) => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    debouncedSearch.value = newValue
    tableKey.value++
  }, 300)
})

function progressTextClass(value: number) {
  // Use lighter text when the centre is mostly unfilled
  return value >= 60 ? 'text-white' : 'text-medium-emphasis'
}
</script>
