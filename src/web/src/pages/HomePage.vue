<template>
  <v-container class="py-10">
    <v-row class="align-center">
      <v-col cols="12" md="7">
        <div class="mb-6">
          <h1 class="text-h4 font-weight-medium mb-2">Find safer places to park</h1>
          <p class="text-body-1 text-medium-emphasis">
            Search by suburb or postcode to see risk and nearby secure parking.
          </p>
        </div>

        <v-form @submit.prevent="onGo">
          <v-autocomplete
            v-model="model"
            :items="items"
            :loading="loading"
            :hide-no-data="!query"
            item-title="label"
            return-object
            label="Search suburb or postcode"
            prepend-inner-icon="mdi-magnify"
            variant="outlined"
            density="comfortable"
            @update:search="onSearch"
            @keyup.enter="onGo"
          />
          <div class="d-flex ga-2 mt-3">
            <v-btn color="primary" @click="goReport" prepend-icon="mdi-file-document">View Report</v-btn>
            <v-btn color="tertiary" variant="tonal" @click="goParking" prepend-icon="mdi-parking">Find Safe Parking</v-btn>
          </div>
          <v-alert
            v-if="error"
            type="error"
            class="mt-4"
            density="comfortable"
            :text="error"
            variant="tonal"
          />
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import { isPostcode, toSlug } from "@/utils/geo";
import { fetchSearchResults, type SearchResult } from "@/services/search";

const router = useRouter();

const query = ref("");
const items = ref<SearchResult[]>([]);
const model = ref<SearchResult | null>(null);
const loading = ref(false);
const error = ref("");

async function onSearch(val: string) {
  query.value = val;
  error.value = "";
  if (!val) {
    items.value = [];
    return;
  }
  loading.value = true;
  try {
    items.value = await fetchSearchResults(val);
  } finally {
    loading.value = false;
  }
}

function resolveTarget() {
  const raw = (model.value?.label || query.value || "").trim();
  if (!raw) {
    error.value = "Enter a suburb or postcode.";
    return null;
  }
  saveRecent(raw);

  if (isPostcode(raw)) {
    return { kind: "postcode", value: raw };
  }
  // crude: treat last 4 digits as postcode if present; otherwise slug the suburb
  const m = raw.match(/(\d{4})\b/);
  if (m) return { kind: "postcode", value: m[1] };
  return { kind: "suburb", value: toSlug(raw.replace(/,.*$/, "")) };
}

function goReport() {
  const t = resolveTarget();
  if (!t) return;
  error.value = "";
  if (t.kind === "suburb") router.push({ path: `/suburb/${t.value}` });
  else router.push({ path: "/hotspots", query: { postcode: t.value } });
}
function goParking() {
  const t = resolveTarget();
  if (!t) return;
  error.value = "";
  const q: Record<string, string> = t.kind === "suburb" ? { suburb: t.value } : { postcode: t.value };
  router.push({ path: "/parking", query: q });
}
function onGo() {
  // default action when pressing Enter: go to Report
  goReport();
}

// Keep model and query loosely in sync for better UX
watch(model, (m) => { if (m?.label) query.value = m.label; });
</script>
