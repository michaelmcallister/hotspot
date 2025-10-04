import { defineConfig, devices } from '@playwright/test';
import path from 'path';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  outputDir: path.join(__dirname, 'artefacts'),
  use: {
    baseURL: 'http://localhost:5173',
    screenshot: 'on',
    video: 'on',
    launchOptions: {
      slowMo: 200,
    },
  },

  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1920, height: 1080 },
        deviceScaleFactor: 1,
      },
    },
  ],

  webServer: {
    command: 'cd .. && make dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
