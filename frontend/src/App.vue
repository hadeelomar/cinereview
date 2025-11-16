<template>
  <div class="app-wrapper" @mousemove="handleMouseMove">
    <div class="animated-background">
      <div class="mouse-glow" :style="mouseGlowStyle"></div>
      
      <div class="grid-lines">
        <div v-for="i in 4" :key="`h-${i}`" class="grid-line horizontal" :style="{ top: `${i * 25}%` }"></div>
        <div v-for="i in 6" :key="`v-${i}`" class="grid-line vertical" :style="{ left: `${i * 16.66}%` }"></div>
      </div>
      
      <div class="stars-container">
        <div v-for="i in 20" :key="`star-${i}`" class="star" :style="getStarStyle(i)"></div>
      </div>
    </div>

    <div class="container">
      <header class="app-header">
        <div class="logo-section">
          <svg width="50" height="50" viewBox="0 0 50 50" fill="none" class="logo">
            <circle cx="15" cy="25" r="12" fill="#ff8000" opacity="0.7"/>
            <circle cx="25" cy="25" r="12" fill="#00e054" opacity="0.7"/>
            <circle cx="35" cy="25" r="12" fill="#40bcf4" opacity="0.7"/>
          </svg>
          <div class="title-container">
            <h1 class="app-title gradient-text">
              {{ displayedText }}
              <span v-if="showCursor" class="typing-cursor">|</span>
            </h1>
          </div>
        </div>
        <button class="btn-add" @click="openAddMovieModal" data-bs-toggle="modal" data-bs-target="#movieModal">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M8 2V14M2 8H14" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
          </svg>
          ADD
        </button>
      </header>

      <div v-if="showHelp" class="help-section">
        <div class="help-header">
          <h3>⌨️ Keyboard Shortcuts</h3>
          <button class="close-btn" @click="showHelp = false">✕</button>
        </div>
        <div class="shortcuts-grid">
          <div class="shortcut-item">
            <div class="keys">
              <kbd>Alt</kbd> + <kbd>N</kbd>
            </div>
            <span>Add new movie</span>
          </div>
          <div class="shortcut-item">
            <div class="keys">
              <kbd>/</kbd>
            </div>
            <span>Focus search</span>
          </div>
          <div class="shortcut-item">
            <div class="keys">
              <kbd>Esc</kbd>
            </div>
            <span>Close modals</span>
          </div>
        </div>
      </div>

      <div class="text-center mb-3">
        <button class="shortcuts-toggle-btn" @click="showHelp = !showHelp">
          {{ showHelp ? 'Hide' : 'Show' }} Keyboard Shortcuts
        </button>
      </div>

      <div v-if="!loading && movies.length > 0" class="controls-section">
        <div class="search-container">
          <svg class="search-icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
            <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
            <path d="M12.5 12.5L16 16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <input
            ref="searchInput"
            v-model="searchQuery"
            type="text"
            placeholder="Search films... (Press / to focus)"
            class="search-input"
          />
          <button v-if="searchQuery" @click="searchQuery = ''" class="clear-search">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M2 2L12 12M12 2L2 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <div class="filter-sort-container">
          <div class="genre-container">
            <select v-model="filterGenre" class="sort-select">
              <option value="">All Genres</option>
              <option v-for="filter in filters" :key="filter.value" :value="filter.value">
                {{ filter.label }}
              </option>
            </select>
          </div>

          <div class="sort-container">
            <select v-model="sortBy" class="sort-select">
              <option value="title">Sort by Title</option>
              <option value="year">Sort by Year</option>
              <option value="rating">Sort by Rating</option>
            </select>
          </div>

          <div class="featured-toggle">
            <label class="toggle-label">
              <input type="checkbox" v-model="showFeaturedOnly" class="toggle-input">
              <span class="toggle-slider"></span>
              <span class="toggle-text">Featured</span>
            </label>
          </div>
        </div>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading films...</p>
      </div>

      <div v-else-if="filteredMovies.length === 0" class="empty-state">
        <svg width="80" height="80" viewBox="0 0 80 80" fill="none" class="empty-icon">
          <rect x="10" y="15" width="60" height="50" rx="3" stroke="currentColor" stroke-width="2" opacity="0.2"/>
          <circle cx="20" cy="25" r="2" fill="currentColor" opacity="0.2"/>
          <circle cx="60" cy="25" r="2" fill="currentColor" opacity="0.2"/>
        </svg>
        <h3>{{ searchQuery || filterGenre || showFeaturedOnly ? 'No films found' : 'No films yet' }}</h3>
        <p>{{ searchQuery || filterGenre || showFeaturedOnly ? 'Try adjusting your search or filters' : 'Start building your collection' }}</p>
        <button class="btn-primary" @click="resetFilters" v-if="searchQuery || filterGenre || showFeaturedOnly">Clear Filters</button>
        <button class="btn-primary" @click="openAddMovieModal" data-bs-toggle="modal" data-bs-target="#movieModal" v-else>Add Film</button>
      </div>

      <div v-else class="movies-list">
        <MovieItem 
          v-for="(movie, index) in filteredMovies" 
          :key="movie.id" 
          :movie="movie"
          :index="movie.id"
          :style="{ animationDelay: `${index * 0.1}s` }"
          class="movie-item-animated"
          @edit-movie="openEditMovieModal"
          @delete-movie="confirmDeleteMovie"
          @add-review="openAddReviewModal"
          @edit-review="openEditReviewModal"
          @delete-review="confirmDeleteReview"
        />
      </div>
    </div>

    <MovieModal 
      :movie="currentMovie"
      :is-edit="isEditMovie"
      @save-movie="saveMovie"
    />

    <ReviewModal 
      :review="currentReview"
      :movie-id="currentMovieId"
      :is-edit="isEditReview"
      @save-review="saveReview"
    />

    <div class="modal fade" id="confirmModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content modal-modern">
          <div class="modal-header bg-danger text-white border-0">
            <h5 class="modal-title fw-bold">Confirm Delete</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <p class="mb-0">{{ confirmMessage }}</p>
          </div>
          <div class="modal-footer border-0">
            <button type="button" class="btn btn-secondary rounded-pill px-4" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger rounded-pill px-4" @click="executeDelete" data-bs-dismiss="modal">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="toast-container position-fixed bottom-0 end-0 p-3">
      <transition name="slide-in">
        <div v-if="toast.show" class="toast show toast-modern" role="alert">
          <div class="toast-header border-0" :class="toast.type === 'success' ? 'bg-success text-white' : 'bg-danger text-white'">
            <i class="bi me-2" :class="toast.type === 'success' ? 'bi-check-circle-fill' : 'bi-exclamation-triangle-fill'"></i>
            <strong class="me-auto">{{ toast.type === 'success' ? 'Success' : 'Error' }}</strong>
            <button type="button" class="btn-close btn-close-white" @click="toast.show = false"></button>
          </div>
          <div class="toast-body">
            {{ toast.message }}
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import MovieItem from './components/MovieItem.vue'
import MovieModal from './components/MovieModal.vue'
import ReviewModal from './components/ReviewModal.vue'
import * as bootstrap from 'bootstrap'

