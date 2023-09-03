<template>
    
</template>
  
<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from 'axios'

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
const dialog = ref(null)
const dialog_title = ref(null)
const dialog_content = ref(null)




</script>
  
<style scoped>
/* Additional styles if needed */
</style>
  