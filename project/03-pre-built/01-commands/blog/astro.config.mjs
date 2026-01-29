// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
	site: 'https://d1swik7o06rp8f.cloudfront.net',
	integrations: [mdx(), sitemap(), tailwind()],
});
