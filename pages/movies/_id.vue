<template>
  <main>
    <div v-if="!movie" class="text-center">
      <b-spinner label="Loading..." />
    </div>
    <b-row v-else class="justify-content-center">
      <b-col sm="10">
        <b-card :title="movie.name" :sub-title="new Date(movie.modified).toLocaleString()">
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
  data (): {
      movie: {name: string, route: string}|null,
      error: Error|null
      } {
    return {
      movie: null,
      error: null
    }
  },

  head: {
    title: 'Movie'
  },

  mounted () {
    fetch(`/api/movies/${this.$route.params.id}`)
      .then(response => response.json())
      .then((data) => {
        this.movie = data
      })
      .catch((err) => {
        this.error = err
      })
  }
})
</script>
