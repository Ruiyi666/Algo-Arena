<template>
    <div class="text-center border rounded-md border-base-100 aspect-square" :class="bg_colors[props.color + 1]" :style="{
        transition: 'background-color ' + (1 / props.speed) + 's linear, color ' + (1 / props.speed) + 's linear'
    }">
        <slot></slot>
    </div>
</template>

<script setup>
const props = defineProps({
    color: {
        type: Number,
        default: 0,
    },
    speed: {
        type: Number,
        default: 4,
    }
})

const bg_colors = [
    'bg-base-100',  
    'bg-info',  
    'bg-warning',
    'bg-success',
    'bg-error',
];

</script>

<style scoped>
</style>