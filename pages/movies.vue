<template>
  <main>
    <Error :error="error" />
    <div class="d-flex justify-content-center">
      <b-pagination
        v-model="currentPage"
        :total-rows="total"
        :per-page="perPage"
      />
    </div>
    <div v-if="!movies" class="text-center">
      <b-spinner label="Loading..." />
    </div>
    <b-row v-else-if="movies.length > 0">
      <b-col v-for="movie in movies" :key="movie.name" sm="6" xl="4" class="pb-3">
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
    <div v-else>
      There are no saved movies.
    </div>
    <div class="d-flex justify-content-center">
      <b-pagination
        v-model="currentPage"
        :total-rows="total"
        :per-page="perPage"
      />
    </div>
  </main>
</template>

<script lang="ts">
import Vue from 'vue'
import Error from '~/components/Error.vue'

export default Vue.extend({

  components: {
    Error
  },

  data (): {
      movies: {name: string, route: string}[]|null,
      error: Error|null,
      perPage: number
      currentPage: number
      total: number
      } {
    return {
      movies: null,
      error: null,
      perPage: 10,
      currentPage: 1,
      total: 0
    }
  },
  head: {
    title: 'Movies'
  },

  watch: {
    currentPage (val) {
      this.getMovies(val)
    }
  },

  mounted () {
    this.getMovies(1)
  },

  methods: {
    getMovies (page: number) {
      fetch(`/api/movies?p=${page}`)
        .then(response => response.json())
        .then((data) => {
          this.movies = data.movies
          this.total = data.total
        })
        .catch((err) => {
          this.movies = []
          this.error = err
        })
    }
  }
})
</script>
