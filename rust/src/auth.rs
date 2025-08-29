use crate::error::{AppStoreConnectError, AuthenticationError};
use chrono::{Duration, Utc};
use jsonwebtoken::{encode, Algorithm, EncodingKey, Header};
use serde::{Deserialize, Serialize};
use std::path::Path;
use std::sync::Arc;
use tokio::sync::RwLock;

#[derive(Debug, Serialize, Deserialize)]
struct Claims {
    iss: String,
    iat: i64,
    exp: i64,
    aud: String,
}

#[derive(Clone)]
pub struct Auth {
    key_id: String,
    issuer_id: String,
    private_key: EncodingKey,
    token_cache: Arc<RwLock<Option<(String, i64)>>>,
}

impl Auth {
    pub async fn new(
        key_id: impl Into<String>,
        issuer_id: impl Into<String>,
        private_key_path: impl AsRef<Path>,
    ) -> Result<Self, AppStoreConnectError> {
        let key_id = key_id.into();
        let issuer_id = issuer_id.into();
        let private_key_path = private_key_path.as_ref();

        if !private_key_path.exists() {
            return Err(AppStoreConnectError::Authentication(
                AuthenticationError::new(format!(
                    "Private key file not found: {}",
                    private_key_path.display()
                )),
            ));
        }

        let private_key_content =
            tokio::fs::read_to_string(private_key_path)
                .await
                .map_err(|e| {
                    AppStoreConnectError::Authentication(AuthenticationError::new(format!(
                        "Failed to read private key file: {}",
                        e
                    )))
                })?;

        let private_key =
            EncodingKey::from_ec_pem(private_key_content.as_bytes()).map_err(|e| {
                AppStoreConnectError::Authentication(AuthenticationError::new(format!(
                    "Failed to parse private key: {}",
                    e
                )))
            })?;

        Ok(Self {
            key_id,
            issuer_id,
            private_key,
            token_cache: Arc::new(RwLock::new(None)),
        })
    }

    pub async fn get_token(&self) -> Result<String, AppStoreConnectError> {
        let now = Utc::now().timestamp();

        {
            let cache = self.token_cache.read().await;
            if let Some((token, expiry)) = cache.as_ref() {
                if now < (expiry - 60) {
                    return Ok(token.clone());
                }
            }
        }

        let token = self.generate_token().await?;

        {
            let mut cache = self.token_cache.write().await;
            let expiry = now + (20 * 60);
            *cache = Some((token.clone(), expiry));
        }

        Ok(token)
    }

    async fn generate_token(&self) -> Result<String, AppStoreConnectError> {
        let now = Utc::now();
        let expiry = now + Duration::minutes(20);

        let claims = Claims {
            iss: self.issuer_id.clone(),
            iat: now.timestamp(),
            exp: expiry.timestamp(),
            aud: "appstoreconnect-v1".to_string(),
        };

        let mut header = Header::new(Algorithm::ES256);
        header.kid = Some(self.key_id.clone());
        header.typ = Some("JWT".to_string());

        let token = encode(&header, &claims, &self.private_key).map_err(|e| {
            AppStoreConnectError::Authentication(AuthenticationError::new(format!(
                "Failed to generate JWT token: {}",
                e
            )))
        })?;

        Ok(token)
    }

    pub async fn headers(&self) -> Result<reqwest::header::HeaderMap, AppStoreConnectError> {
        let token = self.get_token().await?;
        let mut headers = reqwest::header::HeaderMap::new();

        headers.insert(
            reqwest::header::AUTHORIZATION,
            reqwest::header::HeaderValue::from_str(&format!("Bearer {}", token))
                .map_err(|e| AppStoreConnectError::Unknown(e.to_string()))?,
        );

        headers.insert(
            reqwest::header::CONTENT_TYPE,
            reqwest::header::HeaderValue::from_static("application/json"),
        );

        Ok(headers)
    }

    pub async fn is_token_valid(&self) -> bool {
        let cache = self.token_cache.read().await;
        if let Some((_, expiry)) = cache.as_ref() {
            let now = Utc::now().timestamp();
            now < *expiry
        } else {
            false
        }
    }

    pub async fn refresh_token(&self) -> Result<(), AppStoreConnectError> {
        let token = self.generate_token().await?;
        let now = Utc::now().timestamp();
        let expiry = now + (20 * 60);

        let mut cache = self.token_cache.write().await;
        *cache = Some((token, expiry));

        Ok(())
    }
}
