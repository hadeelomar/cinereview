# Create your models here.
"""
Models for the movie review application.

This module contains the Movie and Review models with proper validation,
relationships, and custom methods.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Movie(models.Model):
    """
    Main model representing a movie with validation.

    Attributes:
        title (str): The movie title (max 200 characters)
        description (str): Genre or detailed description
        director (str): Director name (max 100 characters)
        release_year (int): Year of release (validated 1900-2100)
        release_date (date): Specific release date
        is_featured (bool): Whether movie is featured on homepage
        poster_url (str): Optional URL to movie poster image
        duration_minutes (int): Optional runtime in minutes
        created_at (datetime): Auto-generated creation timestamp
        updated_at (datetime): Auto-updated modification timestamp
    """

    title = models.CharField(max_length=200, help_text="Movie title (required)")
    description = models.TextField(
        help_text="Genre or detailed description of the movie"
    )
    director = models.CharField(max_length=100, help_text="Director's name (required)")
    release_year = models.IntegerField(
        validators=[
            MinValueValidator(1900, message="Release year must be 1900 or later"),
            MaxValueValidator(2100, message="Release year must be before 2100"),
        ],
        help_text="Year the movie was released",
    )
    release_date = models.DateField(help_text="Specific release date")
    is_featured = models.BooleanField(default=False, help_text="Mark as featured movie")
    poster_url = models.URLField(
        max_length=500, blank=True, null=True, help_text="URL to movie poster image"
    )
    duration_minutes = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
        help_text="Movie runtime in minutes",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when movie was added"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when movie was last updated"
    )

    class Meta:
        """Meta options for Movie model."""

        ordering = ["-release_year", "title"]
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["release_year"]),
        ]

    def __str__(self) -> str:
        """
        String representation of Movie.

        Returns:
            str: Movie title and release year
        """
        return f"{self.title} ({self.release_year})"

    def clean(self) -> None:
        """
        Validate model data before saving.

        Raises:
            ValidationError: If validation fails
        """
        super().clean()
        if self.release_year and self.release_date:
            if self.release_year != self.release_date.year:
                raise ValidationError(
                    "Release year must match the year in release date"
                )

    def get_average_rating(self) -> float:
        """
        Calculate average rating from all reviews.

        Returns:
            float: Average rating (0.0 if no reviews)
        """
        reviews = self.reviews.all()
        if not reviews:
            return 0.0
        total = sum(review.rating for review in reviews)
        return round(total / len(reviews), 1)

    def get_review_count(self) -> int:
        """
        Get total number of reviews for this movie.

        Returns:
            int: Number of reviews
        """
        return self.reviews.count()


class Review(models.Model):
    """
    Secondary model representing a review for a movie.

    One-to-many relationship: one movie can have many reviews.

    Attributes:
        movie (ForeignKey): Reference to the Movie being reviewed
        reviewer_name (str): Name of the person reviewing
        review_text (str): The actual review content
        rating (int): Rating from 1-5 stars (validated)
        review_date (date): Date when review was written
        is_verified (bool): Whether review is verified/approved
        helpful_count (int): Number of users who found review helpful
        created_at (datetime): Auto-generated creation timestamp
        updated_at (datetime): Auto-updated modification timestamp
    """

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="Movie being reviewed",
    )
    reviewer_name = models.CharField(max_length=100, help_text="Name of the reviewer")
    review_text = models.TextField(
        max_length=500, help_text="Review content (max 500 characters)"
    )
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Rating must be at least 1 star"),
            MaxValueValidator(5, message="Rating cannot exceed 5 stars"),
        ],
        help_text="Rating from 1-5 stars",
    )
    review_date = models.DateField(help_text="Date of review")
    is_verified = models.BooleanField(
        default=False, help_text="Mark as verified review"
    )
    helpful_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Number of users who found this helpful",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when review was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when review was last updated"
    )

    class Meta:
        """Meta options for Review model."""

        ordering = ["-review_date", "-created_at"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        indexes = [
            models.Index(fields=["movie", "-review_date"]),
            models.Index(fields=["rating"]),
        ]

    def __str__(self) -> str:
        """
        String representation of Review.

        Returns:
            str: Reviewer name and movie title
        """
        return f"Review by {self.reviewer_name} for {self.movie.title}"

    def clean(self) -> None:
        """
        Validate review data before saving.

        Raises:
            ValidationError: If validation fails
        """
        super().clean()
        if self.review_text and len(self.review_text.strip()) < 10:
            raise ValidationError("Review text must be at least 10 characters long")

    def get_star_display(self) -> str:
        """
        Get visual star representation of rating.

        Returns:
            str: Star characters representing rating
        """
        return "★" * self.rating + "☆" * (5 - self.rating)
