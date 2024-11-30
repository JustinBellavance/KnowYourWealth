<template>
  <div id="app">
    <header class="text-white p-4" style="background-color: #2c3e50;">
      <div class="mx-auto flex justify-between items-center">
        <router-link to="/" class="text-2xl text-white">
          <h1 class="ml-1 text-3xl font-bold">
            <u>KnowYourWealth</u>
          </h1>
        </router-link>
        <nav>
          <router-link to="/signup" class="text-2xl text-white mr-4">Sign Up</router-link>
        </nav>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class=" mx-auto">
      <router-view></router-view>
    </main>

    <!-- Footer -->
    <footer class="text-white py-4" style="background-color: #2c3e50;">
      <div class="max-w-7xl mx-auto text-center">
        <p>&copy; 2024 KnowYourWealth - All Rights Reserved</p>
      </div>
    </footer>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "App",
});
</script>

<style scoped>
body {
  font-family: 'Arial', sans-serif;
}
</style>
