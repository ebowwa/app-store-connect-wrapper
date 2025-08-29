use crate::base::BaseAPI;
use crate::error::AppStoreConnectError;
use serde_json::{json, Value};
use std::collections::HashMap;

#[derive(Clone)]
pub struct AppsAPI {
    base: BaseAPI,
}

impl AppsAPI {
    pub fn new(base: BaseAPI) -> Self {
        Self { base }
    }

    pub async fn get_all(&self, limit: Option<u32>) -> Result<Vec<Value>, AppStoreConnectError> {
        self.base.get_all_pages("apps", None, limit).await
    }

    pub async fn get_app(&self, app_id: &str) -> Result<Value, AppStoreConnectError> {
        let response = self.base.get(&format!("apps/{}", app_id), None).await?;
        response
            .get("data")
            .cloned()
            .ok_or_else(|| AppStoreConnectError::Api {
                message: "Invalid response format".to_string(),
            })
    }

    pub async fn get_by_bundle_id(
        &self,
        bundle_id: &str,
    ) -> Result<Option<Value>, AppStoreConnectError> {
        let mut params = HashMap::new();
        params.insert("filter[bundleId]".to_string(), bundle_id.to_string());

        let response = self.base.get("apps", Some(params)).await?;

        if let Some(data) = response.get("data").and_then(|d| d.as_array()) {
            Ok(data.first().cloned())
        } else {
            Ok(None)
        }
    }

    pub async fn update(
        &self,
        app_id: &str,
        attributes: Value,
    ) -> Result<Value, AppStoreConnectError> {
        let data = json!({
            "data": {
                "type": "apps",
                "id": app_id,
                "attributes": attributes
            }
        });

        let response = self.base.patch(&format!("apps/{}", app_id), data).await?;
        response
            .get("data")
            .cloned()
            .ok_or_else(|| AppStoreConnectError::Api {
                message: "Invalid response format".to_string(),
            })
    }

    pub async fn get_app_infos(&self, app_id: &str) -> Result<Vec<Value>, AppStoreConnectError> {
        let response = self
            .base
            .get(&format!("apps/{}/appInfos", app_id), None)
            .await?;

        if let Some(data) = response.get("data").and_then(|d| d.as_array()) {
            Ok(data.clone())
        } else {
            Ok(Vec::new())
        }
    }

    pub async fn get_app_store_versions(
        &self,
        app_id: &str,
    ) -> Result<Vec<Value>, AppStoreConnectError> {
        let response = self
            .base
            .get(&format!("apps/{}/appStoreVersions", app_id), None)
            .await?;

        if let Some(data) = response.get("data").and_then(|d| d.as_array()) {
            Ok(data.clone())
        } else {
            Ok(Vec::new())
        }
    }

    pub async fn get_builds(&self, app_id: &str) -> Result<Vec<Value>, AppStoreConnectError> {
        let response = self
            .base
            .get(&format!("apps/{}/builds", app_id), None)
            .await?;

        if let Some(data) = response.get("data").and_then(|d| d.as_array()) {
            Ok(data.clone())
        } else {
            Ok(Vec::new())
        }
    }
}
