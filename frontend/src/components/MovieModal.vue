<template>
  <div class="modal fade" id="movieModal" tabindex="-1" aria-labelledby="movieModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="movieModalLabel">
            {{ isEdit ? 'Edit Movie' : 'Add New Movie' }}
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="movieTitle" class="form-label">Title *</label>
              <input 
                type="text" 
                class="form-control" 
                id="movieTitle" 
                v-model="formData.title"
                placeholder="Enter movie title"
              >
            </div>
            <div class="col-md-6 mb-3">
              <label for="movieDirector" class="form-label">Director *</label>
              <input 
                type="text" 
                class="form-control" 
                id="movieDirector" 
                v-model="formData.director"
                placeholder="Enter director name"
              >
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="movieGenre" class="form-label">Genre *</label>
              <select 
                class="form-select" 
                id="movieGenre" 
                v-model="formData.description"
              >
                <option value="">Select a genre</option>
                <option value="Action">Action</option>
                <option value="Comedy">Comedy</option>
                <option value="Drama">Drama</option>
                <option value="Horror">Horror</option>
                <option value="Sci-Fi">Sci-Fi</option>
                <option value="Romance">Romance</option>
                <option value="Thriller">Thriller</option>
                <option value="Documentary">Documentary</option>
              </select>
            </div>
            <div class="col-md-6 mb-3">
              <label for="movieYear" class="form-label">Release Year *</label>
              <input 
                type="number" 
                class="form-control" 
                id="movieYear" 
                v-model.number="formData.release_year"
                min="1900"
                max="2100"
                placeholder="e.g., 2024"
              >
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="movieDate" class="form-label">Release Date *</label>
              <input 
                type="date" 
                class="form-control" 
                id="movieDate" 
                v-model="formData.release_date"
              >
            </div>
          </div>

          <div class="mb-3">
            <label for="moviePoster" class="form-label">Poster URL</label>
            <input 
              type="url" 
              class="form-control" 
              id="moviePoster" 
              v-model="formData.poster_url"
              placeholder="https://example.com/poster.jpg"
            >
            <div class="form-text">Enter a valid URL to a movie poster image</div>
          </div>

          <div class="mb-3 form-check">
            <input 
              type="checkbox" 
              class="form-check-input" 
              id="movieFeatured"
              v-model="formData.is_featured"
            >
            <label class="form-check-label" for="movieFeatured">
              Mark as Featured Movie ★
            </label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-primary rounded-pill" @click="handleSubmit" data-bs-dismiss="modal">
            <i class="bi bi-check-circle"></i> {{ isEdit ? 'Update Movie' : 'Add Movie' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MovieFormModal',
  props: {
    movie: {
      type: Object,
      default: null
    },
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      formData: {
        title: '',
        director: '',
        description: '',
        release_year: new Date().getFullYear(),
        release_date: new Date().toISOString().split('T')[0],
        poster_url: '',
        duration_minutes: null,
        is_featured: false
      }
    }
  },
  watch: {
    movie: {
      handler(newMovie) {
        if (newMovie) {
          this.formData = { ...newMovie }
        } else {
          this.resetForm()
        }
      },
      immediate: true,
      deep: true
    }
  },
  methods: {
    handleSubmit() {
      if (!this.formData.title || !this.formData.director || !this.formData.description) {
        alert('Please fill in all required fields')
        return
      }
      
      if (this.formData.release_year < 1900 || this.formData.release_year > 2100) {
        alert('Release year must be between 1900 and 2100')
        return
      }

      const movieData = { ...this.formData }
      this.$emit('save-movie', movieData)
      this.resetForm()
    },
    resetForm() {
      this.formData = {
        title: '',
        director: '',
        description: '',
        release_year: new Date().getFullYear(),
        release_date: new Date().toISOString().split('T')[0],
        poster_url: '',
        duration_minutes: null,
        is_featured: false
      }
    }
  }
}
</script>

<style scoped>
* {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.modal-content {
  background: #2c3440;
  border-radius: 12px;
  color: #ffffff;
}

.modal-header {
  background: #1e252f;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.modal-title {
  color: #00e054;
  font-weight: 600;
}

.modal-body {
  background: #2c3440;
  color: #ffffff;
  padding: 2rem;
}

.modal-footer {
  background: #2c3440;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.form-label {
  color: #9ab;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.form-control,
.form-select {
  background: #1e252f;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #ffffff;
  padding: 0.625rem 0.875rem;
  border-radius: 4px;
}

.form-control:focus,
.form-select:focus {
  background: #1e252f;
  border-color: #00e054;
  color: #ffffff;
  box-shadow: 0 0 0 3px rgba(0, 224, 84, 0.15);
}

.form-control::placeholder {
  color: #667788;
}

.form-select option {
  background: #1e252f;
  color: #ffffff;
}

.form-text {
  color: #667788;
  font-size: 0.8125rem;
}

.form-check-input {
  background-color: #1e252f;
  border-color: rgba(255, 255, 255, 0.2);
  cursor: pointer;
}

.form-check-input:checked {
  background-color: #00e054;
  border-color: #00e054;
}

.form-check-input:focus {
  box-shadow: 0 0 0 3px rgba(0, 224, 84, 0.15);
}

.form-check-label {
  color: #9ab;
  cursor: pointer;
}

.btn-close {
  filter: brightness(0) invert(1);
}

.btn-secondary {
  background: #667788;
  border: none;
  color: #ffffff;
  padding: 0.625rem 1.5rem;
  font-weight: 500;
}

.btn-secondary:hover {
  background: #556677;
}

.btn-primary {
  background: #00e054;
  border: none;
  color: #ffffff;
  padding: 0.625rem 1.5rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary:hover {
  background: #00c048;
  transform: translateY(-1px);
}
</style>