import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../dist'
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@utils': resolve(__dirname, './src/utils'),
      '@routes': resolve(__dirname, './src/routes'),
      '@common': resolve(__dirname, './src/common'),
      '@auth': resolve(__dirname, './src/auth')
    },
  }
});
