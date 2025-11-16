<template>
  <div class="modal fade" id="reviewModal" tabindex="-1" aria-labelledby="reviewModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="reviewModalLabel">
            {{ isEdit ? 'Edit Review' : 'Add New Review' }}
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label for="reviewerName" class="form-label">Reviewer Name *</label>
              <input 
                type="text" 
                class="form-control" 
                id="reviewerName" 
                v-model="formData.reviewer_name"
                required
                placeholder="Enter your name"
              >
            </div>
            <div class="mb-3">
              <label for="rating" class="form-label">Rating *</label>
              <div class="rating-input mb-2">
                <span 
                  v-for="n in 5" 
                  :key="n"
                  @click="formData.rating = n"
                  @mouseover="hoverRating = n"
                  @mouseleave="hoverRating = 0"
                  class="star"
                  :class="{ 'filled': n <= (hoverRating || formData.rating) }"
                >
                  {{ n <= (hoverRating || formData.rating) ? '★' : '☆' }}
                </span>
                <span class="form-text">{{ formData.rating }}/5</span>
              </div>
              <input 
                type="number" 
                class="form-control" 
                id="rating" 
                v-model.number="formData.rating"
                min="1"
                max="5"
                required
              >
            </div>
            <div class="mb-3">
              <label for="reviewText" class="form-label">Review *</label>
              <textarea 
                class="form-control" 
                id="reviewText" 
                rows="4"
                v-model="formData.review_text"
                required
                minlength="10"
                placeholder="Share your thoughts about this movie..."
                :maxlength="500"
                :class="{ 'is-invalid': formData.review_text.length > 0 && formData.review_text.length < 10 }"
              ></textarea>
              <div class="form-text" :class="{ 'text-danger': formData.review_text.length > 0 && formData.review_text.length < 10 }">
                {{ formData.review_text.length }}/500 characters
                <span v-if="formData.review_text.length > 0 && formData.review_text.length < 10">
                  (minimum 10 characters required)
                </span>
              </div>
            </div>
            <div class="mb-3">
              <label for="reviewDate" class="form-label">Review Date *</label>
              <input 
                type="date" 
                class="form-control" 
                id="reviewDate" 
                v-model="formData.review_date"
                :max="new Date().toISOString().split('T')[0]"
                required
              >
            </div>
            <div class="mb-3 form-check">
              <input 
                type="checkbox" 
                class="form-check-input" 
                id="reviewVerified"
                v-model="formData.is_verified"
              >
              <label class="form-check-label" for="reviewVerified">
                Mark as Verified Review
              </label>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-primary rounded-pill" @click="handleSubmit" data-bs-dismiss="modal">
            <i class="bi bi-check-circle"></i> {{ isEdit ? 'Update Review' : 'Submit Review' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReviewModal',
  props: {
    review: {
      type: Object,
      default: null,
      validator(value) {
        if (value === null) return true
        return typeof value.reviewer_name === 'string' && 
               typeof value.rating === 'number' &&
               value.rating >= 1 && value.rating <= 5
      }
    },
    movieId: {
      type: Number,
      default: null,
      validator(value) {
        return value === null || (typeof value === 'number' && value > 0)
      }
    },
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      formData: {
        reviewer_name: '',
        rating: 5,
        review_text: '',
        review_date: new Date().toISOString().split('T')[0],
        is_verified: false
      },
      hoverRating: 0
    }
  },
  watch: {
    review: {
      handler(newReview) {
        if (newReview) {
          this.formData = { ...newReview }
        } else {
          this.resetForm()
        }
      },
      immediate: true
    }
  },
  methods: {
    handleSubmit() {
      if (!this.formData.reviewer_name || !this.formData.review_text) {
        alert('Please fill in all required fields')
        return
      }
      if (this.formData.review_text.trim().length < 10) {
        alert('Review text must be at least 10 characters long')
        return
      }
      if (this.formData.rating < 1 || this.formData.rating > 5) {
        alert('Rating must be between 1 and 5')
        return
      }
      const reviewData = { 
        ...this.formData,
        movie_id: this.formData.movie_id || this.movieId
      }
      this.$emit('save-review', reviewData)
      this.resetForm()
    },
    resetForm() {
      this.formData = {
        reviewer_name: '',
        rating: 5,
        review_text: '',
        review_date: new Date().toISOString().split('T')[0],
        is_verified: false
      }
      this.hoverRating = 0
    }
  }
}
</script>

<style scoped>
* {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.form-text {
  color: #667788;
}
.rating-input {
  display: flex;
  align-items: center;
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

.star {
  font-size: 2rem;
  cursor: pointer;
  color: #00e054;
  transition: all 0.2s;
  user-select: none;
}

.star:hover {
  transform: scale(1.2);
}

.star.filled {
  color: #00e054;
}

/* Added responsive design for mobile */
@media (max-width: 576px) {
  .star {
    font-size: 1.5rem;
  }
}
</style>
