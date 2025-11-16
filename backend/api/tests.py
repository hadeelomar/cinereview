from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date
from .models import Movie, Review


class MovieModelTest(TestCase):
    """Tests for the Movie model, its methods, and validation."""

    def setUp(self):
        """Set up a test Movie instance before each test."""
        self.movie = Movie.objects.create(
            title="Inception",
            description="A thief who enters the dreams of others to steal secrets.",
            director="Christopher Nolan",
            release_year=2010,
            release_date=date(2010, 7, 16),
            duration_minutes=148,
            is_featured=True,
            poster_url="http://example.com/inception.jpg",
        )

    def test_movie_creation(self):
        """Test that a Movie object can be created successfully."""
        self.assertEqual(self.movie.title, "Inception")
        self.assertEqual(self.movie.director, "Christopher Nolan")
        self.assertTrue(self.movie.is_featured)
        self.assertEqual(self.movie.duration_minutes, 148)

    def test_movie_str_representation(self):
        """Test the __str__ method of the Movie model."""
        expected_str = "Inception (2010)"
        self.assertEqual(str(self.movie), expected_str)

    def test_movie_clean_validation_success(self):
        """Test Movie clean method succeeds when year and date match."""
        # No exception should be raised
        self.movie.full_clean()

    def test_movie_clean_validation_failure(self):
        """Test Movie clean method fails when release_year and release_date year do not match."""
        self.movie.release_date = date(2011, 1, 1)  # Mismatch year
        with self.assertRaisesMessage(
            ValidationError, "Release year must match the year in release date"
        ):
            self.movie.full_clean()

    def test_movie_release_year_validators(self):
        """Test MinValueValidator and MaxValueValidator on release_year."""
        # Test MinValueValidator
        self.movie.release_year = 1899
        with self.assertRaises(ValidationError):
            self.movie.full_clean()

        # Test MaxValueValidator
        self.movie.release_year = 2101
        with self.assertRaises(ValidationError):
            self.movie.full_clean()

    def test_movie_duration_minutes_validator(self):
        """Test MinValueValidator on duration_minutes."""
        self.movie.duration_minutes = 0
        with self.assertRaises(ValidationError):
            self.movie.full_clean()

    def test_get_review_count_no_reviews(self):
        """Test get_review_count returns 0 when no reviews exist."""
        self.assertEqual(self.movie.get_review_count(), 0)

    def test_get_average_rating_no_reviews(self):
        """Test get_average_rating returns 0.0 when no reviews exist."""
        self.assertEqual(self.movie.get_average_rating(), 0.0)

    def test_get_review_count_with_reviews(self):
        """Test get_review_count returns the correct number of reviews."""
        Review.objects.create(
            movie=self.movie,
            reviewer_name="A",
            review_text="Great film!",
            rating=5,
            review_date=date.today(),
        )
        Review.objects.create(
            movie=self.movie,
            reviewer_name="B",
            review_text="Amazing visuals.",
            rating=4,
            review_date=date.today(),
        )
        self.assertEqual(self.movie.get_review_count(), 2)

    def test_get_average_rating_with_reviews(self):
        """Test get_average_rating calculates the correct average."""
        Review.objects.create(
            movie=self.movie,
            reviewer_name="A",
            review_text="Perfect score.",
            rating=5,
            review_date=date.today(),
        )
        Review.objects.create(
            movie=self.movie,
            reviewer_name="B",
            review_text="Needs work.",
            rating=3,
            review_date=date.today(),
        )
        Review.objects.create(
            movie=self.movie,
            reviewer_name="C",
            review_text="Solid effort.",
            rating=4,
            review_date=date.today(),
        )

        # Average should be (5 + 3 + 4) / 3 = 4.0
        self.assertEqual(self.movie.get_average_rating(), 4.0)

    def test_get_average_rating_with_decimals(self):
        """Test get_average_rating rounds correctly to one decimal place."""
        Review.objects.create(
            movie=self.movie,
            reviewer_name="A",
            review_text="A",
            rating=5,
            review_date=date.today(),
        )
        Review.objects.create(
            movie=self.movie,
            reviewer_name="B",
            review_text="B",
            rating=4,
            review_date=date.today(),
        )

        # Average should be (5 + 4) / 2 = 4.5
        self.assertEqual(self.movie.get_average_rating(), 4.5)


class ReviewModelTest(TestCase):
    """Tests for the Review model, its methods, and validation."""

    def setUp(self):
        """Set up a test Movie and Review instance before each test."""
        self.movie = Movie.objects.create(
            title="Dunkirk",
            description="War film",
            director="Christopher Nolan",
            release_year=2017,
            release_date=date(2017, 7, 21),
        )
        self.review = Review.objects.create(
            movie=self.movie,
            reviewer_name="Jane Doe",
            review_text="A masterpiece of tension and visual storytelling.",
            rating=5,
            review_date=date(2024, 10, 20),
            is_verified=True,
            helpful_count=10,
        )

    def test_review_creation_and_relationship(self):
        """Test that a Review object is created and linked correctly."""
        self.assertEqual(self.review.reviewer_name, "Jane Doe")
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.movie.title, "Dunkirk")
        self.assertTrue(self.review.is_verified)
        self.assertEqual(self.movie.reviews.count(), 1)

    def test_review_str_representation(self):
        """Test the __str__ method of the Review model."""
        expected_str = "Review by Jane Doe for Dunkirk"
        self.assertEqual(str(self.review), expected_str)

    def test_review_clean_validation_success(self):
        """Test Review clean method succeeds with review text >= 10 chars."""
        # No exception should be raised
        self.review.full_clean()

    def test_review_clean_validation_failure(self):
        """Test Review clean method fails when review_text is less than 10 characters."""
        self.review.review_text = "Too short"  # 9 characters
        with self.assertRaisesMessage(
            ValidationError, "Review text must be at least 10 characters long"
        ):
            self.review.full_clean()

    def test_review_rating_validators(self):
        """Test MinValueValidator and MaxValueValidator on rating."""
        # Test MinValueValidator (Rating must be at least 1)
        self.review.rating = 0
        with self.assertRaises(ValidationError):
            self.review.full_clean()

        # Test MaxValueValidator (Rating cannot exceed 5)
        self.review.rating = 6
        with self.assertRaises(ValidationError):
            self.review.full_clean()

    def test_get_star_display(self):
        """Test get_star_display returns the correct star characters."""

        # 5-star rating
        self.review.rating = 5
        self.assertEqual(self.review.get_star_display(), "★★★★★")

        # 3-star rating
        self.review.rating = 3
        self.assertEqual(self.review.get_star_display(), "★★★☆☆")

        # 1-star rating
        self.review.rating = 1
        self.assertEqual(self.review.get_star_display(), "★☆☆☆☆")
