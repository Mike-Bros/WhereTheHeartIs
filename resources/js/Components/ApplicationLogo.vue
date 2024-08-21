<template>
    <img
        :src="getAssetUrl('images/logos/logo.svg')"
        alt="Logo"
        class="w-20 h-20"
    />
</template>

<script setup>
import { computed } from "vue";

// Base URL for your assets
const baseUrl = computed(() => {
    return `${window.location.origin}/`; // This gets your app's base URL
});

// Helper function to get the full asset URL
function getAssetUrl(path) {
    return baseUrl.value + path;
}
</script>
