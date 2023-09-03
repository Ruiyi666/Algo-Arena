<template>
    <div class="flex flex-col items-center justify-center w-full max-w-4xl">
        <div class="flex flex-col justify-center min-w-full">
            <h1 class="text-4xl font-bold">Rankings</h1>
            <p class="my-2 text-xl">This is the rankings page.</p>

            <table class="table w-full border-collapse">
                <thead>
                    <tr>
                        <th class="text-center">Rank</th>
                        <th>Username</th>
                        <th class="text-end">Rating</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- <tr v-for="rank in rankings" class="hover">
                            <td class="text-center">{{ rank.rank }}</td>
                            <td>{{ rank.username }}</td>
                            <td class="text-end">{{ rank.rating }}</td>
                        </tr> -->
                    <RankingItem v-for="rank in rankings" :rank="rank.rank" :username="rank.username"
                        :rating="rank.rating" />
                </tbody>
            </table>

            <div class="sticky bottom-0 flex justify-center my-4">
                <div class="join">
                    <button class="join-item btn">«</button>
                    <button class="join-item btn">1</button>
                    <button class="join-item btn btn-active">2</button>
                    <button class="join-item btn">3</button>
                    <button class="join-item btn">4</button>
                    <button class="join-item btn">»</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import RankingItem from './RankingItem.vue';
const rankings = ref([]);

onMounted(() => {
    for (let i = 0; i < 100; i++) {
        rankings.value.push({
            rank: i + 1,
            username: 'user' + i,
            rating: 1000 - i
        });
    }
});

</script>

<style lang="scss" scoped></style>