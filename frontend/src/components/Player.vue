<template>
  <div class="absolute grid rounded-full" :class="colorList[props.color]" :style="{
    top: props.position.y * props.size + 'px',
    left: props.position.x * props.size + 'px',
    width: props.size + 'px',
    height: props.size + 'px',
    transform: 'rotate(' + rotate + 'deg)',
    transition: 'top ' + (1 / props.speed) + 's , left ' + (1 / props.speed) + 's , transform ' + (1 / props.speed) + 's ',
  }">
    <i class="fas fa-arrow-up place-self-center text-secondary dark:text-secondary-dark"></i>
  </div>
</template>

<script setup>
import { ref, computed, toRefs } from 'vue';

const props = defineProps({
  position: {
    x: {
      type: Number,
      default: 0,
    },
    y: {
      type: Number,
      default: 0,
    },
  },
  direction: {
    x: {
      type: Number,
      default: 0,
    },
    y: {
      type: Number,
      default: 0,
    },
  },
  color: {
    type: Number,
    default: 0,
  },
  size: {
    type: Number,
    default: 0,
  },
  speed: {
    type: Number,
    default: 2,
  },
});

const colorList = [
  'bg-red-500 dark:bg-red-700',
  'bg-blue-500 dark:bg-blue-700',
  'bg-green-500 dark:bg-green-700',
  'bg-yellow-500 dark:bg-yellow-700',
];

const last_direction = ref(0);

const rotate = computed(() => {
  var angle = 0;
  if (props.direction.x === 0 && props.direction.y === -1) {
    angle = 0;
  } else if (props.direction.x === 1 && props.direction.y === 0) {
    angle = 90;
  } else if (props.direction.x === 0 && props.direction.y === 1) {
    angle = 180;
  } else if (props.direction.x === -1 && props.direction.y === 0) {
    angle = 270;
  }

  var delta = (angle - last_direction.value) % 360;
  if (delta > 180) {
    delta -= 360;
  } else if (delta < -180) {
    delta += 360;
  }
  angle = last_direction.value + delta;
  last_direction.value = angle;
  return angle;
});

</script>

<style scoped></style>
