<template>
    <div class="m-8 p-4 border border-gray-300 rounded-md max-w-md">
        <div ref="map" :class="{
            'grid-cols-1': width === 1,
            'grid-cols-2': width === 2,
            'grid-cols-3': width === 3,
            'grid-cols-4': width === 4,
            'grid-cols-5': width === 5,
            'grid-cols-6': width === 6,
            'grid-cols-7': width === 7,
            'grid-cols-8': width === 8,
            'grid-cols-9': width === 9,
            'grid-cols-10': width === 10,
            'grid-cols-11': width === 11,
            'grid-cols-12': width === 12,
        }" class="relative grid">
            <Tile v-for="tile in props.tiles" :color="tile.color" />
            <slot></slot>
        </div>
    </div>
</template>

<script setup>
import { toRefs, ref, onMounted, watch, onBeforeUnmount } from 'vue';
import Tile from './Tile.vue';
const props = defineProps({
    width: {
        type: Number,
        default: 11
    },
    height: {
        type: Number,
        default: 11
    },
    tiles: {
        type: Array,
        default: () => []
    }
})

const { width, height } = toRefs(props);
const map = ref(null);
const cell_size = ref(0);

function getCellSize() {
    if (map.value) {
        cell_size.value = map.value.offsetWidth / width.value;
    }
}

onMounted(() => {
    getCellSize();
    addEventListener('resize', getCellSize);
})

onBeforeUnmount(() => {
    removeEventListener('resize', getCellSize);
})

defineExpose({
    cell_size,
})

</script>

<style lang="scss" scoped></style>