<template>
    <div class="flex flexrow max-w-md">
        <div class="flex bg-base-100 h-8 w-8 justify-center m-2">
            <span>{{ cur_operation.action }}</span>
        </div>
        <TransitionGroup name="list">
            <div class="flex h-8 w-8 justify-center m-2" v-for="op in operations" :key="op.id">
                <span>{{ op.action }}</span>
            </div>
        </TransitionGroup>

    </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, reactive, ref } from 'vue';

const props = defineProps({
    frequency: { type: Number, default: 1 }
});

const emits = defineEmits(['action']);

// operation queue
const operations = reactive([]);
const cur_operation = reactive({ id: 0, direction: 'L' });
const operation_count = ref(0);

const keys = {};

function pressedKeys() {
    if (keys['ArrowUp'] || keys['KeyW']) {
        operations.push({ id: operation_count.value++, action: 'up' });
    }
    if (keys['ArrowLeft'] || keys['KeyA']) {
        operations.push({ id: operation_count.value++, action: 'left' });
    }
    if (keys['ArrowDown'] || keys['KeyS']) {
        operations.push({ id: operation_count.value++, action: 'down' });
    }
    if (keys['ArrowRight'] || keys['KeyD']) {
        operations.push({ id: operation_count.value++, action: 'right' });
    }
    if (keys['Space'] || keys['KeyJ']) {
        operations.push({ id: operation_count.value++, action: 'shoot' });
    }
    while (operations.length > 2) {
        operations.shift();
    }

}

function handleOperation() {
    const op = operations.shift();
    if (!op) {
        // cur_operation.direction = ' ';
        emits('action', 'idle');
        return;
    }
    emits('action', op.action);
}

setInterval(handleOperation, 1000 / props.frequency);

onMounted(() => {
    // listen to key events
    document.addEventListener('keydown', (event) => {
        keys[event.code] = true;
        pressedKeys();
    });

    document.addEventListener('keyup', (event) => {
        delete keys[event.code];
    });

    // window.addEventListener('keydown', handleKeydown);
});

onBeforeUnmount(() => {
    // remove key event listener
    // window.removeEventListener('keydown', handleKeydown);
});

</script>

<style scoped>
.list-move,
.list-enter-active,
.list-leave-active {
    transition: all 0.5s;
}

.list-enter-from,
.list-leave-to {
    opacity: 0;
}

.list-leave-active {
    position: absolute;
}
</style>