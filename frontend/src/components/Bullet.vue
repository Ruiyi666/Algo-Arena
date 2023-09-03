<template>
  <div class="absolute grid" :class="colorList[props.color]" :style="{
    top: props.position.y * props.size + 'px',
    left: props.position.x * props.size + 'px',
    width: props.size + 'px',
    height: props.size + 'px',
    transform: 'rotate(' + rotate + 'deg)',
    transition: 'top ' + (1 / props.speed) + 's linear, left ' + (1 / props.speed) + 's linear, transform ' + (1 / props.speed) + 's linear',
  }">
    <i class="fas fa-circle place-self-center"></i>
  </div>
</template>

<script setup>
import { ref, computed, toRefs } from 'vue';

const props = defineProps({
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
    default: 1,
  },
})

const colorList = [
  'text-info-content',
  'text-warning-content',
  'text-success-content',
  'text-error-content',
];

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
  return angle;
});

</script>

<style scoped></style>