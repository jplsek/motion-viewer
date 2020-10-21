<template>
  <main>
    <b-row>
      <b-col v-for="movie in movies" :key="movie.name" sm="6" xl="4" class="pb-3">
        <b-card>
          <b-card-title>
            <nuxt-link :to="'/movies/' + movie.api.split(/[\\/]/).pop()">
              {{ movie.name }}
            </nuxt-link>
          </b-card-title>
          <b-card-sub-title>
            {{ new Date(movie.modified).toLocaleString() }}
          </b-card-sub-title>
          <b-embed type="video" controls class="pb-3">
            <source :src="movie.route" type="video/mp4">
          </b-embed>
          <!-- Download button for Firefox -->
          <b-link :href="movie.route" class="card-link">
            Download
          </b-link>
        </b-card>
      </b-col>
    </b-row>
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
