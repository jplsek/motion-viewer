<template>
  <main>
    <b-row>
      <b-col sm="4">
        <b-button-group class="pb-3">
          <b-button
            variant="outline-dark"
            title="Icon view"
            :pressed="view === 'icon'"
            @click="setViewStacked"
          >
            <b-icon-view-stacked />
          </b-button>
          <b-button
            variant="outline-dark"
            title="List view"
            :pressed="view === 'list'"
            @click="setViewList"
          >
            <b-icon-view-list />
          </b-button>
        </b-button-group>
      </b-col>
      <b-col sm="4">
        <div class="d-flex justify-content-center">
          <b-pagination
            v-model="currentPage"
            :total-rows="total"
            :per-page="perPage"
          />
        </div>
      </b-col>
    </b-row>
    <Error :error="error" />
    <div v-if="!movies" class="text-center">
      <b-spinner label="Loading..." />
    </div>
    <div v-else-if="movies.length > 0" :movies="movies">
      <MoviesIconView v-if="view === 'icon'" :movies="movies" />
      <MoviesListView v-if="view === 'list'" :movies="movies" />
    </div>
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
import MoviesIconView from '~/components/MoviesIconView.vue'
import MoviesListView from '~/components/MoviesListView.vue'

export default Vue.extend({

  components: {
    Error,
    MoviesIconView,
    MoviesListView
  },

  data (): {
      movies: {name: string, route: string}[]|null,
      error: Error|null,
      perPage: number
      currentPage: number
      total: number,
      view: string
      } {
    return {
      movies: null,
      error: null,
      perPage: 10,
      currentPage: 1,
      total: 0,
      view: ''
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
    this.view = localStorage.getItem('view') || 'icon'
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
    },

    setViewStacked () {
      localStorage.setItem('view', 'icon')
      this.view = 'icon'
    },

    setViewList () {
      localStorage.setItem('view', 'list')
      this.view = 'list'
    }
  }
})
</script>
