<template>
  <v-card class="parking-feed" color="white" elevation="1">
    <v-tabs
      v-model="tab"
      color="primary"
      grow
    >
      <v-tab value="Parking Feed">
        <v-icon size="20">mdi-parking</v-icon>
        <span class="d-none d-sm-inline ml-2">Parking Feed</span>
        <v-spacer class="d-none d-sm-flex" />
        <v-chip size="small" class="d-none d-sm-flex ml-2">{{ feedData.parking_submissions.length }}</v-chip>
      </v-tab>
      <v-tab value="Nearest Suburbs">
        <v-icon size="20">mdi-shield-check</v-icon>
        <span class="d-none d-sm-inline ml-2">Safer Suburbs</span>
      </v-tab>
      <v-tab value="Trends">
        <v-icon size="20">mdi-chart-line</v-icon>
        <span class="d-none d-sm-inline ml-2">Trends</span>
      </v-tab>
    </v-tabs>

    <v-tabs-window v-model="tab">
      <v-tabs-window-item value="Parking Feed">
        <v-card-text v-if="loading" class="pa-0">
          <div class="scroll-container pa-3">
            <v-skeleton-loader
              v-for="n in 3"
              :key="n"
              type="list-item-two-line"
              class="mb-2"
            />
          </div>
        </v-card-text>

        <v-card-text v-else-if="feedData.parking_submissions.length === 0" class="pa-0">
          <div class="scroll-container pa-3">
            <v-empty-state>
              <template v-slot:media>
                <v-icon size="64" color="grey-lighten-1">mdi-parking</v-icon>
              </template>
              <template v-slot:title>
                <h3 class="text-grey">No parking suggestions yet</h3>
              </template>
              <template v-slot:text>
                <div class="text-center mt-4">
                  <v-btn
                    color="primary"
                    variant="elevated"
                    @click="showAddParkingModal = true"
                    size="large"
                  >
                    <v-icon start>mdi-plus</v-icon>
                    Add First Location
                  </v-btn>
                </div>
              </template>
            </v-empty-state>
          </div>
        </v-card-text>

        <v-card-text v-else class="pa-0">
          <div class="scroll-container pa-3" @scroll="(e) => handleScroll(e, loadMoreSubmissions)">
            <div class="d-flex justify-end align-center mb-3">
              <v-btn
                color="primary"
                variant="tonal"
                size="small"
                @click="showAddParkingModal = true"
              >
                <v-icon start size="18">mdi-plus</v-icon>
                Add Location
              </v-btn>
            </div>

            <ParkingCard
              v-for="submission in displayedSubmissions"
              :key="submission.parking_id"
              :submission="submission"
            />

            <div v-if="displayedSubmissions.length < feedData.parking_submissions.length" class="text-center py-2">
              <v-btn variant="text" color="primary" @click="loadMoreSubmissions">
                Load More
              </v-btn>
            </div>
          </div>
        </v-card-text>
      </v-tabs-window-item>

      <v-tabs-window-item value="Nearest Suburbs">
        <v-card-text v-if="loading" class="pa-0">
          <div class="scroll-container pa-3">
            <v-skeleton-loader
              v-for="n in 3"
              :key="n"
              type="list-item-two-line"
              class="mb-2"
            />
          </div>
        </v-card-text>

        <v-card-text v-else-if="feedData.nearest_safer_suburbs.length === 0" class="pa-0">
          <div class="scroll-container pa-3">
            <v-empty-state>
              <template v-slot:media>
                <v-icon size="64" color="grey-lighten-1">mdi-map-marker-off</v-icon>
              </template>
              <template v-slot:title>
                <h3 class="text-grey">No safer suburbs nearby</h3>
              </template>
              <template v-slot:text>
                <p class="text-grey">This area has one of the lowest risk scores</p>
              </template>
            </v-empty-state>
          </div>
        </v-card-text>

        <v-card-text v-else class="pa-0">
          <div class="scroll-container pa-3" @scroll="(e) => handleScroll(e, loadMoreSuburbs)">
            <SuburbCard
              v-for="suburb in displayedSuburbs"
              :key="`${suburb.postcode}-${suburb.suburb}`"
              :suburb="suburb"
            />

            <div v-if="displayedSuburbs.length < feedData.nearest_safer_suburbs.length" class="text-center py-2">
              <v-btn variant="text" color="primary" @click="loadMoreSuburbs">
                Load More
              </v-btn>
            </div>
          </div>
        </v-card-text>
      </v-tabs-window-item>

      <v-tabs-window-item value="Trends">
        <v-card-text class="pa-0">
          <TrendsCard
            ref="trendsCardRef"
            :postcode="props.postcode"
          />
        </v-card-text>
      </v-tabs-window-item>
    </v-tabs-window>

    <ParkingLocationModal
      :show="showAddParkingModal"
      :postcode="props.postcode"
      :suburb="props.suburb"
      @close="showAddParkingModal = false"
      @submit="handleParkingSubmit"
    />
  </v-card>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import ParkingCard from './ParkingCard.vue'
import SuburbCard from './SuburbCard.vue'
import TrendsCard from './TrendsCard.vue'
import ParkingLocationModal from './ParkingLocationModal.vue'
import { feedService } from '../services'

const route = useRoute()
const props = defineProps<{ postcode: string; suburb?: string }>()
const emit = defineEmits<{ 'parking-submit': [data: any] }>()

const ITEMS_PER_PAGE = 3

const tab = ref('Parking Feed')
const showAddParkingModal = ref(false)
const loading = ref(false)

const feedData = ref({
  parking_submissions: [],
  nearest_safer_suburbs: []
})

const submissionCount = ref(ITEMS_PER_PAGE)
const suburbCount = ref(ITEMS_PER_PAGE)

const displayedSubmissions = computed(() =>
  feedData.value.parking_submissions.slice(0, submissionCount.value)
)

const displayedSuburbs = computed(() =>
  feedData.value.nearest_safer_suburbs.slice(0, suburbCount.value)
)

async function fetchFeedData() {
  if (!props.postcode) return

  loading.value = true
  try {
    const response = await feedService.getPostcodeFeed(props.postcode)
    feedData.value = response
    submissionCount.value = ITEMS_PER_PAGE
    suburbCount.value = ITEMS_PER_PAGE
  } catch {
    feedData.value = { parking_submissions: [], nearest_safer_suburbs: [] }
  } finally {
    loading.value = false
  }
}

const loadMoreSubmissions = () => {
  submissionCount.value = Math.min(
    submissionCount.value + ITEMS_PER_PAGE,
    feedData.value.parking_submissions.length
  )
}

const loadMoreSuburbs = () => {
  suburbCount.value = Math.min(
    suburbCount.value + ITEMS_PER_PAGE,
    feedData.value.nearest_safer_suburbs.length
  )
}

const handleScroll = (event: Event, loadMore: () => void) => {
  const { scrollTop, scrollHeight, clientHeight } = event.target as HTMLElement
  if (scrollTop + clientHeight >= scrollHeight - 10) loadMore()
}

function handleParkingSubmit(data: any) {
  emit('parking-submit', data)
  fetchFeedData()
}

watch(() => props.postcode, fetchFeedData)
watch(() => route.query.tab, (newTab) => {
  if (newTab === 'parking-feed') tab.value = 'Parking Feed'
}, { immediate: true })

onMounted(fetchFeedData)
</script>

<style scoped>
.parking-feed {
  max-width: 800px;
  margin: 0 auto;
}

.scroll-container {
  height: 500px;
  overflow-y: auto;
}
</style>
