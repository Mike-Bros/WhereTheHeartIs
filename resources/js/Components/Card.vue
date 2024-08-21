<template>
    <a href="javascript:void(0);" :id="link"
       class="block rounded-lg bg-white p-6 shadow-lg ring-1 ring-black/5 transition duration-300 hover:text-black/70 hover:ring-black/20 focus:outline-none focus-visible:ring-[#FF2D20] dark:bg-zinc-900 dark:ring-zinc-800 dark:hover:text-white/70 dark:hover:ring-zinc-700 dark:focus-visible:ring-[#FF2D20]">
        <h2 class="text-xl font-semibold mb-4">{{ title }}</h2>
        <div class="text-sm text-black/70 dark:text-white/70">
            <slot></slot>
        </div>
    </a>
</template>

<script setup>
defineProps({
    title: {
        type: String,
        required: true,
    },
    link: {
        type: String,
        required: true,
    },
});
</script>
