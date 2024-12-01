/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_API_URL: string; // Declare your custom environment variables
    // Add other variables as needed
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }