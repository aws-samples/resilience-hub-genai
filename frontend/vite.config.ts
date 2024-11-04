// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import { resolve } from 'path';
import { defineConfig } from 'vite';
import { nodePolyfills } from 'vite-plugin-node-polyfills'
import react from '@vitejs/plugin-react';


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    nodePolyfills({
      // To add only specific polyfills, add them here. If no option is passed, adds all polyfills
      include: ['path'],
      // To exclude specific polyfills, add them to this list. Note: if include is provided, this has no effect
      exclude: [
        'http', // Excludes the polyfill for `http` and `node:http`.
      ],
      // Whether to polyfill specific globals.
      globals: {
        Buffer: true, // can also be 'build', 'dev', or false
        global: true,
        process: true,
      },
      // Override the default polyfills for specific modules.
      overrides: {
        // Since `fs` is not supported in browsers, we can use the `memfs` package to polyfill it.
        fs: 'memfs',
      },
      // Whether to polyfill `node:` protocol imports.
      protocolImports: true,
    })
  ],
  server: {
    port: 8080,
  },
  root: resolve(__dirname, 'src/pages'),
  publicDir: resolve(__dirname, 'public'),
  build: {
    outDir: resolve(__dirname, './dist'),
    rollupOptions: {
      input: {
        welcome: resolve(__dirname, './src/pages/welcome/index.html'),
        report: resolve(__dirname, './src/pages/report/index.html'),
      }
    }
  }
});
