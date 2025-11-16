<template>
  <div class="accordion-item movie-card">
    <h2 class="accordion-header">
      <button 
        class="accordion-button collapsed" 
        type="button" 
        data-bs-toggle="collapse" 
        :data-bs-target="`#collapse${index}`"
      >
        <div class="movie-main">
          <div class="title-row">
            <span class="movie-title">{{ movie.title }}</span>
            <span v-if="movie.is_featured" class="badge-featured">★</span>
          </div>
          <div class="movie-meta">
            <span>{{ releaseYear }}</span> 
            <span v-if="averageRating > 0">•</span>
            <span v-if="averageRating > 0" class="rating-stars">
              {{ '★'.repeat(Math.round(averageRating)) }}{{ '☆'.repeat(5 - Math.round(averageRating)) }}
            </span>
          </div>
        </div>
      </button>
    </h2>
    <div :id="`collapse${index}`" class="accordion-collapse collapse" data-bs-parent="#moviesAccordion">
      <div class="accordion-body">
        <div class="movie-details-row">
          <div v-if="movie.poster_url" class="movie-poster">
            <img :src="movie.poster_url" :alt="movie.title" />
          </div>
          <div class="movie-info">
            <p class="movie-description">{{ movie.director ? `Directed by ${movie.director}` : 'Director information not available' }}</p>
            
            <p class="movie-description" v-if="movie.release_date">Released: {{ formatReleaseDate(movie.release_date) }}</p>
            
            <p class="movie-description">Genre: {{ movie.description }}</p>
            
            <div v-if="movie.duration_minutes" class="movie-duration">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none" style="margin-right: 0.25rem;">
                <circle cx="7" cy="7" r="6" stroke="currentColor" stroke-width="1.5"/>
                <path d="M7 3.5V7L9.5 9.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              {{ movie.duration_minutes }} minutes
            </div>
          </div>
        </div>
        
        <div class="actions">
          <button 
            type="button" 
            class="btn-action" 
            data-bs-toggle="modal" 
            data-bs-target="#movieModal"
            @click="$emit('edit-movie', movie)"
          >
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M10 1.5L12.5 4L4.5 12H2V9.5L10 1.5Z" stroke="currentColor" stroke-width="1.5"/>
            </svg>
            Edit
          </button>
          <button 
            type="button" 
            class="btn-action"
            @click="$emit('delete-movie', movie.id)"
          >
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M2 3H12M4 3V2H10V3M5 6V10M9 6V10M3 3L4 12H10L11 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            Delete
          </button>
          <button 
            type="button" 
            class="btn-action btn-review" 
            data-bs-toggle="modal" 
            data-bs-target="#reviewModal"
            @click="$emit('add-review', movie.id)"
          >
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M7 3V11M3 7H11" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            Review
          </button>
        </div>

        <div v-if="movie.reviews && movie.reviews.length > 0" class="reviews">
          <h4 class="reviews-title">REVIEWS ({{ reviewCount }})</h4>
          <ReviewItem 
            v-for="review in movie.reviews" 
            :key="review.id" 
            :review="review"
            @edit="$emit('edit-review', review)"
            @delete="$emit('delete-review', { reviewId: review.id, movieId: movie.id })"
          />
        </div>
        <div v-else class="no-reviews">
          <p>No reviews yet</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ReviewItem from './ReviewItem.vue'

export default {
  name: 'MovieItem',
  components: {
    ReviewItem
  },
  props: {
    movie: {
      type: Object,
      required: true,
      validator: (value) => {
        return value && typeof value.title === 'string' && typeof value.director === 'string'
      }
    },
    index: {
      type: Number,
      required: true
    }
  },
  computed: {
    reviewCount() {
      return this.movie.reviews ? this.movie.reviews.length : 0
    },
    averageRating() {
      if (!this.movie.reviews || this.movie.reviews.length === 0) return 0
      const sum = this.movie.reviews.reduce((acc, review) => acc + review.rating, 0)
      return sum / this.movie.reviews.length
    },
    releaseYear() {
      if (!this.movie.release_date) return '';
      const date = new Date(this.movie.release_date);
      return isNaN(date) ? '' : date.getFullYear();
    }
  },
  methods: {
    formatReleaseDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      if (isNaN(date)) return '';
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric', 
        year: 'numeric' 
      })
    }
  }
}
</script>

<style scoped>
* {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.movie-card {
  background: #2c3440;
  border: none;
  border-radius: 4px;
  margin-bottom: 0;
  transition: all 0.2s ease;
}

.movie-card:hover {
  background: #323a48;
}

.movie-card .accordion-button {
  background: transparent;
  border: none;
  box-shadow: none;
  padding: 1.25rem 1.5rem;
  color: #fff;
}

.movie-card .accordion-button:not(.collapsed) {
  background: transparent;
  color: #fff;
  box-shadow: none;
}

.movie-card .accordion-button:focus {
  box-shadow: none;
  border: none;
}

.movie-card .accordion-button::after {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%239ab'%3e%3cpath fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z'/%3e%3c/svg%3e");
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

.movie-card .accordion-button:hover::after {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23fff'%3e%3cpath fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z'/%3e%3c/svg%3e");
}

.movie-main {
  flex: 1;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.movie-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #fff;
}

.badge-featured {
  color: #ff8000;
  font-size: 1rem;
}

.movie-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #9ab;
  font-size: 0.8125rem;
}

.rating-stars {
  color: #00e054;
  letter-spacing: 0.5px;
}

.accordion-body {
  padding: 0 1.5rem 1.5rem;
  background: transparent;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.movie-details-row {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.movie-poster {
  flex-shrink: 0;
  width: 120px;
  height: 180px;
  border-radius: 4px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.05);
}

.movie-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.movie-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.movie-description {
  color: #9ab;
  font-size: 0.875rem;
  line-height: 1.6;
  margin: 0;
}

.movie-duration {
  display: flex;
  align-items: center;
  color: #667788;
  font-size: 0.8125rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.btn-action {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.875rem;
  background: rgba(255, 255, 255, 0.05);
  border: none;
  border-radius: 3px;
  color: #9ab;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-action:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.btn-review {
  color: #00e054;
}

.btn-review:hover {
  background: rgba(0, 224, 84, 0.1);
}

.reviews {
  margin-top: 1.5rem;
}

.reviews-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 1rem;
  letter-spacing: 0.05em;
}

.no-reviews {
  text-align: center;
  padding: 2rem;
  color: #9ab;
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .movie-card .accordion-button {
    padding: 1rem;
  }
  
  .accordion-body {
    padding: 0 1rem 1rem;
  }
  
  .movie-details-row {
    flex-direction: column;
  }
  
  .movie-poster {
    width: 100%;
    max-width: 200px;
    height: 300px;
    margin: 0 auto;
  }
  
  .actions {
    flex-wrap: wrap;
  }
}
</style>