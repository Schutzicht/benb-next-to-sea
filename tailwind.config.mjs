/** @type {import('tailwindcss').Config} */
export default {
    content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
    theme: {
        extend: {
            fontFamily: {
                heading: ['"Playfair Display"', 'serif'],
                body: ['"Inter"', 'sans-serif'],
            },
            colors: {
                'sea-blue': '#0e4c92',
                'dune-sand': '#E7E5E4',
                'foam-white': '#f8fcfd',
                'lighthouse-red': '#d32f2f',
            },
        },
    },
    plugins: [],
}
