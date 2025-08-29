use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppStoreConnectError {
    #[error("Authentication failed: {0}")]
    Authentication(#[from] AuthenticationError),

    #[error("Rate limit exceeded: {0}")]
    RateLimit(#[from] RateLimitError),

    #[error("Resource not found: {0}")]
    NotFound(#[from] NotFoundError),

    #[error("Validation failed: {0}")]
    Validation(#[from] ValidationError),

    #[error("Conflict occurred: {0}")]
    Conflict(#[from] ConflictError),

    #[error("HTTP request failed: {0}")]
    Http(#[from] reqwest::Error),

    #[error("JSON parsing failed: {0}")]
    Json(#[from] serde_json::Error),

    #[error("Environment variable error: {0}")]
    Env(#[from] std::env::VarError),

    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("JWT error: {0}")]
    Jwt(#[from] jsonwebtoken::errors::Error),

    #[error("API error: {message}")]
    Api { message: String },

    #[error("Unknown error: {0}")]
    Unknown(String),
}

#[derive(Error, Debug)]
#[error("Authentication failed: {message}")]
pub struct AuthenticationError {
    pub message: String,
}

impl AuthenticationError {
    pub fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
        }
    }
}

#[derive(Error, Debug)]
#[error("Rate limit exceeded: {message}")]
pub struct RateLimitError {
    pub message: String,
}

impl RateLimitError {
    pub fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
        }
    }
}

#[derive(Error, Debug)]
#[error("Resource not found: {message}")]
pub struct NotFoundError {
    pub message: String,
}

impl NotFoundError {
    pub fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
        }
    }
}

#[derive(Error, Debug)]
#[error("Validation failed: {message}")]
pub struct ValidationError {
    pub message: String,
}

impl ValidationError {
    pub fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
        }
    }
}

#[derive(Error, Debug)]
#[error("Conflict occurred: {message}")]
pub struct ConflictError {
    pub message: String,
}

impl ConflictError {
    pub fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
        }
    }
}
