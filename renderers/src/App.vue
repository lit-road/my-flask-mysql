<script setup lang="ts">
// See vite.config.ts for details about automatic imports
const route = useRoute()

useHead({
  title: () => route.meta.title || 'Vite + Vue Template',
  meta: [
    {
      property: 'og:title',
      content: () => route.meta.title,
    },
    {
      name: 'twitter:title',
      content: () => route.meta.title,
    },
  ],
})

const VERSION = import.meta.env.VITE_APP_VERSION
const BUILD_DATE = import.meta.env.VITE_APP_BUILD_EPOCH
  ? new Date(Number(import.meta.env.VITE_APP_BUILD_EPOCH))
  : undefined
const thisYear = new Date().getFullYear()
</script>
<template>
  <div class="relative py-8">
    <div
      class="absolute inset-0 bg-[url(/img/grid.svg)] bg-top [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]" />
    <div class="container relative max-w-2xl mx-auto bg-white shadow-xl shadow-slate-700/10 ring-1 ring-gray-900/5">
      <header class="px-4 pt-6 text-center prose-sm md:px-6 md:prose">
        <h3>Vite + Vue 3 + TS + Tailwind + Flask + mysql</h3>
      </header>
      <main>
        <router-view />
      </main>
      <footer class="py-6 text-sm text-center text-gray-700">
        <p>
          &copy; 2021{{ thisYear > 2021 ? `–${thisYear}` : '' }} ez
          <span v-if="BUILD_DATE">, built on {{ BUILD_DATE.toISOString() }}</span>
        </p>
      </footer>
    </div>
  </div>
</template>
