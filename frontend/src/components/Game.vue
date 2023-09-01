<template>
    <div>
        <CodeInput />
        <Map ref="map" :width="map_size" :height="map_size" :tiles="state.map">
            <Player v-for="player in state.players" :position="player.position" :direction="player.direction"
                :color="player.color" :size="map?.cell_size" :key="player.key" />

            <Bullet v-for="bullet in state.bullets" :position="bullet.position" :direction="bullet.direction"
                :color="bullet.color" :size="map?.cell_size" :key="bullet.key" />
        </Map>
        <Controller @action="user_action($event)" :frequency="6" />
    </div>
</template>
  
<script setup>
import { ref, toRefs, onMounted, onBeforeUnmount, reactive, watch } from 'vue';
import Map from './Map.vue';
import Player from './Player.vue';
import Bullet from './Bullet.vue';
import Controller from './Controller.vue';
import CodeInput from './CodeInput.vue';

const props = defineProps({
    map_size: {
        type: Number,
        default: 9
    }
})

const map_size = ref(9);

const socket = new WebSocket('ws://127.0.0.1:8000/ws/123/');

const emits = defineEmits([

]);

const map = ref(null);
const self_action_map = {
    'up': { x: 0, y: -1 },
    'down': { x: 0, y: 1 },
    'left': { x: -1, y: 0 },
    'right': { x: 1, y: 0 },
    'shoot': { x: 0, y: 0 },
    'idle': { x: 0, y: 0 },
};

const opponent_action_map = {
    'up': { x: 0, y: 1 },
    'down': { x: 0, y: -1 },
    'left': { x: 1, y: 0 },
    'right': { x: -1, y: 0 },
    'shoot': { x: 0, y: 0 },
    'idle': { x: 0, y: 0 },
};

const state = reactive({
    players: [
        {
            position: {
                x: (props.map_size - 1) / 2,
                y: props.map_size - 1,
            },
            direction: {
                x: 0,
                y: -1,
            },
            key: Math.random(),
            color: 0,
            alive: true,
        },
        {
            position: {
                x: (props.map_size - 1) / 2,
                y: 0,
            },
            direction: {
                x: 0,
                y: 1,
            },
            key: Math.random(),
            color: 1,
            alive: true,
        }
    ],
    bullets: [],
    map: [],
});

const authority_state = JSON.parse(JSON.stringify(state));
const action_frame_queue = ref([]);

function init_map(state) {
    for (let i = 0; i < props.map_size; i++)
        for (let j = 0; j < props.map_size; j++) {
            state.map.push({
                color: Math.floor(Math.random() * 4),
            });
        }
}

onMounted(
    () => init_map(state)
)

function user_action(action) {
    var action_frame = [
        {
            player: 0,
            operation: action,
        }
    ];
    // actions_queue.value.push(action_frame);
    socket.send(JSON.stringify(action_frame));
}

socket.onmessage = function (event) {
    const action_frame = JSON.parse(event.data);
    // console.log(action_frame);
    apply_frame(state, action_frame);
    // action_frame_queue.value.push(action_frames);
}

function apply_frame(cur_state, action_frame) {
    // remove all the dead players
    cur_state.players = cur_state.players.filter(
        (player) => player.alive
    );

    // remove all the bullets that are out of the map
    cur_state.bullets = cur_state.bullets.filter(
        (bullet) => bullet.alive
    );

    // move all the bullets first
    for (var bullet of cur_state.bullets) {
        bullet.position.x += bullet.direction.x;
        bullet.position.y += bullet.direction.y;
        if (bullet.position.x < 0
            || bullet.position.x >= props.map_size
            || bullet.position.y < 0
            || bullet.position.y >= props.map_size) {
            bullet.alive = false;
        }
    }

    // check if any bullet hit the player
    for (var bullet of cur_state.bullets) {
        for (var player of cur_state.players) {
            if (bullet.color !== player.color
                && bullet.position.x === player.position.x
                && bullet.position.y === player.position.y) {
                player.alive = false;
            }
        }
    }

    // move all the players

    for (let action of action_frame) {
        const player = cur_state.players[action.player];
        if (!player) {
            console.log('player not found');
            continue;
        }
        var direction = { x: 0, y: 0 };
        const action_map = action.player === 0 ? self_action_map : opponent_action_map;
        direction.x = action_map[action.operation].x;
        direction.y = action_map[action.operation].y;
        if (direction.x === player.direction.x
            && direction.y === player.direction.y) {
            if (direction.x + player.position.x < 0)
                direction.x = 0;
            if (direction.x + player.position.x >= props.map_size)
                direction.x = 0;
            if (direction.y + player.position.y < 0)
                direction.y = 0;
            if (direction.y + player.position.y >= props.map_size)
                direction.y = 0;
            player.position.x += direction.x;
            player.position.y += direction.y;
        } else if (direction.x !== 0 || direction.y !== 0) {
            player.direction.x = direction.x;
            player.direction.y = direction.y;
        }
        if (action.operation === 'shoot') {
            cur_state.bullets.push({
                position: {
                    x: player.position.x,
                    y: player.position.y,
                },
                direction: {
                    x: player.direction.x,
                    y: player.direction.y,
                },
                color: player.color,
                alive: true,
                key: Math.random(),
            });
        }
    }
}

function apply(cur_state, action_frames) {
    for (let action_frame of action_frames) {
        apply_frame(cur_state, action_frame);
    }
}

</script>
  
<style scoped></style>
  