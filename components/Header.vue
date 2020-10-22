<template>
  <b-navbar toggleable="sm" type="dark" variant="dark">
    <nuxt-link class="navbar-brand" to="/">
      Motion Viewer
    </nuxt-link>

    <b-navbar-toggle target="nav-collapse" />

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <nuxt-link class="nav-link" to="/streams">
          Streams
        </nuxt-link>
        <nuxt-link class="nav-link" to="/movies">
          Movies
        </nuxt-link>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">
        <b-nav-item href="https://github.com/jplsek/motion-viewer" title="Source code">
          <b-icon-code-square />
        </b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>
