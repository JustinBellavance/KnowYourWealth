<template>
  <div class="landing-page">
    <Header></Header>
    <main class="hero-section">
      <div class="hero-content">
        <div class="text">
          <h1>
            <span class="word1">Track</span>
            <span class="word2">your</span>
            <span class="word3">growing</span>
            <span class="highlight">Wealth</span>
          </h1>
          <p>An all-encompassing net worth tracker made by Canadians, for Canadians.</p>
        </div>
        <button class="waitlist-button">Join the waitlist</button>
      </div>
      <div class="background">
        <!-- <img src="/path/to/clouds.png" alt="Cloud Background" /> -->
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import Header from "@/components/HeaderHome.vue"
</script>

<style scoped>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Roboto:wght@400;500;700&display=swap');

.landing-page {
  font-family: 'Roboto', sans-serif; /* Default font for the rest of the page */
  color: #333;
  text-align: center;
  font-size: 2rem;
  margin-top:10px;
}

.hero-section {
  height: 90vh; /* Full height of the viewport */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  position: relative;
}

.hero-content {
  max-width: 650px;
  margin: 0 auto;
}

.text {
  margin-bottom: 20px;
}

h1 {
  font-family: 'Playfair Display', serif; /* Apply Playfair Display to h1 */
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 20px;
  line-height: 1.2; /* Ensures the lines are not too far apart */
  white-space: nowrap; /* Prevent line breaks */
}

.word1 {
  font-size: 2.5rem; /* Smaller size for 'Track' */
  margin-right: 10px;
}

.word2 {
  font-size: 3rem; /* Medium size for 'your' */
  margin-right: 10px;
}

.word3 {
  font-size: 3.5rem; /* Larger size for 'growing' */
  margin-right: 2px;
}

.highlight {
  font-style: italic;
  font-size: 4rem; /* Largest size for 'Wealth' */
}

/* Enhanced Waitlist Button Styling */
.waitlist-button {
  background-color: #000; /* Black background */
  color: #fff; /* White text */
  font-size: 1.2rem;
  padding: 12px 30px;
  border: 2px solid #fff; /* White border */
  border-radius: 30px; /* Rounded corners */
  cursor: pointer;
  transition: all 0.3s ease; /* Smooth transition for hover effects */
  font-weight: 600;
  text-transform: uppercase; /* Uppercase text for a modern look */
  letter-spacing: 1px; /* Slight letter spacing for clarity */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
}

.waitlist-button:hover {
  background-color: #fff; /* White background on hover */
  color: #000; /* Black text on hover */
  transform: translateY(-2px); /* Slight lift effect on hover */
}

.waitlist-button:focus {
  outline: none; /* Remove default focus outline */
}

.waitlist-button:active {
  transform: translateY(0); /* Return to normal position when clicked */
}

.background img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: auto;
  z-index: -1;
}

.portfolio {
  padding: 50px 20px;
  background-color: #f4f4f4;
}

.portfolio .companies {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
}

.portfolio .companies img {
  height: 60px;
}
</style>
