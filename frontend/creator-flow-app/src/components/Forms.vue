<script setup>
    import CreatorFlow from './CreatorFlow.vue'
</script>

<template>
    <div class="forms bg-teal-300 border-round-2xl shadow-8">
        <RouterView />
    </div>
</template>

<style scoped>
.forms{
    display: flex;
    align-items: center;
    justify-content: space-evenly;
}
</style>