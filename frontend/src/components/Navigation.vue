<template>
    <header class="sticky top-0 shadow-lg bg-gray-800">
        <nav class="flex flex-col sm:flex-row px-4 items-center gap-4 text-white py-6">
            <RouterLink :to="{ name: 'home' }">
                <div class="flex items-center gap-3 flex-1">
                    <i class="fa-solid fa-home"></i> Home
                </div>
            </RouterLink>

            <RouterLink :to="{ name: 'game' }" class="">
                <i class="fa-solid fa-gamepad"></i> Game
            </RouterLink>

            <RouterLink :to="{ name: 'about' }">
                <i class="fa-solid fa-info-circle"></i> About
            </RouterLink>
        </nav>
    </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>