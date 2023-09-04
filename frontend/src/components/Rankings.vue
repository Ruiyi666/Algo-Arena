<template>
    <div class="container w-3/4 max-w-4xl px-4 py-16 mx-auto">
        <h1 class="mb-4 text-4xl font-bold">Rankings</h1>
        <div class="p-10 card bordered bg-base-100">

            <table class="table w-full card-body">
                <thead>
                    <tr>
                        <th class="text-center">Rank</th>
                        <th>Winner</th>
                        <th class="text-end">Rating</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- <tr v-for="rank in rankings" class="hover">
                            <td class="text-center">{{ rank.rank }}</td>
                            <td>{{ rank.username }}</td>
                            <td class="text-end">{{ rank.rating }}</td>
                        </tr> -->
                    <RankingItem v-for="rank in rankings" :rank="rank.rank" :username="rank.username"
                        :rating="rank.rating" :date="rank.date" />    
                </tbody>
            </table>

            <!-- <div class="sticky bottom-0 flex justify-center my-4">
                <div class="join">
                    <button class="join-item btn">«</button>
                    <button class="join-item btn">1</button>
                    <button class="join-item btn btn-active">2</button>
                    <button class="join-item btn">3</button>
                    <button class="join-item btn">4</button>
                    <button class="join-item btn">»</button>
                </div>
            </div> -->
            <Dialog ref="dialog" />
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useStore } from 'vuex'
import axios from 'axios';
import Dialog from './Dialog.vue';
import RankingItem from './RankingItem.vue';
const props = defineProps({
    host: { type: String, default: '127.0.0.1' },
    port: { type: Number, default: 8000 },
});

const dialog = ref(null);
const rankings = ref([]);

onMounted(async () => {
    try {
        const url = `http://${props.host}:${props.port}/api/games/`;
        const response = await axios.get(url);

        if (response.status === 200) {
            // rankings.value = response.data;
            for (let i = 0; i < response.data.length; i++) {
                const game_item = response.data[i];
                var username = null;
                var score = null;
                for (let j = 0; j < game_item.players.length; j++) {
                    if (score === null || game_item.players[j].score > score) {
                        score = game_item.players[j].score;
                        username = game_item.players[j].username;
                    }
                }
                rankings.value.push({
                    rank: i + 1,
                    username: username,
                    rating: score,
                    date: game_item.created_at,
                });
                rankings.value.sort((a, b) => b.rating - a.rating);
                for (let j = 0; j < rankings.value.length; j++) {
                    rankings.value[j].rank = j + 1
                }
            }
        } else {
            console.log('Failed to get rankings');
            dialog.value.showModal(
                'Error',
                'Failed to get rankings'
            )
        }
    } catch (error) {
        console.log(error);   
        dialog.value.showModal(
            'Error',
            'Failed to get rankings'
        )
    }
});

</script>

<style lang="scss" scoped></style>