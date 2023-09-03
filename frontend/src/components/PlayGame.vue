<template>
    <div class="flex flex-col items-center justify-start w-full max-w-4xl min-h-screen mx-auto">
        <CodeInput @finish="connect_websocket($event)" @generate="generate_codes($event)" />
        <progress class="w-3/4 progress md:max-w-lg" :value="predict_state.settings.cur_frames" :max="predict_state.settings.max_frames"></progress>
        <Map ref="map" :width="predict_state.settings.n_cols" :height="predict_state.settings.n_rows" :tiles="predict_state.map" :speed="frequency">
            <Player v-for="player, id in predict_state.players" :position="player.position" :direction="player.direction"
                :color="player.color" :size="map?.cell_size" :key="id" />

            <Bullet v-for="bullet, id in predict_state.bullets" :position="bullet.position" :direction="bullet.direction"
                :color="bullet.color" :size="map?.cell_size" :key="id" :speed="frequency" />
        </Map>
        
        <Controller @action="player_action($event)" :frequency="frequency" ref="controller" />
    </div>
</template>

<script setup>
import { ref, onMounted, reactive, watch } from 'vue';
import Map from './Map.vue';
import Player from './Player.vue';
import Bullet from './Bullet.vue';
import Controller from './Controller.vue';
import CodeInput from './CodeInput.vue';

const props = defineProps({
    host: {
        type: String,
        default: '127.0.0.1',
    },
    port: {
        type: Number,
        default: 8000,
    },
    route: {
        type: String,
        default: 'ws/play',
    },
    room: {
        type: String,
        default: '',
    },
    map_size: {
        type: Number,
        default: 9
    }
})

const private_data = ref({})
const socket = ref(null);
const map = ref(null);
const controller = ref(null);
const frequency = ref(1)

const predict_state = reactive({
    settings: {
        n_cols: props.map_size,
        n_rows: props.map_size,
        cur_frames: null,
        max_frames: 1 * 60 * 6,
    },
    players: {},
    bullets: {},
    map: [],
});

watch(predict_state.settings, () => {
    if ("frequency" in predict_state.settings) {
        frequency.value = predict_state.settings.frequency
    }
})

const emits = defineEmits([

]);



onMounted(() => {
    if (props.room)
        connect_websocket(props.room);
})

const generate_codes = (callback) => {
    // random 6 code
    const codes = [];
    for (let i = 0; i < 6; i++) {
        codes.push(Math.floor(Math.random() * 10));
    }
    callback(codes.join(""));
}

const self_action_map = {
    'up': { x: 0, y: -1 },
    'down': { x: 0, y: 1 },
    'left': { x: -1, y: 0 },
    'right': { x: 1, y: 0 },
    'shoot': { x: 0, y: 0 },
    'idle': { x: 0, y: 0 },
};


const authority_state = JSON.parse(JSON.stringify(predict_state));
const action_frame_queue = [];

function init_map(state) {
    for (let i = 0; i < props.map_size; i++)
        for (let j = 0; j < props.map_size; j++) 
            state.map.push({ color: Math.floor(Math.random() * 4) });
}

onMounted(
    () => init_map(predict_state)
)

function player_action(action) {
    // actions_queue.value.push(frame_action);
    if (socket.value != null && socket.value.readyState === WebSocket.OPEN) {
        socket.value.send(JSON.stringify({
            type: "update.game.action",
            content: action,
        }));
    }
}

function apply_state(cur_state, frame_state) {
    if (frame_state.settings) {
        for (const key in frame_state.settings)
            cur_state.settings[key] = frame_state.settings[key]
    }

    if (frame_state.players) {
        for (const id in frame_state.players) {
            const player = frame_state.players[id];
            cur_state.players[id] = {
                position: { x: player.position.x, y: player.position.y },
                direction: { x: player.direction.x, y: player.direction.y },
                color: player.color,
                alive: player.alive
            };
        }
        for (const id in cur_state.players) {
            if (!(id in frame_state.players)) {
                delete cur_state.players[id];
            }
        }
    }

    if (frame_state.bullets) {
        for (const id in frame_state.bullets) {
            const bullet = frame_state.bullets[id];
            cur_state.bullets[id] = {
                position: { x: bullet.position.x, y: bullet.position.y },
                direction: { x: bullet.direction.x, y: bullet.direction.y },
                color: bullet.color,
                alive: bullet.alive
            };
        }
        for (const id in cur_state.bullets) {
            if (!(id in frame_state.bullets)) {
                delete cur_state.bullets[id];
            }
        }
    }

    if (frame_state.map) {
        cur_state.map = [...frame_state.map];
    }
}

