pub mod auth;
pub mod base;
pub mod client;
pub mod error;
pub mod api {
    pub mod apps;
    pub mod categories;
    pub mod localizations;
    pub mod media;
    pub mod versions;
}

pub use auth::Auth;
pub use client::Client;
pub use error::{
    AppStoreConnectError, AuthenticationError, ConflictError, NotFoundError, RateLimitError,
    ValidationError,
};

pub type Result<T> = std::result::Result<T, AppStoreConnectError>;

#[cfg(test)]
mod tests {
    use super::*;
    use std::env;

    #[tokio::test]
    async fn test_auth_creation() {
        let temp_key = std::env::temp_dir().join("test_key.p8");
        std::fs::write(&temp_key, "-----BEGIN PRIVATE KEY-----\nMIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQg\n-----END PRIVATE KEY-----").unwrap();

        let result = Auth::new("test_key_id", "test_issuer_id", &temp_key).await;
        std::fs::remove_file(&temp_key).ok();

        assert!(result.is_err());
    }

    #[test]
    fn test_error_types() {
        let auth_error = AuthenticationError::new("test auth error");
        assert_eq!(auth_error.message, "test auth error");

        let rate_limit_error = RateLimitError::new("test rate limit");
        assert_eq!(rate_limit_error.message, "test rate limit");

        let not_found_error = NotFoundError::new("test not found");
        assert_eq!(not_found_error.message, "test not found");

        let validation_error = ValidationError::new("test validation");
        assert_eq!(validation_error.message, "test validation");

        let conflict_error = ConflictError::new("test conflict");
        assert_eq!(conflict_error.message, "test conflict");
    }

    #[tokio::test]
    async fn test_client_from_env_missing_vars() {
        env::remove_var("APP_STORE_CONNECT_KEY_ID");
        env::remove_var("APP_STORE_CONNECT_ISSUER_ID");
        env::remove_var("APP_STORE_CONNECT_PRIVATE_KEY_PATH");

        let result = Client::from_env().await;
        assert!(result.is_err());
    }
}
