<script setup>
import Rankings from '../components/Rankings.vue';
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
    <Rankings :host="props.host" :port="props.port" />
  </main>
</template>
