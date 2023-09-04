<template>
    <div class="min-h-screen -mt-16 hero bg-base-200">
        <div class="flex-col w-3/4 hero-content md:flex-row-reverse md:max-w-4xl">
            <div class="p-8 text-center md:text-left">
                <h1 class="text-4xl font-bold">Get Started</h1>
                <p class="py-6">
                    AlgoArena is an online multiplayer game, where you can battle against other players with your mannual
                    strategy.
                    <br>
                    <br>
                    In the future, you will be able to control the game programmatically.
                </p>
            </div>
            <div v-if="showLogin" class="flex-shrink-0 w-full max-w-sm shadow-2xl card bg-base-100">
                <!-- Login Form -->
                <div class="card-body">
                    <div class="form-control">
                        <label class="label">
                            <span class="label-text">Username</span>
                        </label>
                        <input v-model="login.username" type="text" placeholder="username" class="input input-bordered" />
                    </div>
                    <div class="form-control">
                        <label class="label">
                            <span class="label-text">Password</span>
                        </label>
                        <input v-model="login.password" type="password" placeholder="password"
                            class="input input-bordered" />
                    </div>
                    <div class="mt-6 form-control">
                        <button @click="handleLogin" class="btn btn-primary">Login</button>
                    </div>
                    <div class="mt-6">
                        No account yet? <a @click="showLogin = false" href="#"
                            class="link link-hover link-secondary">Register</a>
                    </div>
                </div>
            </div>
            <div v-else class="flex-shrink-0 w-full max-w-sm shadow-2xl card bg-base-100">
                <!-- Register Form -->
                <div class="card-body">
                    <div class="form-control">
                        <label class="label">
                            <span class="label-text">Username</span>
                        </label>
                        <input v-model="register.username" type="text" placeholder="username"
                            class="input input-bordered" />
                    </div>
                    <div class="form-control">
                        <label class="label">
                            <span class="label-text">Password</span>
                        </label>
                        <input v-model="register.password" type="password" placeholder="password"
                            class="input input-bordered" />
                    </div>
                    <div class="mt-6 form-control">
                        <button @click="handleRegister" class="btn btn-secondary">Register</button>
                    </div>
                    <div class="mt-6">
                        Already have an account? <a @click="showLogin = true" href="#"
                            class="link link-hover link-primary">Login</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <Dialog ref="dialog" />
</template>


  
<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

import axios from 'axios'

import Dialog from './Dialog.vue'

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
const store = useStore();
const router = useRouter();
const dialog = ref(null)

const login = ref({
    username: '',
    password: ''
})

const register = ref({
    username: '',
    password: ''
})

const showLogin = ref(true)  // By default, show the login form

const clearForm = () => {
    login.value.username = ''
    login.value.password = ''
    register.value.username = ''
    register.value.password = ''
}

const handleLogin = async (event) => {
    event.preventDefault();
    try {
        const url = `http://${props.host}:${props.port}/api-token-auth/`
        const response = await axios.post(url, {
            username: login.value.username,
            password: login.value.password
        })

        if (response.data && response.data.token) {
            dialog.value.showModal(
                'Success',
                'Logged in successfully',
            )
            store.commit('login', response.data.token)
            router.push({ name: 'game' })
        } else {
            localStorage.removeItem('token')
            console.error('Failed to retrieve token')
            dialog.value.showModal('Failed', 'Failed to retrieve token')
        }
    } catch (error) {
        console.error('Login error:', error)
        dialog.value.showModal('Failed', error)
    }
}

const handleRegister = async (event) => {
    event.preventDefault();
    try {
        const url = `http://${props.host}:${props.port}/api/users/`
        const response = await axios.post(url, {
            username: register.value.username,
            password: register.value.password
        })
        
        if (response.status === 201) {
            console.log('User registered successfully')
            login.value.username = register.value.username
            login.value.password = register.value.password
            dialog.value.showModal('Success', 'Registered successfully')
            showLogin.value = true
        } else {
            console.error('Failed to register')
            dialog.value.showModal('Failed', response.data)
        }
    } catch (error) {
        console.error('Registration error:', error)
        dialog.value.showModal('Failed', error)
    }
}


</script>
  
<style scoped>
/* Additional styles if needed */
</style>
  