<template>
  <div class="absolute grid border rounded-full alert-error" :class="bg_colors[props.color]" :style="{
    top: (props.position.y * props.size + props.padding) + 'px',
    left: (props.position.x * props.size + props.padding) + 'px',
    width: (props.size - 2 * props.padding) + 'px',
    height: (props.size - 2 * props.padding) + 'px',
    transform: 'rotate(' + rotate + 'deg)',
    transition: 'top ' + (1 / props.speed) + 's , left ' + (1 / props.speed) + 's , transform ' + (1 / props.speed) + 's ',
  }">
    <i class="fa-solid fa-arrow-up place-self-center" :class="text_colors[props.color]"></i>
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
  padding: {
    type: Number,
    default: 2,
  }
});

const bg_colors = [
  'bg-info',
  'bg-warning',
  'bg-success',
  'bg-error',
];

const text_colors = [
  'text-info-content',
  'text-warning-content',
  'text-success-content',
  'text-error-content',
]

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
