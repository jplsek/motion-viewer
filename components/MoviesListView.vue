<template>
  <main class="table-responsive">
    <table class="table">
      <thead>
        <th>Id</th>
        <th>Date</th>
        <th>Actions</th>
      </thead>
      <tr v-for="movie in movies" :key="movie.name">
        <td>
          <nuxt-link :to="'/movies/' + movie.api.split(/[\\/]/).pop()">
            {{ movie.name }}
          </nuxt-link>
        </td>
        <td>
          {{ new Date(movie.modified).toLocaleString() }}
        </td>
        <!-- Download button for Firefox -->
        <td>
          <b-link :href="movie.route" class="card-link">
            Download
          </b-link>
        </td>
      </tr>
    </table>
  </main>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    movies: {
      type: Array,
      default () { return [] }
    }
  }
})
</script>