export default {
  components: {
    MovieItem,
    MovieModal,
    ReviewModal
  },
  data() {
    return {
      movies: [],
      currentMovie: null,
      currentReview: null,
      currentMovieId: null,
      isEditMovie: false,
      isEditReview: false,
      searchQuery: '',
      filterGenre: '',
      sortBy: 'title',
      showFeaturedOnly: false,
      loading: true,
      showHelp: false,
      toast: {
        show: false,
        message: '',
        type: 'success'
      },
      confirmMessage: '',
      confirmAction: null,
      abortController: null,
      displayedText: '',
      isTypingComplete: false,
      showCursor: true,
      fullText: 'CineReview',
      mouseX: 0,
      mouseY: 0,
      filters: [
        { label: 'All', value: '' },
        { label: 'Action', value: 'Action' },
        { label: 'Comedy', value: 'Comedy' },
        { label: 'Drama', value: 'Drama' },
        { label: 'Horror', value: 'Horror' },
        { label: 'Sci-Fi', value: 'Sci-Fi' },
        { label: 'Romance', value: 'Romance' }
      ]
    }
  },
  computed: {
    mouseGlowStyle() {
      return {
        left: `${this.mouseX}px`,
        top: `${this.mouseY}px`
      }
    },
    filteredMovies() {
      let filtered = [...this.movies]

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(movie => 
          movie.title.toLowerCase().includes(query) ||
          movie.director.toLowerCase().includes(query)
        )
      }

      if (this.filterGenre) {
        filtered = filtered.filter(movie => movie.description === this.filterGenre)
      }

      if (this.showFeaturedOnly) {
        filtered = filtered.filter(movie => movie.is_featured)
      }

      filtered.sort((a, b) => {
        if (this.sortBy === 'title') {
          return a.title.localeCompare(b.title)
        } else if (this.sortBy === 'year') {
          return b.release_year - a.release_year
        } else if (this.sortBy === 'rating') {
          const avgA = this.calculateAverageRating(a)
          const avgB = this.calculateAverageRating(b)
          return avgB - avgA
        }
        return 0
      })

      return filtered
    }
  },
  async mounted() {
    await this.fetchMovies()
    this.loading = false
    this.startTypingAnimation()
    document.addEventListener('keydown', this.handleKeyboardShortcuts)
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleKeyboardShortcuts)
    if (this.abortController) {
      this.abortController.abort()
    }
  },
  methods: {
    handleMouseMove(event) {
      this.mouseX = event.clientX
      this.mouseY = event.clientY
    },
    getStarStyle(index) {
      const x = Math.random() * 100
      const y = Math.random() * 100
      const size = Math.random() * 1.5 + 0.5
      const delay = Math.random() * 3
      return {
        left: `${x}%`,
        top: `${y}%`,
        width: `${size}px`,
        height: `${size}px`,
        animationDelay: `${delay}s`
      }
    },
    startTypingAnimation() {
      let i = 0
      this.displayedText = ''
      this.isTypingComplete = false
      this.showCursor = true

      const typingInterval = setInterval(() => {
        if (i < this.fullText.length) {
          this.displayedText = this.fullText.slice(0, i + 1)
          i++
        } else {
          clearInterval(typingInterval)
          this.isTypingComplete = true

          setTimeout(() => {
            this.showCursor = false
            setTimeout(() => {
              this.startTypingAnimation()
            }, 2000)
          }, 1000)
        }
      }, 100)
    },
    resetFilters() {
      this.searchQuery = ''
      this.filterGenre = ''
      this.sortBy = 'title'
      this.showFeaturedOnly = false
    },
    handleKeyboardShortcuts(event) {
      const isTyping = event.target.tagName === 'INPUT' || 
                       event.target.tagName === 'TEXTAREA' ||
                       event.target.isContentEditable

      if (event.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show')
        modals.forEach(modal => {
          const modalInstance = bootstrap.Modal.getInstance(modal)
          if (modalInstance) modalInstance.hide()
        })
        return
      }

      if (isTyping && event.key !== '/') return

      if ((event.altKey && event.key === 'n') || (event.altKey && event.key === 'N')) {
        event.preventDefault()
        this.openAddMovieModal()
        const modal = new bootstrap.Modal(document.getElementById('movieModal'))
        modal.show()
      }

      if (event.key === '/') {
        event.preventDefault()
        this.$refs.searchInput?.focus()
      }
    },
    showToast(message, type = 'success') {
      this.toast = { show: true, message, type }
      setTimeout(() => {
        this.toast.show = false
      }, 3000)
    },
    calculateAverageRating(movie) {
      if (!movie.reviews || movie.reviews.length === 0) return 0
      const sum = movie.reviews.reduce((acc, review) => acc + review.rating, 0)
      return sum / movie.reviews.length
    },
    async fetchWithRetry(url, options = {}, retries = 3) {
      for (let i = 0; i < retries; i++) {
        try {
          this.abortController = new AbortController()
          const response = await fetch(url, {
            ...options,
            signal: this.abortController.signal
          })
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`)
          }
          return response
        } catch (error) {
          if (i === retries - 1 || error.name === 'AbortError') throw error
          await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)))
        }
      }
    },
    async fetchMovies() {
      try {
        const response = await this.fetchWithRetry('http://localhost:8000/api/movies/')
        const data = await response.json()
        this.movies = Array.isArray(data.movies) ? data.movies : []
        
        for (let movie of this.movies) {
          await this.fetchReviewsForMovie(movie.id)
        }
      } catch (error) {
        console.error('Error fetching movies:', error)
        this.movies = []
        this.showToast('Failed to load movies. Please refresh the page.', 'error')
      }
    },
    async fetchReviewsForMovie(movieId) {
      try {
        const response = await this.fetchWithRetry(`http://localhost:8000/api/reviews/?movie_id=${movieId}`)
        const data = await response.json()
        const movie = this.movies.find(m => m.id === movieId)
        if (movie) {
          movie.reviews = Array.isArray(data.reviews) ? data.reviews : []
        }
      } catch (error) {
        console.error('Error fetching reviews:', error)
      }
    },
    openAddMovieModal() {
      this.isEditMovie = false
      this.currentMovie = null
    },
    openEditMovieModal(movie) {
      this.isEditMovie = true
      this.currentMovie = { ...movie }
    },
    async saveMovie(movieData) {
      try {
        this.loading = true
        const tempId = Date.now()
        let optimisticMovie = null
        
        if (this.isEditMovie) {
          const response = await this.fetchWithRetry(`http://localhost:8000/api/movies/${movieData.id}/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(movieData)
          })
          const data = await response.json()
          const updatedMovie = data.movie || data 
          const index = this.movies.findIndex(m => m.id === updatedMovie.id)
          if (index !== -1) {
            this.movies[index] = { ...this.movies[index], ...updatedMovie }
          }
          this.showToast('Movie updated successfully!')
        } else {
          optimisticMovie = { ...movieData, id: tempId, reviews: [] }
          this.movies.push(optimisticMovie)
          
          const response = await this.fetchWithRetry('http://localhost:8000/api/movies/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(movieData)
          })
          const data = await response.json()
          const newMovie = data.movie || data 
          newMovie.reviews = [] 
          
          const index = this.movies.findIndex(m => m.id === tempId)
          if (index !== -1) {
            this.movies[index] = newMovie
          }
          this.showToast('Movie added successfully!')
        }
      } catch (error) {
        console.error('Error saving movie:', error)
        this.showToast('Failed to save movie. Please try again.', 'error')
        if (!this.isEditMovie && optimisticMovie) {
          this.movies = this.movies.filter(m => m.id !== tempId)
        }
      } finally {
        this.loading = false
      }
    },
    confirmDeleteMovie(movieId) {
      this.confirmMessage = 'Are you sure you want to delete this movie and all its reviews?'
      this.confirmAction = () => this.deleteMovie(movieId)
      const modal = new bootstrap.Modal(document.getElementById('confirmModal'))
      modal.show()
    },
    async deleteMovie(movieId) {
      try {
        this.loading = true
        await this.fetchWithRetry(`http://localhost:8000/api/movies/${movieId}/`, {
          method: 'DELETE'
        })
        this.movies = this.movies.filter(m => m.id !== movieId)
        this.showToast('Movie deleted successfully!')
      } catch (error) {
        console.error('Error deleting movie:', error)
        this.showToast('Failed to delete movie. Please try again.', 'error')
      } finally {
        this.loading = false
      }
    },
    executeDelete() {
      if (this.confirmAction) {
        this.confirmAction()
        this.confirmAction = null
      }
    },
    openAddReviewModal(movieId) {
      this.isEditReview = false
      this.currentReview = null
      this.currentMovieId = movieId
    },
    openEditReviewModal(review) {
      this.isEditReview = true
      this.currentReview = { ...review }
      this.currentMovieId = review.movie_id
    },
    async saveReview(reviewData) {
      try {
        if (this.isEditReview) {
          const response = await this.fetchWithRetry(`http://localhost:8000/api/reviews/${reviewData.id}/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(reviewData)
          })
          const data = await response.json()
          const updatedReview = data.review || data
          const movie = this.movies.find(m => m.id === updatedReview.movie_id)
          if (movie && movie.reviews) {
            const index = movie.reviews.findIndex(r => r.id === updatedReview.id)
            if (index !== -1) {
              movie.reviews[index] = updatedReview
            }
          }
          this.showToast('Review updated successfully!')
        } else {
          const response = await this.fetchWithRetry('http://localhost:8000/api/reviews/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(reviewData)
          })
          if (!response.ok) {
            const errorData = await response.json()
            this.showToast(`Failed to save review: ${errorData.error || 'Unknown error'}`, 'error')
            return
          }
          const data = await response.json()
          const newReview = data.review || data
          const movie = this.movies.find(m => m.id === newReview.movie_id)
          if (movie) {
            if (!movie.reviews) {
              movie.reviews = []
            }
            movie.reviews.push(newReview)
          }
          this.showToast('Review added successfully!')
        }
      } catch (error) {
        console.error('Error saving review:', error)
        this.showToast('Failed to save review. Please try again.', 'error')
      }
    },
    confirmDeleteReview(reviewData) {
      this.confirmMessage = 'Are you sure you want to delete this review?'
      this.confirmAction = () => this.deleteReview(reviewData)
      const modal = new bootstrap.Modal(document.getElementById('confirmModal'))
      modal.show()
    },
    async deleteReview(reviewData) {
      try {
        await this.fetchWithRetry(`http://localhost:8000/api/reviews/${reviewData.reviewId}/`, {
          method: 'DELETE'
        })
        const movie = this.movies.find(m => m.id === reviewData.movieId)
        if (movie && movie.reviews) {
          movie.reviews = movie.reviews.filter(r => r.id !== reviewData.reviewId)
        }
        this.showToast('Review deleted successfully!')
      } catch (error) {
        console.error('Error deleting review:', error)
        this.showToast('Failed to delete review. Please try again.', 'error')
      }
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: #14181c;
  color: #fff;
  overflow-x: hidden;
}

.animated-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: radial-gradient(ellipse at center, #1a1d29 0%, #14181c 70%, #0f1115 100%);
  overflow: hidden;
}

.mouse-glow {
  position: absolute;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0, 224, 84, 0.15) 0%, transparent 70%);
  pointer-events: none;
  transform: translate(-50%, -50%);
  transition: opacity 0.3s ease;
  mix-blend-mode: screen;
}

