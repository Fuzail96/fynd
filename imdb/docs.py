from .serializers import MovieSerializer


search_movie = {
    "operation_description": "Search Movie",
    "method": "GET",
    "responses": {
        200 : MovieSerializer,
        400 : 'invalid input for lookup.',
        500 : 'Some Execption Occured.'
    }
}

get_movie_by_id = {
    "operation_description": "Get Movie By Id",
    "method": "GET",
    "responses": {
        200 : MovieSerializer,
        400 : 'Movie does not exist.',
        500 : 'Some Execption Occured.'
    }
}

create_movie = {
    "operation_description": "Create Movie",
    "method": "POST",
    "request_body": MovieSerializer,
    "responses": {
        201 : 'Movie created.',
        500 : 'Some Execption Occured.'
    }
}


update_movie = {
    "operation_description": "Update Movie",
    "method": "PUT",
    # "manual_parameters": Movie.id,
    "request_body": MovieSerializer,
    "responses": {
        200 : 'Movie updated.',
        400 : 'Movie does not exist.',
        500 : 'Some Execption Occured.'
    }
}


delete_movie = {
    "operation_description": "Delete Movie",
    "method": "DELETE",
    # "manual_parameters": Movie.id,
    "responses": {
        200 : 'Movie deleted.',
        400 : 'Movie does not exist.',
        500 : 'Some Execption Occured.'
    }
}