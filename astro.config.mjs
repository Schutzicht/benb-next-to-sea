import { defineConfig } from 'astro/config';
import tailwind from "@astrojs/tailwind";

// https://astro.build/config
export default defineConfig({
  integrations: [tailwind()],
  i18n: {
    defaultLocale: "nl",
    locales: ["nl", "en", "de"],
    routing: {
      prefixDefaultLocale: true
    }
  }
});
