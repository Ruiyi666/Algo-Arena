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

const props = defineProps({
    host: {
        type: String,
        default: '127.0.0.1',
        // default: '192.168.56.12',
    },
    port: {
        type: Number,
        default: 8000,
    },
})


</script>

<style lang="scss" scoped></style>