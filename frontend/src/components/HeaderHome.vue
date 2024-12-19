<template>
    <header class="header">
      <div class="logo">
        <router-link to="/" class="logo-link">
          <span class="logo-text">KnowYourWealth</span>
          <img :src="logo" alt="KnowYourWealth Logo" />
        </router-link>
      </div>
      <nav class="navigation">
        <router-link to="/about" class="nav-link">About</router-link>
        <a href="https://discord.gg/qxN52prMyM" target="_blank" class="nav-link">Community</a>
        <router-link to="/signup" class="nav-link">Sign Up</router-link>
      </nav>
    </header>
  </template>
  
  <script setup lang="ts">
  import logo from '@/assets/logo.svg';

  </script>
  
  <style scoped>
  /* Header styling */
  .header {
    height: 60px;  /* Set the height of your navbar */
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: white;
  }
  
  /* Logo styling */
  .logo {
    padding: 1rem 0;
    align-items: center; 
  }
  
  .logo-link {
    display: flex;
    justify-content: space-between;
  }
  
  .logo img {
    width: 40px; 
    height: auto;
    margin-left : 5px;
  }
  
  .logo-text {
    font-size: 1.5rem;
    font-weight: bold;
    color: #333; 
    text-decoration: none;
  }
  
  /* Navigation styling */
  .navigation {
    display: flex;
    gap: 1.5rem;
  }
  
  .nav-link {
    font-size: 1.5rem;
    color: black; 
    text-decoration: none;
  }
  
  .nav-link:hover {
    color: #007bff; /* Hover effect */
  }
  
  /* Responsive Design */
  @media (max-width: 768px) {
    .header {
      flex-direction: column;
      align-items: flex-start;
    }
  
    .navigation {
      flex-direction: column;
      gap: 1rem;
    }
  }
  </style>
  