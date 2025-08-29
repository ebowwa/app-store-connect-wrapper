use crate::auth::Auth;
use crate::error::{
    AppStoreConnectError, ConflictError, NotFoundError, RateLimitError, ValidationError,
};
use reqwest::{Method, Response, StatusCode};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;
use url::Url;

const BASE_URL: &str = "https://api.appstoreconnect.apple.com/v1/";

#[derive(Clone)]
pub struct BaseAPI {
    auth: Auth,
    client: reqwest::Client,
    base_url: Url,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ApiResponse<T> {
    pub data: T,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub included: Option<Vec<Value>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub links: Option<HashMap<String, String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub meta: Option<Value>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ErrorResponse {
    pub errors: Vec<ApiError>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ApiError {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub status: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub code: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub title: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub detail: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub source: Option<Value>,
}

impl BaseAPI {
    pub fn new(auth: Auth) -> Result<Self, AppStoreConnectError> {
        let client = reqwest::Client::new();
        let base_url = Url::parse(BASE_URL)
            .map_err(|e| AppStoreConnectError::Unknown(format!("Invalid base URL: {}", e)))?;

        Ok(Self {
            auth,
            client,
            base_url,
        })
    }

    pub async fn request(
        &self,
        method: Method,
        endpoint: &str,
        data: Option<Value>,
        params: Option<HashMap<String, String>>,
    ) -> Result<Value, AppStoreConnectError> {
        let url = self
            .base_url
            .join(endpoint)
            .map_err(|e| AppStoreConnectError::Unknown(format!("Invalid endpoint: {}", e)))?;

        let headers = self.auth.headers().await?;
        let mut request = self.client.request(method, url).headers(headers);

        if let Some(params) = params {
            request = request.query(&params);
        }

        if let Some(data) = data {
            request = request.json(&data);
        }

        let response = request.send().await?;
        self.handle_response(response).await
    }

    async fn handle_response(&self, response: Response) -> Result<Value, AppStoreConnectError> {
        let status = response.status();
        let response_text = response.text().await?;

        match status {
            StatusCode::OK | StatusCode::CREATED => {
                if response_text.is_empty() {
                    Ok(Value::Object(serde_json::Map::new()))
                } else {
                    serde_json::from_str(&response_text).map_err(AppStoreConnectError::Json)
                }
            }
            StatusCode::NO_CONTENT => Ok(Value::Object(serde_json::Map::new())),
            StatusCode::UNAUTHORIZED => Err(AppStoreConnectError::Api {
                message: "Authentication failed. Check your credentials.".to_string(),
            }),
            StatusCode::FORBIDDEN => Err(AppStoreConnectError::Api {
                message: "Forbidden. Check your permissions.".to_string(),
            }),
            StatusCode::NOT_FOUND => {
                let error_msg = self.extract_error_message(&response_text);
                Err(AppStoreConnectError::NotFound(NotFoundError::new(
                    error_msg.unwrap_or_else(|| "Resource not found".to_string()),
                )))
            }
            StatusCode::CONFLICT => {
                let error_msg = self.extract_error_message(&response_text);
                Err(AppStoreConnectError::Conflict(ConflictError::new(
                    error_msg.unwrap_or_else(|| "Conflict occurred".to_string()),
                )))
            }
            StatusCode::UNPROCESSABLE_ENTITY => {
                let error_msg = self.extract_error_message(&response_text);
                Err(AppStoreConnectError::Validation(ValidationError::new(
                    error_msg.unwrap_or_else(|| "Validation failed".to_string()),
                )))
            }
            StatusCode::TOO_MANY_REQUESTS => {
                Err(AppStoreConnectError::RateLimit(RateLimitError::new(
                    "API rate limit exceeded. Please wait before retrying.".to_string(),
                )))
            }
            _ => {
                let error_msg = self.extract_error_message(&response_text);
                Err(AppStoreConnectError::Api {
                    message: format!(
                        "API request failed with status {}: {}",
                        status,
                        error_msg.unwrap_or_else(|| "Unknown error".to_string())
                    ),
                })
            }
        }
    }

    fn extract_error_message(&self, response_text: &str) -> Option<String> {
        if let Ok(error_response) = serde_json::from_str::<ErrorResponse>(response_text) {
            if let Some(error) = error_response.errors.first() {
                return error
                    .title
                    .clone()
                    .or_else(|| error.detail.clone())
                    .or_else(|| error.code.clone());
            }
        }
        None
    }

    pub async fn get(
        &self,
        endpoint: &str,
        params: Option<HashMap<String, String>>,
    ) -> Result<Value, AppStoreConnectError> {
        self.request(Method::GET, endpoint, None, params).await
    }

    pub async fn post(&self, endpoint: &str, data: Value) -> Result<Value, AppStoreConnectError> {
        self.request(Method::POST, endpoint, Some(data), None).await
    }

    pub async fn patch(&self, endpoint: &str, data: Value) -> Result<Value, AppStoreConnectError> {
        self.request(Method::PATCH, endpoint, Some(data), None)
            .await
    }

    pub async fn delete(&self, endpoint: &str) -> Result<Value, AppStoreConnectError> {
        self.request(Method::DELETE, endpoint, None, None).await
    }

    pub async fn get_all_pages(
        &self,
        endpoint: &str,
        params: Option<HashMap<String, String>>,
        limit: Option<u32>,
    ) -> Result<Vec<Value>, AppStoreConnectError> {
        let mut all_results = Vec::new();
        let mut current_params = params.unwrap_or_default();

        if let Some(limit) = limit {
            current_params.insert("limit".to_string(), limit.min(200).to_string());
        } else {
            current_params.insert("limit".to_string(), "200".to_string());
        }

        let mut current_endpoint = endpoint.to_string();

        loop {
            let response = self
                .get(&current_endpoint, Some(current_params.clone()))
                .await?;

            if let Some(data) = response.get("data").and_then(|d| d.as_array()) {
                all_results.extend(data.iter().cloned());
            }

            if let Some(links) = response.get("links").and_then(|l| l.as_object()) {
                if let Some(next_url) = links.get("next").and_then(|n| n.as_str()) {
                    if let Ok(url) = Url::parse(next_url) {
                        current_endpoint = url.path().trim_start_matches("/v1/").to_string();
                        current_params.clear();
                        for (key, value) in url.query_pairs() {
                            current_params.insert(key.to_string(), value.to_string());
                        }
                    } else {
                        break;
                    }
                } else {
                    break;
                }
            } else {
                break;
            }
        }

        Ok(all_results)
    }
}