.grid-lines {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0.08;
}

.grid-line {
  position: absolute;
}

.grid-line.horizontal {
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
}

.grid-line.vertical {
  width: 1px;
  height: 100%;
  background: linear-gradient(180deg, transparent, rgba(255, 255, 255, 0.2), transparent);
}

.stars-container {
  position: absolute;
  width: 100%;
  height: 100%;
}

.star {
  position: absolute;
  background: white;
  border-radius: 50%;
  animation: star-twinkle 4s ease-in-out infinite;
  opacity: 0.4;
}

@keyframes star-twinkle {
  0%, 100% {
    opacity: 0.2;
  }
  50% {
    opacity: 0.6;
  }
}

.container {
  position: relative;
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
  padding-top: 3.5rem;
  z-index: 1;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  animation: fade-in-down 0.8s ease-out;
}

@keyframes fade-in-down {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo {
  display: block;
  animation: logo-float 3s ease-in-out infinite;
}

@keyframes logo-float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

.app-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  min-height: 2.5rem;
}

.gradient-text {
  background: linear-gradient(135deg, #ffffff 0%, rgba(255, 255, 255, 0.6) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(0, 224, 84, 0.3);
}

.typing-cursor {
  display: inline-block;
  margin-left: 3px;
  animation: cursor-blink 1s step-end infinite;
  color: #00e054;
  font-weight: 300;
  text-shadow: 0 0 10px rgba(0, 224, 84, 0.5);
}

@keyframes cursor-blink {
  0%, 50% {
    opacity: 1;
  }
  51%, 100% {
    opacity: 0;
  }
}

.btn-add {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: #00e054;
  color: #ffffff;
  border: none;
  border-radius: 3px;
  font-weight: 700;
  font-size: 0.8125rem;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-transform: uppercase;
}

.btn-add:hover {
  background: #00c048;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 224, 84, 0.4);
}

.controls-section {
  margin-bottom: 2rem;
  flex-direction: column;
  align-items: center;
  animation: fade-in-up 0.6s ease-out 0.2s both;
}

@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.search-container {
  position: relative;
  margin-bottom: 1rem;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #667788;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.875rem 3rem 0.875rem 3rem;
  background: #2c3440;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  color: #ffffff;
  font-size: 0.9375rem;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #00e054;
  box-shadow: 0 0 0 3px rgba(0, 224, 84, 0.15);
}

.search-input::placeholder {
  color: #667788;
}

.clear-search {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #667788;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
}

.clear-search:hover {
  color: #ffffff;
}

.filter-sort-container {
  display: flex;
  gap: 1rem;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  gap: 0.5rem;
  flex: 1;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 0.5rem 1rem;
  background: #2c3440;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 3px;
  color: #9ab;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(0, 224, 84, 0.4);
  color: #ffffff;
}

.filter-btn.active {
  background: rgba(0, 224, 84, 0.15);
  border-color: #00e054;
  color: #00e054;
}

.sort-container {
  min-width: 180px;
}

.sort-select {
  width: 100%;
  padding: 0.5rem 2.5rem 0.5rem 1rem;
  background: #2c3440;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 3px;
  color: #ffffff;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg width='12' height='8' viewBox='0 0 12 8' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1.5L6 6.5L11 1.5' stroke='%23667788' stroke-width='1.5' stroke-linecap='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
}

.sort-select:hover {
  border-color: rgba(0, 224, 84, 0.4);
}

.sort-select:focus {
  outline: none;
  border-color: #00e054;
  box-shadow: 0 0 0 3px rgba(0, 224, 84, 0.15);
}

.featured-toggle {
  display: flex;
  align-items: center;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  user-select: none;
}

.toggle-input {
  display: none;
}

.toggle-slider {
  position: relative;
  width: 48px;
  height: 24px;
  background: #2c3440;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.3s ease;
}

.toggle-slider::before {
  content: '';
  position: absolute;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #667788;
  top: 2px;
  left: 2px;
  transition: all 0.3s ease;
}

.toggle-input:checked + .toggle-slider {
  background: rgba(0, 224, 84, 0.25);
  border-color: #00e054;
}

.toggle-input:checked + .toggle-slider::before {
  transform: translateX(24px);
  background: #00e054;
}

.toggle-text {
  color: #9ab;
  font-size: 0.875rem;
  font-weight: 500;
}

.toggle-input:checked ~ .toggle-text {
  color: #00e054;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 1.5rem;
  border: 3px solid rgba(0, 224, 84, 0.15);
  border-top-color: #00e054;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p,
.empty-state p {
  color: #9ab;
  font-size: 0.875rem;
}

.empty-icon {
  color: rgba(255, 255, 255, 0.1);
  margin-bottom: 1.5rem;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #fff;
}

.empty-state p {
  margin-bottom: 2rem;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: #00e054;
  color: #ffffff;
  border: none;
  border-radius: 3px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: #00c048;
  transform: translateY(-1px);
}

.movies-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.movie-item-animated {
  animation: fade-in-up 0.6s ease-out both;
}

:deep(.modal-modern) {
  border-radius: 12px;
  overflow: hidden;
}

.toast-modern {
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  border: none;
  min-width: 300px;
}

.slide-in-enter-active,
.slide-in-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-in-enter-from {
  opacity: 0;
  transform: translateX(100px);
}

.slide-in-leave-to {
  opacity: 0;
  transform: translateX(50px) scale(0.9);
}

:deep(.accordion-item) {
  background: #2a3441;
  border: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 0;
  margin-bottom: 0;
  overflow: hidden;
  transition: all 0.2s ease;
}

:deep(.accordion-item:first-child) {
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

:deep(.accordion-button) {
  background: transparent;
  color: #ffffff;
  font-weight: normal;
  font-size: 1.125rem;
  padding: 1.5rem;
  border: none;
  transition: all 0.2s ease;
  box-shadow: none;
}

:deep(.accordion-button:hover) {
  background: rgba(255, 255, 255, 0.03);
}

:deep(.accordion-button:not(.collapsed)) {
  background: #2a3441;
  color: #ffffff;
  box-shadow: none;
}

:deep(.accordion-button:focus) {
  box-shadow: none;
  border-color: transparent;
  outline: none;
}

:deep(.accordion-button::after) {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23667788'%3e%3cpath fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z'/%3e%3c/svg%3e");
  filter: none;
}

:deep(.accordion-collapse) {
  background: #2a3441;
  border: none;
}

:deep(.accordion-body) {
  background: #2a3441;
  color: #ffffff;
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

:deep(.modal-content) {
  background: #2c3440;
  border: 1px solid rgba(0, 224, 84, 0.3);
  border-radius: 12px;
  color: #ffffff;
}

:deep(.modal-header) {
  background: #1e252f;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

:deep(.modal-title) {
  color: #ffffff;
}

:deep(.modal-body) {
  background: #2c3440;
  color: #ffffff;
}

:deep(.modal-footer) {
  background: #2c3440;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.form-label) {
  color: #9ab;
  font-weight: 500;
}

:deep(.form-control),
:deep(.form-select),
:deep(textarea.form-control) {
  background: #1e252f;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

:deep(.form-control:focus),
:deep(.form-select:focus),
:deep(textarea.form-control:focus) {
  background: #1e252f;
  border-color: #00e054;
  color: #ffffff;
  box-shadow: 0 0 0 3px rgba(0, 224, 84, 0.15);
}

:deep(.form-control::placeholder) {
  color: #667788;
}

:deep(.btn-close) {
  filter: brightness(0) invert(1);
}

:deep(.form-check-input) {
  background-color: #1e252f;
  border-color: rgba(255, 255, 255, 0.2);
}

:deep(.form-check-input:checked) {
  background-color: #00e054;
  border-color: #00e054;
}

.help-section {
  background: rgba(44, 52, 64, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 224, 84, 0.3);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  animation: fade-in-up 0.4s ease-out;
}

.help-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.help-header h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #fff;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: #9ab;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
}

.close-btn:hover {
  color: #fff;
}

.shortcuts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.shortcut-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.shortcut-item .keys {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.shortcut-item span {
  color: #9ab;
  font-size: 0.875rem;
}

.shortcuts-toggle-btn {
  background: rgba(0, 224, 84, 0.15);
  border: 1px solid rgba(0, 224, 84, 0.4);
  color: #00e054;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.shortcuts-toggle-btn:hover {
  background: rgba(0, 224, 84, 0.25);
  border-color: #00e054;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
  
  .app-header {
    flex-direction: column;
    gap: 1.5rem;
    align-items: flex-start;
  }

  .filter-sort-container {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-group {
    width: 100%;
  }

  .sort-container {
    width: 100%;
    min-width: auto;
  }

  .gradient-text {
    font-size: 1.5rem;
  }
}

::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #00e054;
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: #00c048;
}
</style>
