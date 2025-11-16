<template>
  <!-- Redesigned review card to match ReelRate with avatar, inline edit/delete icons -->
  <div class="review-item-reelrate">
    <div class="review-avatar">
      {{ getInitials(review.reviewer_name) }}
    </div>
    <div class="review-content-reelrate">
      <div class="review-header-reelrate">
        <div class="reviewer-details">
          <span class="reviewer-name-text">{{ review.reviewer_name }}</span>
          <div class="review-meta">
            <span class="stars-inline">
              {{ '★'.repeat(review.rating) }}{{ '☆'.repeat(5 - review.rating) }}
            </span>
            <span class="review-date-text">{{ formatDate(review.review_date) }}</span>
          </div>
        </div>
        <div class="review-actions-inline">
          <button 
            type="button" 
            class="btn-icon-inline" 
            data-bs-toggle="modal" 
            data-bs-target="#reviewModal"
            @click="$emit('edit', review)"
            title="Edit"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M11.333 2.00004C11.5081 1.82494 11.716 1.68605 11.9447 1.59129C12.1735 1.49653 12.4187 1.44775 12.6663 1.44775C12.914 1.44775 13.1592 1.49653 13.3879 1.59129C13.6167 1.68605 13.8246 1.82494 13.9997 2.00004C14.1748 2.17513 14.3137 2.383 14.4084 2.61178C14.5032 2.84055 14.552 3.08575 14.552 3.33337C14.552 3.58099 14.5032 3.82619 14.4084 4.05497C14.3137 4.28374 14.1748 4.49161 13.9997 4.66671L5.33301 13.3334L1.33301 14.6667L2.66634 10.6667L11.333 2.00004Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button 
            type="button" 
            class="btn-icon-inline btn-delete-inline"
            @click="$emit('delete', review)"
            title="Delete"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M2 4h12M5.333 4V2.667a1.333 1.333 0 0 1 1.334-1.334h2.666a1.333 1.333 0 0 1 1.334 1.334V4m2 0v9.333a1.333 1.333 0 0 1-1.334 1.334H4.667a1.333 1.333 0 0 1-1.334-1.334V4h9.334Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
      <p class="review-text-content">{{ review.review_text }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReviewItem',
  props: {
    review: {
      type: Object,
      required: true,
      validator: (value) => {
        return value && typeof value.reviewer_name === 'string' && typeof value.rating === 'number'
      }
    }
  },
  methods: {
    getInitials(name) {
      if (!name) return '?'
      const parts = name.trim().split(' ')
      if (parts.length >= 2) {
        return (parts[0][0] + parts[1][0]).toUpperCase()
      }
      return name.substring(0, 1).toUpperCase()
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
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
/* Completely redesigned to match ReelRate's review style with avatar */
* {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.review-item-reelrate {
  display: flex;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.review-item-reelrate:last-child {
  border-bottom: none;
}

.review-avatar {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff8000 0%, #ff9933 100%);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
}

.review-content-reelrate {
  flex: 1;
  min-width: 0;
}

.review-header-reelrate {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
  gap: 1rem;
}

.reviewer-details {
  flex: 1;
  min-width: 0;
}

.reviewer-name-text {
  display: block;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 0.25rem;
}

.review-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
}

.stars-inline {
  color: #00e054;
  letter-spacing: 1px;
}

.review-date-text {
  color: #9ab;
}

.review-actions-inline {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.btn-icon-inline {
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

.btn-icon-inline:hover {
  color: #ffffff;
}

.btn-delete-inline:hover {
  color: #ff6b6b;
}

.review-text-content {
  color: #c9d1d9;
  font-size: 0.9375rem;
  line-height: 1.6;
  margin: 0;
}

@media (max-width: 576px) {
  .review-header-reelrate {
    flex-direction: column;
  }
  
  .review-actions-inline {
    align-self: flex-end;
  }
}
</style>
