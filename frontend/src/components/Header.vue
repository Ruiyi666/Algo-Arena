<template>
    <div class="sticky top-0 z-10 shadow navbar bg-base-100">
        <div class="navbar-start">
            <div class="dropdown">
                <label tabindex="0" class="btn btn-ghost sm:hidden">
                    <i class="fa-solid fa-bars"></i>
                </label>
                <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
                    <li>
                        <RouterLink :to="{ name: 'home' }">
                            <i class="fa-solid fa-home"></i> Home
                        </RouterLink>
                    </li>
                    <li>
                        <RouterLink :to="{ name: 'rankings' }">
                            <i class="fa-solid fa-trophy"></i> Rankings
                        </RouterLink>
                    </li>
                    <li v-if="isLogin">
                        <RouterLink :to="{ name: 'game' }">
                            <i class="fa-solid fa-gamepad"></i> Game
                        </RouterLink>
                    </li>
                    <li>
                        <RouterLink :to="{ name: 'about' }">
                            <i class="fa-solid fa-question"></i> About
                        </RouterLink>
                    </li>
                </ul>
            </div>
            <button class="text-xl normal-case btn btn-ghost">AlgoArena</button>
        </div>
        <div class="hidden navbar-center sm:flex">
            <ul class="gap-1 px-1 menu menu-horizontal">
                <li>
                    <RouterLink :to="{ name: 'home' }" :class="{ 'active': $route.name === 'home' }">
                        <i class="fa-solid fa-home"></i>
                        <span class="hidden md:inline">Home</span>
                    </RouterLink>
                </li>
                <li>
                    <RouterLink :to="{ name: 'rankings' }" :class="{ 'active': $route.name === 'rankings' }">
                        <i class="fa-solid fa-trophy"></i>
                        <span class="hidden md:inline">Rankings</span>
                    </RouterLink>
                </li>
                <li v-if="isLogin">
                    <RouterLink :to="{ name: 'game' }" class="" :class="{ 'active': $route.name === 'game' }">
                        <i class="fa-solid fa-gamepad"></i>
                        <span class="hidden md:inline">Game</span>
                    </RouterLink>
                </li>
                <li>
                    <RouterLink :to="{ name: 'about' }" :class="{ 'active': $route.name === 'about' }">
                        <i class="fa-solid fa-question"></i>
                        <span class="hidden md:inline">About</span>
                    </RouterLink>
                </li>
            </ul>
        </div>
        <div class="navbar-end">
            <label class="btn btn-ghost btn-circle swap swap-rotate">
                <input type="checkbox" v-model="isDark" @change="setTheme(isDark ? 'dark' : 'light')">
                <i class="fill-current swap-off fa-solid fa-sun"></i>
                <i class="fill-current swap-on fa-solid fa-moon"></i>
            </label>

            <div v-if="isLogin" class="dropdown dropdown-end">
                <label tabindex="0" class="btn btn-ghost btn-circle avatar">
                    <i class="fa-solid fa-user"></i>
                </label>
                <ul tabindex="0" class="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52">
                    <li>
                        <a class="justify-between">
                            Profile
                            <span class="badge">New</span>
                        </a>
                    </li>
                    <li><a>Settings</a></li>
                    <li><a @click="handleLogout">Logout</a></li>
                </ul>
            </div>

            <button v-else class="btn btn-ghost btn-circle">
                <RouterLink :to="{ name: 'home' }">
                    <div class="indicator">
                        <i class="fa-solid fa-user"></i>
                        <span class="badge badge-xs badge-primary indicator-item"></span>
                    </div>
                </RouterLink>
            </button>
        </div>
    </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, computed } from 'vue';
import { useStore } from 'vuex';
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'

const props = defineProps({
    host: {
        type: String,
        default: '127.0.0.1'
    },
    port: {
        type: Number,
        default: 8000
    },
})

const isDark = ref(false);
const router = useRouter();
const store = useStore();
const isLogin = computed(() => store.state.isLoggedIn);

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}

onMounted(() => {
    const theme = localStorage.getItem('theme');
    if (theme) {
        isDark.value = theme === 'dark';
        setTheme(theme);
    } else {
        isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(isDark.value ? 'dark' : 'light');
    }
});

onBeforeUnmount(() => {
    // localStorage.removeItem('theme');
});

const handleLogout = async () => {
    try {
        const url = `http://${props.host}:${props.port}/api-token-auth/`
        const response = await axios.delete(url, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`
            }
        })   
        if (response.status === 200) {
            console.log('User registered successfully')
        } else {
            console.error('Failed to register')
        }
    } catch (error) {
        console.error('Registration error:', error)
    }
    store.commit('logout')
    router.push({ name: 'home' });
}
</script>