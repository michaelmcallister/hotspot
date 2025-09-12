# Hotspot Web Frontend

## Developer Documentation

### Install Dependencies

You'll need Node.js (LTS version recommended) and npm (or pnpm/yarn).  

From the `web/` directory, install packages with:
```
npm install
```

### Running the development server

```
npm run dev
```

This will start the Vite dev server at http://127.0.0.1:5173/  

The frontend is configured to proxy API requests under `/api` to the backend at http://127.0.0.1:8000  (if you've started the API)

### Adding new components

Please place Vue components under the `src/components/` directory.  
Use `<script setup lang="ts">` with TypeScript enabled.  

For example:

```vue
<template>
  <p>{{ msg }}</p>
</template>

<script setup lang="ts">
defineProps<{ msg: string }>()
</script>

