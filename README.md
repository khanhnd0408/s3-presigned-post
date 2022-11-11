# s3-presigned-post
## Simple S3 Post Upload with presigned URL.

For testing purpose, add S3 CORS following
/!\ This for testing only, don't do this in production.
```
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "PUT",
            "POST",
            "DELETE",
            "HEAD",
            "GET"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": [
            "ETag"
        ]
    }
]
```