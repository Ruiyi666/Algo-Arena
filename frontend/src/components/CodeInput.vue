<template>
    <div class="game-room-code-wrapper flex justify-center space-x-4">
        <input v-for="(n, index) in 6" :key="index"
            class="room-code-input w-10 h-10 text-center text-xl border-2 border-neutral rounded outline-none focus:border-primary"
            maxlength="1" v-model="codes[index]" @keyup="handleKeyUp(index, $event)"
            @keydown="handleKeyDown(index, $event)" />
    </div>
</template>
  
<script setup>
import { ref } from 'vue';

const codes = ref(Array(6).fill(''));

const handleKeyUp = (index, event) => {
    const value = event.target.value;
    if (value && index < 5) {
        event.target.nextElementSibling.focus();
    }
};

const handleKeyDown = (index, event) => {
    if (!event.target.value && event.key === "Backspace" && index > 0) {
        event.target.previousElementSibling.focus();
    }
};

</script>
  