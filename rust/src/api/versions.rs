use crate::base::BaseAPI;
use crate::error::AppStoreConnectError;
use serde_json::{json, Value};

#[derive(Clone)]
pub struct VersionsAPI {
    base: BaseAPI,
}

impl VersionsAPI {
    pub fn new(base: BaseAPI) -> Self {
        Self { base }
    }

    pub async fn get_all(&self, app_id: &str) -> Result<Vec<Value>, AppStoreConnectError> {
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

    pub async fn get(&self, version_id: &str) -> Result<Value, AppStoreConnectError> {
        let response = self
            .base
            .get(&format!("appStoreVersions/{}", version_id), None)
            .await?;

        response
            .get("data")
            .cloned()
            .ok_or_else(|| AppStoreConnectError::Api {
                message: "Invalid response format".to_string(),
            })
    }

    pub async fn get_current(&self, app_id: &str) -> Result<Option<Value>, AppStoreConnectError> {
        let versions = self.get_all(app_id).await?;

        let priority_states = [
            "READY_FOR_SALE",
            "PROCESSING_FOR_APP_STORE",
            "PENDING_DEVELOPER_RELEASE",
            "IN_REVIEW",
            "WAITING_FOR_REVIEW",
            "PREPARE_FOR_SUBMISSION",
            "DEVELOPER_REJECTED",
        ];

        for state in &priority_states {
            for version in &versions {
                if let Some(app_store_state) = version
                    .get("attributes")
                    .and_then(|a| a.get("appStoreState"))
                    .and_then(|s| s.as_str())
                {
                    if app_store_state == *state {
                        return Ok(Some(version.clone()));
                    }
                }
            }
        }

        Ok(versions.first().cloned())
    }

    pub async fn create(
        &self,
        app_id: &str,
        version_string: &str,
        platform: Option<&str>,
        copyright: Option<&str>,
        release_type: Option<&str>,
    ) -> Result<Value, AppStoreConnectError> {
        let mut attributes = json!({
            "versionString": version_string,
            "platform": platform.unwrap_or("IOS")
        });

        if let Some(copyright) = copyright {
            attributes["copyright"] = json!(copyright);
        }
        if let Some(release_type) = release_type {
            attributes["releaseType"] = json!(release_type);
        }

        let data = json!({
            "data": {
                "type": "appStoreVersions",
                "attributes": attributes,
                "relationships": {
                    "app": {
                        "data": {
                            "type": "apps",
                            "id": app_id
                        }
                    }
                }
            }
        });

        let response = self.base.post("appStoreVersions", data).await?;
        response
            .get("data")
            .cloned()
            .ok_or_else(|| AppStoreConnectError::Api {
                message: "Invalid response format".to_string(),
            })
    }

    pub async fn update(
        &self,
        version_id: &str,
        version_string: Option<&str>,
        copyright: Option<&str>,
        release_type: Option<&str>,
        earliest_release_date: Option<&str>,
        uses_idfa: Option<bool>,
        is_watch_only: Option<bool>,
        downloadable: Option<bool>,
    ) -> Result<Value, AppStoreConnectError> {
        let mut attributes = json!({});

        if let Some(version_string) = version_string {
            attributes["versionString"] = json!(version_string);
        }
        if let Some(copyright) = copyright {
            attributes["copyright"] = json!(copyright);
        }
        if let Some(release_type) = release_type {
            attributes["releaseType"] = json!(release_type);
        }
        if let Some(earliest_release_date) = earliest_release_date {
            attributes["earliestReleaseDate"] = json!(earliest_release_date);
        }
        if let Some(uses_idfa) = uses_idfa {
            attributes["usesIdfa"] = json!(uses_idfa);
        }
        if let Some(is_watch_only) = is_watch_only {
            attributes["isWatchOnly"] = json!(is_watch_only);
        }
        if let Some(downloadable) = downloadable {
            attributes["downloadable"] = json!(downloadable);
        }

        let data = json!({
            "data": {
                "type": "appStoreVersions",
                "id": version_id,
                "attributes": attributes
            }
        });

        let response = self
            .base
            .patch(&format!("appStoreVersions/{}", version_id), data)
            .await?;

        response
            .get("data")
            .cloned()
            .ok_or_else(|| AppStoreConnectError::Api {
                message: "Invalid response format".to_string(),
            })
    }

    pub async fn submit_for_review(&self, version_id: &str) -> Result<Value, AppStoreConnectError> {
        let data = json!({
            "data": {
                "type": "appStoreVersionSubmissions",
                "relationships": {
                    "appStoreVersion": {
                        "data": {
                            "type": "appStoreVersions",
                            "id": version_id
                        }
                    }
                }
            }
        });

        let response = self.base.post("appStoreVersionSubmissions", data).await?;
        response
            .get("data")
            .cloned()
            .ok_or_else(|| AppStoreConnectError::Api {
                message: "Invalid response format".to_string(),
            })
    }

    pub async fn get_build(&self, version_id: &str) -> Result<Option<Value>, AppStoreConnectError> {
        let response = self
            .base
            .get(&format!("appStoreVersions/{}/build", version_id), None)
            .await?;

        Ok(response.get("data").cloned())
    }

    pub async fn set_build(
        &self,
        version_id: &str,
        build_id: &str,
    ) -> Result<Value, AppStoreConnectError> {
        let data = json!({
            "data": {
                "type": "builds",
                "id": build_id
            }
        });

        self.base
            .patch(
                &format!("appStoreVersions/{}/relationships/build", version_id),
                data,
            )
            .await
    }
}
