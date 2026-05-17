/** @type {import('eslint').Linter.Config} */
module.exports = {
  root: true,
  env: {
    browser: true,
    es2020: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-type-checked',
    'plugin:vue/vue3-recommended',
    'prettier',
  ],
  parser: 'vue-eslint-parser',
  parserOptions: {
    parser: '@typescript-eslint/parser',
    ecmaVersion: 2020,
    sourceType: 'module',
    project: ['./tsconfig.json'],
    extraFileExtensions: ['.vue'],
  },
  plugins: ['@typescript-eslint'],
  rules: {
    'no-console': 'warn',
    'no-debugger': 'error',
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    'vue/multi-word-component-names': 'off',
  },
}
