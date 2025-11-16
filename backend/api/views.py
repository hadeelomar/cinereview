"""
Views for handling API requests for movies and reviews.

This module provides RESTful API endpoints with comprehensive error handling,
validation, and proper HTTP status codes following Django best practices.
"""
from typing import Dict, Any
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from datetime import date, datetime
import json
import logging

from .models import Movie, Review

logger = logging.getLogger(__name__)


def movie_to_dict(movie: Movie) -> Dict[str, Any]:
    """
    Convert a Movie model instance to a dictionary for JSON serialization.

    Args:
        movie (Movie): The movie instance to convert

    Returns:
        Dict[str, Any]: Dictionary representation of the movie
    """
    # Explicitly check the type before calling isoformat() for robustness
    if isinstance(movie.release_date, date):
        release_date_str = movie.release_date.isoformat()
    else:
        release_date_str = None

    return {
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "director": movie.director,
        "release_year": movie.release_year,
        "release_date": release_date_str,
        "is_featured": movie.is_featured,
        "poster_url": movie.poster_url,
        "duration_minutes": movie.duration_minutes,
        "average_rating": movie.get_average_rating(),
        "review_count": movie.get_review_count(),
        "created_at": movie.created_at.isoformat() if movie.created_at else None,
        "updated_at": movie.updated_at.isoformat() if movie.updated_at else None,
    }


def review_to_dict(review: Review) -> Dict[str, Any]:
    """
    Convert a Review model instance to a dictionary for JSON serialization.

    Args:
        review (Review): The review instance to convert

    Returns:
        Dict[str, Any]: Dictionary representation of the review
    """
    # Explicitly check the type before calling isoformat() for robustness
    if isinstance(review.review_date, date):
        review_date_str = review.review_date.isoformat()
    else:
        review_date_str = None

    return {
        "id": review.id,
        "movie_id": review.movie_id,
        "reviewer_name": review.reviewer_name,
        "review_text": review.review_text,
        "rating": review.rating,
        "review_date": review_date_str,
        "is_verified": review.is_verified,
        "helpful_count": review.helpful_count,
        "star_display": review.get_star_display(),
        "created_at": review.created_at.isoformat() if review.created_at else None,
        "updated_at": review.updated_at.isoformat() if review.updated_at else None,
    }


