import { readFileSync, readdirSync, statSync, createReadStream } from 'fs'

const root = process.env.ROOT || ''
const server = process.env.SERVER || 'http://localhost'

function parseConfig (file, cb) {
  for (const line of file.split('\n')) {
    if (line.length < 1 || line[0] === '#' || line[0] === ';') {
      continue
    }

    const key = line.substr(0, line.indexOf(' '))
    const value = line.substr(line.indexOf(' ') + 1)

    cb(key, value)
  }
}

function getMotionConfig () {
  const file = readFileSync(root + '/etc/motion/motion.conf').toString()
  const config = {
    cameras: {}
  }

  parseConfig(file, (key, value) => {
    if (key === 'camera') {
      config.cameras[value] = {}
    } else {
      config[key] = value
    }
  })

  for (const camera in config.cameras) {
    const file = readFileSync(root + camera).toString()

    parseConfig(file, (key, value) => {
      config.cameras[camera][key] = value
    })
  }

  return config
}

function getStreams (motionConfig) {
  const streams = []

  for (const camera in motionConfig.cameras) {
    const id = motionConfig.cameras[camera].camera_id
    const name = motionConfig.cameras[camera].camera_name
    const port = motionConfig.stream_port
    const stream = `${server}:${port}/${id}/stream`
    streams.push({ id, name, route: stream })
  }

  return streams
}

const motionConfig = getMotionConfig()
const streams = getStreams(motionConfig)

function getMovies (page) {
  const dir = `${root}${motionConfig.target_dir}`
  const files = readdirSync(dir).filter(file => file.includes('.mkv'))
  let movies = []

  for (const file of files) {
    const filePath = `${root}${motionConfig.target_dir}/${file}`
    const route = `/api/movies/${file}`
    const stats = statSync(filePath)
    const api = `/api/movies/${file.substr(0, file.lastIndexOf('.'))}`
    movies.push({
      name: file,
      route,
      stats,
      filePath,
      api
    })
  }

  // sort by date
  movies = movies.sort((a, b) => b.stats.mtimeMs - a.stats.mtimeMs)

  // slice result
  const pageSize = 10
  const from = (page - 1) * pageSize
  movies = movies.slice(from, from + pageSize)

  return { movies, total: files.length }
}

// cache movies for individual requests
let movies = []

function getCleanMovie (movie) {
  const { name, route, stats, api } = movie
  return { name, route, modified: stats.mtime, api }
}

function getCleanedMovies (page) {
  const moviesApi = getMovies(page)
  movies = moviesApi.movies
  const cleanedMovies = []

  // remove not needed keys
  for (const i in movies) {
    cleanedMovies.push(getCleanMovie(movies[i]))
  }

  return { movies: cleanedMovies, total: moviesApi.total }
}

export default function (req, res, next) {
  if (req.url === '/api/streams') {
    res.setHeader('Content-Type', 'application/json')
    res.end(JSON.stringify({ streams }))
    return
  } else if (req.url === '/api/movies') {
    res.setHeader('Content-Type', 'application/json')
    res.end(JSON.stringify(getCleanedMovies(1)))
    return
  } else if (req.url.includes('/api/movies?p=')) {
    const page = parseInt(req.url.split('=')[1])
    res.setHeader('Content-Type', 'application/json')
    res.end(JSON.stringify(getCleanedMovies(page)))
    return
  } else if (req.url.includes('/api/movies/')) {
    // only run if needed, because the client usually initially calls /api/movies already.
    if (movies.length === 0) {
      movies = getMovies()
    }

    for (const movie of movies) {
      if (req.url === movie.route) {
        const filePath = `${root}${motionConfig.target_dir}/${movie.name}`
        res.setHeader('Content-Type', 'video/x-matroska')
        res.setHeader('Content-Length', movie.stats.size)
        const readStream = createReadStream(filePath)
        readStream.pipe(res)
        return
      } else if (req.url === movie.api) {
        res.setHeader('Content-Type', 'application/json')
        res.end(JSON.stringify(getCleanMovie(movie)))
        return
      }
    }
  }

  next()
}
