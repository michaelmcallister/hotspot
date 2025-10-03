<template>
  <div class="scroll-container pa-3">
    <div v-if="loading">
      <v-skeleton-loader
        v-for="n in 3"
        :key="n"
        type="list-item-two-line"
        class="mb-2"
      />
    </div>

    <v-empty-state v-else-if="!theftData.length">
      <template v-slot:media>
        <v-icon size="64" color="grey-lighten-1">mdi-chart-line</v-icon>
      </template>
      <template v-slot:title>
        <h3 class="text-grey">No theft data available</h3>
      </template>
      <template v-slot:text>
        <p class="text-grey">No historical theft trends found for this postcode</p>
      </template>
    </v-empty-state>

    <div v-else class="d-flex flex-column justify-center" style="height: 100%;">
      <v-card elevation="1" class="mx-auto" style="max-width: 700px;">
        <v-card-text class="pa-6">
          <div class="mb-6 text-center">
            <h2 class="text-h6 mb-2 font-weight-medium">
              Yearly Motor Vehicle Thefts
            </h2>
            <p class="text-body-1 text-medium-emphasis">
              {{ totalThefts }} thefts ({{ yearRange }})
            </p>
          </div>

          <div class="d-flex justify-center align-center">
            <vue-apex-charts
              width="600"
              height="200"
              type="bar"
              :options="chartOptions"
              :series="chartSeries"
            />
          </div>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue';
import VueApexCharts from 'vue3-apexcharts';
import { postcodeService } from '../services';
import type { TheftData } from '../services/postcodeService';

const props = defineProps<{
  postcode: string;
}>();

// State
const loading = ref(false);
const theftData = ref<TheftData[]>([]);

// Computed properties for chart data
const totalThefts = computed(() => theftData.value.reduce((sum, d) => sum + d.thefts, 0));
const firstYear = computed(() => theftData.value.length > 0 ? theftData.value[0].year : '');
const lastYear = computed(() => theftData.value.length > 0 ? theftData.value[theftData.value.length - 1].year : '');
const yearRange = computed(() => {
  if (theftData.value.length === 0) return '';
  if (theftData.value.length === 1) return theftData.value[0].year.toString();
  return `${firstYear.value}-${lastYear.value}`;
});

const chartSeries = computed(() => [{
  name: 'Thefts',
  data: theftData.value.map(d => d.thefts)
}]);

const chartOptions = computed(() => ({
  chart: {
    toolbar: {
      show: false
    },
    selection: {
      enabled: false
    }
  },
  colors: ['#07a377'],
  plotOptions: {
    bar: {
      borderRadius: 4,
      columnWidth: '60%'
    }
  },
  dataLabels: {
    enabled: false
  },
  xaxis: {
    categories: theftData.value.map(d => d.year.toString()),
    labels: {
      style: {
        fontSize: '12px',
        fontFamily: 'inherit'
      }
    }
  },
  yaxis: {
    forceNiceScale: false,
    labels: {
      formatter: (val: number) => Math.round(val).toString(),
      style: {
        fontSize: '12px',
        fontFamily: 'inherit'
      }
    }
  },
  grid: {
    show: true,
    borderColor: '#e0e0e0'
  },
  tooltip: {
    enabled: false
  },
}));

const fetchTheftData = async () => {
  if (!props.postcode) return;

  loading.value = true;
  try {
    theftData.value = await postcodeService.getTheftData(props.postcode);
  } catch (error) {
    console.warn(`Failed to fetch theft data for ${props.postcode}:`, error);
    theftData.value = [];
  } finally {
    loading.value = false;
  }
};

watch(() => props.postcode, fetchTheftData);
onMounted(fetchTheftData);

defineExpose({ fetchTheftData });
</script>

<style scoped>
.scroll-container {
  height: 500px;
  overflow-y: auto;
}
</style>
