<template>
  <div v-if="error" class="text-danger">
    {{ `${error.name}: ${error.message}` }}<br>
    Please check the console for more information.
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    error: {
      type: Error,
      default: null
    }
  }
})
</script>
