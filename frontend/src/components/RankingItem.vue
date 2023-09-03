<template>
    <tr class="hover">
        <td class="text-center">{{ rank }}</td>
        <td>{{ username }}</td>
        <td class="text-end">{{ rating }}</td>
    </tr>
</template>

<script setup>
import { toRefs } from 'vue';
const props = defineProps({
    rank: Number,
    username: String,
    rating: Number
});
const { rank, username, rating } = toRefs(props);

</script>

<style lang="scss" scoped></style>