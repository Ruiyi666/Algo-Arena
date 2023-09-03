<template>
    <!--
      This example requires updating your template:
  
      ```
      <html class="h-full">
      <body class="h-full">
      ```
    -->
    <main class="grid min-h-screen px-6 py-24 -mt-16 bg-base-200 place-items-center sm:py-32 lg:px-8">
        <div class="text-center">
            <p class="text-base font-semibold text-primary">404</p>
            <h1 class="mt-4 text-3xl font-bold tracking-tight text-base-content sm:text-5xl">Page not found</h1>
            <p class="mt-6 text-base leading-7 text-base-content">Sorry, we couldn't find the page you're looking for.</p>
            <div class="flex items-center justify-center mt-10 gap-x-6">
                <button class="btn btn-primary" @click="$router.go(-1)">
                    Go back home
                </button>
                <a href="#" class="text-sm font-semibold text-base-content">Contact support <span aria-hidden="true">&rarr;</span></a>
            </div>
        </div>
    </main>
</template>
  
<script setup>
import { RouterLink } from 'vue-router';
</script>