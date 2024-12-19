<template>
  <div id="app">


    <!-- Main Content Area -->
    <main class=" mx-auto">
      <router-view></router-view>
    </main>

    <!-- Footer -->
    <footer class="text-black py-4" style="background-color: white;">
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

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: #f9f9f9;
}

.logo {
  display: flex;
  align-items: center;
}

.logo img {
  height: 40px;
  margin-right: 10px;
}

.navigation a {
  margin: 0 10px;
  text-decoration: none;
  color: #333;
}
</style>
