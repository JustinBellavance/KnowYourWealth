module.exports = {
    root: true,
    env: {
      browser: true,
      es2021: true,
    },
    parser: 'vue-eslint-parser',
    parserOptions: {
      parser: '@typescript-eslint/parser',
      ecmaVersion: 2021,
      sourceType: 'module',
    },
    plugins: [
      'vue',
      '@typescript-eslint',
    ],
    extends: [
      'eslint:recommended',
      'plugin:vue/vue3-recommended',
      'plugin:@typescript-eslint/recommended',
    ],
    rules: {
      // Customize your rules here
      '@typescript-eslint/no-unused-vars': ['error'],
      'vue/multi-word-component-names': 'off',
    },
  };
  