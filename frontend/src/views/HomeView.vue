<script setup>
import Login from '../components/Login.vue';
import Home from '../components/Home.vue';
const props = defineProps({
    host: {
        type: String,
        default: '127.0.0.1'
    },
    port: {
        type: Number,
        default: 8000
    },
})
</script>

<template>
  <main class="bg-base-200">
    <Login :host="props.host" :port="props.port" />
  </main>
</template>