@csrf_exempt
@require_http_methods(["GET", "POST"])
def movie_list(request: HttpRequest) -> JsonResponse:
    """
    Handle GET (list all movies) and POST (create new movie) requests.

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        JsonResponse: JSON response with movies data or error message

    GET: Returns list of all movies with their details
    POST: Creates a new movie with provided data
    """
    if request.method == "GET":
        try:
            movies = Movie.objects.all().order_by("id")
            data = [movie_to_dict(m) for m in movies]
            logger.info(f"Successfully fetched {len(data)} movies")
            return JsonResponse({"movies": data}, status=200)
        except Exception as e:
            logger.error(f"Error fetching movies: {str(e)}", exc_info=True)
            return JsonResponse(
                {"error": f"Internal Server Error while fetching movies: {str(e)}"},
                status=500,
            )

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            if not data.get("title"):
                return JsonResponse({"error": "Movie title is required."}, status=400)
            if not data.get("director"):
                return JsonResponse({"error": "Director name is required."}, status=400)

            movie = Movie.objects.create(
                title=data.get("title"),
                description=data.get("description", ""),
                director=data.get("director", ""),
                release_year=data.get("release_year") or datetime.now().year,
                release_date=data.get("release_date") or None,
                is_featured=data.get("is_featured", False),
                poster_url=data.get("poster_url", None),
                duration_minutes=data.get("duration_minutes", None),
            )

            # Run model validation
            movie.full_clean()

            logger.info(f"Successfully created movie: {movie.title}")
            return JsonResponse({"movie": movie_to_dict(movie)}, status=201)

        except json.JSONDecodeError:
            logger.warning("Invalid JSON in request body")
            return JsonResponse({"error": "Invalid JSON in request body."}, status=400)
        except ValidationError as e:
            logger.warning(f"Validation error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Error creating movie: {str(e)}", exc_info=True)
            return JsonResponse(
                {"error": f"Failed to create movie: {str(e)}"}, status=400
            )


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def movie_detail(request: HttpRequest, movie_id: int) -> JsonResponse:
    """
    Handle GET, PUT, DELETE operations for a specific movie.

    Args:
        request (HttpRequest): The HTTP request object
        movie_id (int): The ID of the movie to operate on

    Returns:
        JsonResponse: JSON response with movie data or error message

    GET: Returns details of a specific movie
    PUT: Updates an existing movie
    DELETE: Deletes a movie and all its reviews
    """
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        logger.warning(f"Movie not found: {movie_id}")
        return JsonResponse({"error": "Movie not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({"movie": movie_to_dict(movie)}, status=200)

    if request.method == "PUT":
        try:
            data = json.loads(request.body.decode("utf-8"))

            # Update fields only if they are present in the request data
            movie.title = data.get("title", movie.title)
            movie.description = data.get("description", movie.description)
            movie.director = data.get("director", movie.director)
            movie.release_year = data.get("release_year", movie.release_year)
            movie.release_date = data.get("release_date") or None
            movie.poster_url = data.get("poster_url", movie.poster_url)
            movie.duration_minutes = data.get(
                "duration_minutes", movie.duration_minutes
            )

            # Handle boolean explicitly
            if "is_featured" in data:
                movie.is_featured = data["is_featured"]

            # Run model validation
            movie.full_clean()
            movie.save()

            logger.info(f"Successfully updated movie: {movie.title}")
            return JsonResponse({"movie": movie_to_dict(movie)}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body."}, status=400)
        except ValidationError as e:
            logger.warning(f"Validation error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Error updating movie: {str(e)}", exc_info=True)
            return JsonResponse(
                {"error": f"Failed to update movie: {str(e)}"}, status=400
            )

    if request.method == "DELETE":
        movie_title = movie.title
        movie.delete()
        logger.info(f"Successfully deleted movie: {movie_title}")
        return JsonResponse({"message": "Movie deleted successfully"}, status=204)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def review_list(request: HttpRequest) -> JsonResponse:
    """
    Handle GET (list all reviews) and POST (create new review) requests.

    Args:
        request (HttpRequest): The HTTP request object

    Returns:
        JsonResponse: JSON response with reviews data or error message

    GET: Returns list of all reviews, optionally filtered by movie_id
    POST: Creates a new review for a movie
    """
    if request.method == "GET":
        try:
            movie_id = request.GET.get("movie_id")
            if movie_id:
                reviews = Review.objects.filter(movie_id=movie_id).order_by(
                    "-review_date"
                )
            else:
                reviews = Review.objects.all().order_by("id")

            data = [review_to_dict(r) for r in reviews]
            logger.info(f"Successfully fetched {len(data)} reviews")
            return JsonResponse({"reviews": data}, status=200)
        except Exception as e:
            logger.error(f"Error fetching reviews: {str(e)}", exc_info=True)
            return JsonResponse(
                {"error": "Internal Server Error while fetching reviews"}, status=500
            )

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            # Validation for required fields
            if not data.get("reviewer_name") or not data.get("movie_id"):
                return JsonResponse(
                    {"error": "Reviewer name and movie ID are required."}, status=400
                )

            movie_id = data.get("movie_id")
            try:
                movie = Movie.objects.get(pk=movie_id)
            except Movie.DoesNotExist:
                return JsonResponse(
                    {"error": "Movie not found for this review."}, status=404
                )

            review = Review.objects.create(
                movie=movie,
                reviewer_name=data.get("reviewer_name"),
                review_text=data.get("review_text", ""),
                rating=data.get("rating") or 5,
                review_date=data.get("review_date") or date.today(),
                is_verified=data.get("is_verified", False),
            )

            # Run model validation
            review.full_clean()

            logger.info(f"Successfully created review for movie: {movie.title}")
            return JsonResponse({"review": review_to_dict(review)}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body."}, status=400)
        except ValidationError as e:
            logger.warning(f"Validation error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Error creating review: {str(e)}", exc_info=True)
            return JsonResponse(
                {"error": f"Failed to create review: {str(e)}"}, status=400
            )


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def review_detail(request: HttpRequest, review_id: int) -> JsonResponse:
    """
    Handle GET, PUT, DELETE operations for a specific review.

    Args:
        request (HttpRequest): The HTTP request object
        review_id (int): The ID of the review to operate on

    Returns:
        JsonResponse: JSON response with review data or error message

    GET: Returns details of a specific review
    PUT: Updates an existing review
    DELETE: Deletes a review
    """
    try:
        review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
        logger.warning(f"Review not found: {review_id}")
        return JsonResponse({"error": "Review not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({"review": review_to_dict(review)}, status=200)

    if request.method == "PUT":
        try:
            data = json.loads(request.body.decode("utf-8"))

            # Update fields
            review.reviewer_name = data.get("reviewer_name", review.reviewer_name)
            review.review_text = data.get("review_text", review.review_text)
            review.rating = (
                data.get("rating") if data.get("rating") is not None else review.rating
            )
            review.review_date = data.get("review_date") or None
            review.is_verified = data.get("is_verified", review.is_verified)
            review.helpful_count = data.get("helpful_count", review.helpful_count)

            # If movie_id is being updated
            if "movie_id" in data:
                movie_id = data["movie_id"]
                try:
                    review.movie = Movie.objects.get(pk=movie_id)
                except Movie.DoesNotExist:
                    return JsonResponse({"error": "New movie not found"}, status=404)

            # Run model validation
            review.full_clean()
            review.save()

            logger.info(f"Successfully updated review ID: {review_id}")
            return JsonResponse({"review": review_to_dict(review)}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body."}, status=400)
        except ValidationError as e:
            logger.warning(f"Validation error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Error updating review: {str(e)}", exc_info=True)
            return JsonResponse(
                {"error": f"Failed to update review: {str(e)}"}, status=400
            )

    if request.method == "DELETE":
        review.delete()
        logger.info(f"Successfully deleted review ID: {review_id}")
        return JsonResponse({"message": "Review deleted successfully"}, status=204)
