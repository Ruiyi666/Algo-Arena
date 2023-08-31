<template>
  <div class="flex flex-col min-h-screen bg-slate-50">
    <Header />
    <RouterView />
    <Footer />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
</script>

<style lang="scss" scoped></style>