# Model Service
The service is available as a container image that is hosted on the Github Container Registry:
```
ghcr.io/remla2025-team10/model-service:latest
```

The service is only used internally by the `app-service` repository when making POST requests for sentiment prediction.

The service also includes a small section where it loads an example secret provided by Docker, to illustrate the ability to load sensitive information safely. This could be useful if in the future the service was made more complex and required access to some sensitive information.

## Example Usage
The service provides the `POST /predict` endpoint, which accepts a review and returns the model prediction.

### Request Body:
```
{
    "review": "The food was amazing!"
}
```

### Response:
```
{
    "prediction": 1
}
```
