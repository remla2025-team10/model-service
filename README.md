# Model Service
The service is available as a container image that is hosted on the Github Container Registry:
```
ghcr.io/remla2025-team10/model-service:v0.0.4
```

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