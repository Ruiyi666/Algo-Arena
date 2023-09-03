<template>
    <div class="flex flex-row justify-center w-3/4 p-4 my-8 space-x-4 shadow bg-base-100 card md:max-w-xl border-neutral" @click.self="focusEmpty()">
        <input v-for="(n, index) in props.length" pattern="\d+"  :key="index" :ref="el => (inputs[index] = el)"
            class="w-10 h-10 text-xl text-center rounded outline-none border-neutral focus:border-primary focus:border-2 bg-base-200"
            maxlength="1" v-model="codes[index]" 
            @input="handleInput(index)"
            @keyup="handleKeyUp(index, $event)"
            @keydown="handleKeyDown(index, $event)" />
        <button class="hidden h-10 grow btn btn-sm md:inline" @click="emits('generate', setCodes)">generate</button>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
    length: {
        type: Number,
        default: 6,
    }
});

const emits = defineEmits([
    'finish', 'generate',
]);

const codes = ref(Array(props.length).fill(''));
const inputs = ref([]);

const setCodes = (generated_codes) => {
    // codes : String
    for (let i = 0; i < props.length; i++) {
        if (i < generated_codes.length)
            codes.value[i] = generated_codes[i];
        else
            codes.value[i] = '';
    }
    focusEmpty();
};

const focusEmpty = () => {
    for (let i = 0; i < props.length; i++) {
        if (codes.value[i] === '') {
            inputs.value[i].focus();
            return
        }
    }
    inputs.value[props.length - 1].focus();
}

const handleInput = (index) => {
    codes.value[index] = codes.value[index].replace(/[^0-9]/g, '');
}

const handleKeyUp = (index, event) => {
    const value = event.target.value;

    if (value) {
        if (index < props.length - 1) {
            event.target.nextElementSibling.focus();
        }
        if (index === props.length - 1) {
            event.target.blur();
            emits('finish', codes.value.join(""));
        }
    }
};

const handleKeyDown = (index, event) => {
    if (!event.target.value && event.key === "Backspace" && index > 0) {
        event.target.previousElementSibling.focus();
    }
};

</script>
  