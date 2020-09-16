<template>
  <div>
    <Error :error="error" />
    <b-row>
      <b-col v-for="stream in streams" :key="stream.id" sm="6" xl="4" class="pb-3">
        <b-card :href="stream" :title="stream.name" :sub-title="stream.id">
          <b-img fluid :src="stream.route" class="pb-3" />
          <b-link :href="stream.route" class="card-link">
            View Motion Stream
          </b-link>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Error from '~/components/Error.vue'

export default Vue.extend({
  components: {
    Error
  },

  data (): {streams: {id: string, name: string, route: string}[], error: Error|null} {
    return {
      streams: [],
      error: null
    }
  },

  mounted () {
    fetch('/api/streams')
      .then(response => response.json())
      .then((data) => {
        this.streams = data.streams
      })
      .catch((err) => {
        this.error = err
      })
  }
})
</script>
