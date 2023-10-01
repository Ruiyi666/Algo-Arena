<template>
  <div class="flex flex-col min-h-screen">
    <Header :host="host" :port="port" />
    <RouterView v-slot="{ Component }">
      <component :is="Component" :host="host" :port="port" />
    </RouterView>
    <Footer />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';

const host = import.meta.env.VITE_APP_BACKEND_HOST || '127.0.0.1'
const port = Number(import.meta.env.VITE_APP_BACKEND_PORT) || 8000

</script>

<style lang="scss" scoped></style>