function apply_action(cur_state, frame_action) {
    // console.log(frame_action)
    // console.log(cur_state)

    if (!cur_state.settings.cur_frames) {
        // console.log(cur_state.settings.cur_frames)
        cur_state.settings.cur_frames = 1;
    } else {
        cur_state.settings.cur_frames += 1;
    }

    // remove all the dead players
    for (const id in cur_state.players) {
        if (!cur_state.players[id].alive) {
            delete cur_state.players[id];
        }
    }

    // remove all the bullets that are out of the map
    for (const id in cur_state.bullets) {
        if (!cur_state.bullets[id].alive) {
            delete cur_state.bullets[id];
        }
    }

    // 0. Move bullets
    for (const bulletId in cur_state.bullets) {
        const bullet = cur_state.bullets[bulletId];
        bullet.nextPosition = {
            x: bullet.position.x + bullet.direction.x,
            y: bullet.position.y + bullet.direction.y
        };
    }

    // 1. Move Players
    for (const playerId in cur_state.players) {
        
        const player = cur_state.players[playerId];
        var action = frame_action.action[playerId];
        if (!action) action = 'idle';
        // up, down, left, right, idle, shoot
        
        let direction = {
            x: self_action_map[action].x,
            y: self_action_map[action].y
        };

        if (direction.x === player.direction.x && direction.y === player.direction.y) {
            let nextX = direction.x + player.position.x;
            let nextY = direction.y + player.position.y;

            // Boundary checks
            if (nextX < 0 || nextX >= cur_state.settings.n_cols) direction.x = 0
            else if (nextY < 0 || nextY >= cur_state.settings.n_rows) direction.y = 0
            else if (cur_state.map[nextY * cur_state.settings.n_cols + nextX].color !== player.color) {
                direction.x = 0; direction.y = 0;
            }
        } else if (direction.x !== 0 || direction.y !== 0) {
            player.direction = direction;
            direction = { x: 0, y: 0 }; // Don't move, just change direction
        }

        player.nextPosition = {
            x: player.position.x + direction.x,
            y: player.position.y + direction.y
        };

        if (action === 'shoot') {
            const bulletId = `${cur_state.settings.cur_frames}_${playerId}`;

            cur_state.bullets[bulletId] = {
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
                nextPosition: {
                    x: player.position.x,
                    y: player.position.y,
                }
            };
        }
    }

    // 2. Check for bullet-player collisions
    for (const playerId in cur_state.players) {
        const player = cur_state.players[playerId];
        for (const bulletId in cur_state.bullets) {
            const bullet = cur_state.bullets[bulletId];

            if (bullet.color !== player.color &&
                bullet.nextPosition.x === player.nextPosition.x &&
                bullet.nextPosition.y === player.nextPosition.y) {
                player.alive = false;
                bullet.alive = false;
                break;  // Exit bullet loop if collision detected
            }
            if (bullet.color !== player.color &&
                bullet.position.x === player.nextPosition.x &&
                bullet.position.y === player.nextPosition.y &&
                bullet.nextPosition.x === player.position.x &&
                bullet.nextPosition.y === player.position.y
            ) {
                player.alive = false;
                bullet.alive = false;
                break;
            }
        }
    }

    // 3. Check for bullet-bullet collisions
    for (const bulletIdA in cur_state.bullets) {
        const bulletA = cur_state.bullets[bulletIdA];

        for (const bulletIdB in cur_state.bullets) {
            if (bulletIdA === bulletIdB) continue;  // Skip same bullet comparison

            const bulletB = cur_state.bullets[bulletIdB];
            if (!bulletB.alive) continue;

            if (bulletA.color !== bulletB.color &&
                bulletA.nextPosition.x === bulletB.nextPosition.x &&
                bulletA.nextPosition.y === bulletB.nextPosition.y
            ) {
                // Bullet A and Bullet B have collided
                bulletA.alive = false;
                bulletB.alive = false;
                break;  // Exit inner bullet loop if collision detected
            }

            if (bulletA.color !== bulletB.color &&
                bulletA.position.x === bulletB.nextPosition.x &&
                bulletA.position.y === bulletB.nextPosition.y &&
                bulletA.nextPosition.x === bulletB.position.x &&
                bulletA.nextPosition.y === bulletB.position.y
            ) {
                bulletA.alive = false;
                bulletB.alive = false;
                break;
            }
        }
    }

    for (const bulletId in cur_state.bullets) {
        const bullet = cur_state.bullets[bulletId];
        const x = bullet.position.x;
        const y = bullet.position.y;
        
        if (bullet.alive) 
            cur_state.map[y * cur_state.settings.n_cols + x].color = bullet.color;
        
        // Check if bullets are out of the map
        if (bullet.nextPosition.x < 0 || bullet.nextPosition.x >= cur_state.settings.n_cols
            || bullet.nextPosition.y < 0 || bullet.nextPosition.y >= cur_state.settings.n_rows) {
            bullet.alive = false;
        }
        
    }

    // 4. Update player and bullet positions
    for (const playerId in cur_state.players) {
        const player = cur_state.players[playerId];
        player.position = {
            x: player.nextPosition.x,
            y: player.nextPosition.y
        }
        delete player.nextPosition;
    }

    for (const bulletId in cur_state.bullets) {
        const bullet = cur_state.bullets[bulletId];
        bullet.position = {
            x: bullet.nextPosition.x,
            y: bullet.nextPosition.y
        }
        delete bullet.nextPosition;
    }
}

function apply(cur_state, action_frames) {
    for (let frame_action of action_frames) {
        apply_action(cur_state, frame_action);
    }
}

function connect_websocket(room) {

    if (socket.value)
        socket.value.close();

    const token = localStorage.getItem('token') || "c0adc8958890aac984b0138ef74f49f20527e836";
    const url = `ws://${props.host}:${props.port}/${props.route}/${room}/?token=${token}`;

    socket.value = new WebSocket(url);

    socket.value.onopen = () => {
        // 
        socket.value.send(JSON.stringify({
            "type": "signal",
            "content": "join",
        }))
    }

    socket.value.onclose = () => {
        controller.value.stop()
    }

    socket.value.onmessage = (event) => {
        console.log(event.data);
        const data = JSON.parse(event.data)
        const type = data.type;
        const content = data.content;
        if (type === "connect") {
            private_data.value = content;
        } else if (type === "signal") {
            if (content === "start") 
                controller.value.start()
        } else if (type === "sync.game") {
            // state = content.latest_framestate.state
            apply_state(predict_state, content.latest_framestate.state)
        } else if (type === "sync.game.action") {
            apply_action(predict_state, content);
        } else if (type === "sync.game.state") {
            apply_state(predict_state, content.state);
        } else if (type === "sync.game.player") {

        }
    }

    socket.value.onerror = () => {
        console.log("Socket error");
    }
}


</script>
  
<style scoped></style>
  