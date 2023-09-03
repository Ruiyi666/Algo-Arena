<script setup>
import { onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import PlayGame from '../components/PlayGame.vue';

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

const store = useStore();
const router = useRouter();

onMounted(() => {
  if (!store.state.isLoggedIn) {
    router.push({ name: 'home' });
  }
});

</script>

<template>
  <main class="bg-base-200">
    <PlayGame :host="host" :port="port"/>
  </main>
</template>
