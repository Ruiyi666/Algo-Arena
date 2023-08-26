<template>
    <div class="border border-gray-300 aspect-square text-center">
        <slot></slot>
    </div>
</template>

<script setup>
const props = defineProps({
    color: {
        type: Number,
        default: 0,
    }
})

</script>

<style lang="scss" scoped>

</style>