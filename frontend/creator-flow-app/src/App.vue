<script setup>
  import Forms from './components/Forms.vue';
  import Header from './components/Header.vue';
</script>

<template>
  <div class="container">
    <Header />
    <br><br>
    <RouterView />
    <br><br>
  </div>
</template>

<style scoped>
</style>
