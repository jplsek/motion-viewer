<template>
  <div class="wrapper bg-light">
    <Header />
    <b-container class="py-3" fluid>
      <nuxt />
    </b-container>
  </div>
</template>

<script lang='ts'>
import Header from '~/components/Header.vue'

export default {
  components: {
    Header
  }
}
</script>

<style scoped>
.wrapper {
  min-height: 100vh
}
</style>
