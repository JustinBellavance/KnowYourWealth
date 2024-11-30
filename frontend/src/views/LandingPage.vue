<template>
    <div class="min-h-screen bg-gradient-to-b from-blue-50 to-white flex flex-col items-center">
      <!-- Header -->
      <header class="w-full bg-blue-500 text-white py-4 px-8">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
          <h1 class="text-2xl font-bold">NetWorthTrack</h1>
          <button
            @click="navigateToSignup"
            class="bg-white text-blue-500 px-6 py-2 rounded-lg shadow-md hover:bg-blue-100"
          >
            Sign Up Free
          </button>
        </div>
      </header>
  
      <!-- Hero Section -->
      <section class="flex flex-col md:flex-row items-center justify-between max-w-7xl mx-auto py-16 px-8 gap-8">
        <div class="flex-1">
          <h2 class="text-4xl font-bold text-blue-700 mb-6">
            Take Charge of Your <span class="text-green-500">Net Worth</span>
          </h2>
          <p class="text-gray-600 mb-8 text-lg">
            Track your <span class="font-bold">cash</span>, 
            <span class="font-bold">stocks</span>, 
            <span class="font-bold">debt</span>, and 
            <span class="font-bold">real estate</span> effortlessly. 
            See your progress and stay motivated to achieve financial freedom!
          </p>
          <button
            @click="navigateToSignup"
            class="bg-blue-500 text-white text-lg px-8 py-3 rounded-lg shadow-lg hover:bg-blue-600"
          >
            Sign Up for Free
          </button>
        </div>
        <div class="flex-1">
          <img
            src="https://via.placeholder.com/500x350"
            alt="Net worth tracking illustration"
            class="rounded-lg shadow-lg"
          />
        </div>
      </section>
  
      <!-- Features Section -->
      <section class="w-full bg-blue-100 py-16">
        <div class="max-w-7xl mx-auto px-8">
          <h3 class="text-3xl font-bold text-blue-700 mb-12 text-center">
            Why Choose NetWorthTrack?
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div class="text-center p-6 bg-white rounded-lg shadow-md" v-for="feature in features" :key="feature.title">
              <img
                :src="feature.icon"
                :alt="feature.title"
                class="mx-auto mb-4"
              />
              <h4 class="text-xl font-bold text-blue-600">{{ feature.title }}</h4>
              <p class="text-gray-600">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Call to Action -->
      <section class="w-full py-16 px-8">
        <div class="max-w-7xl mx-auto text-center">
          <h3 class="text-3xl font-bold text-blue-700 mb-6">
            Ready to Track Your Net Worth?
          </h3>
          <p class="text-gray-600 text-lg mb-8">
            Sign up today for free and start making progress toward your financial goals!
          </p>
          <button
            @click="navigateToSignup"
            class="bg-green-500 text-white text-lg px-8 py-3 rounded-lg shadow-lg hover:bg-green-600"
          >
            Create Your Free Account
          </button>
        </div>
      </section>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive } from "vue";
  
  interface Feature {
    title: string;
    description: string;
    icon: string;
  }
  
  export default defineComponent({
    name: "LandingPage",
    setup() {
      // Reactive state for features
      const features = reactive<Feature[]>([
        {
          title: "Cash Tracking",
          description: "Know exactly how much cash you have and where it’s stored.",
          icon: "https://via.placeholder.com/100",
        },
        {
          title: "Stock Portfolio",
          description: "Monitor your stock holdings and market value in real-time.",
          icon: "https://via.placeholder.com/100",
        },
        {
          title: "Debt Management",
          description: "Track and pay down your debt with ease and confidence.",
          icon: "https://via.placeholder.com/100",
        },
        {
          title: "Real Estate",
          description: "Keep tabs on your real estate assets and their current worth.",
          icon: "https://via.placeholder.com/100",
        },
      ]);
  
      // Method to navigate to the signup page
      const navigateToSignup = () => {
        window.location.href = "/signup"; // Update this for router-based navigation if used
      };
  
      return {
        features,
        navigateToSignup,
      };
    },
  });
  </script>
  
  <style scoped>
  /* Add any scoped styles if needed */
  </style>
  