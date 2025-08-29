use crate::api::{
    apps::AppsAPI, categories::CategoriesAPI, localizations::LocalizationsAPI, media::MediaAPI,
    versions::VersionsAPI,
};
use crate::auth::Auth;
use crate::base::BaseAPI;
use crate::error::AppStoreConnectError;
use serde_json::Value;
use std::collections::HashMap;
use std::env;

#[derive(Clone)]
pub struct Client {
    base: BaseAPI,
    apps_api: AppsAPI,
    localizations_api: LocalizationsAPI,
    versions_api: VersionsAPI,
    media_api: MediaAPI,
    categories_api: CategoriesAPI,
}

impl Client {
    pub async fn new(
        key_id: impl Into<String>,
        issuer_id: impl Into<String>,
        private_key_path: impl AsRef<std::path::Path>,
    ) -> Result<Self, AppStoreConnectError> {
        let auth = Auth::new(key_id, issuer_id, private_key_path).await?;
        let base = BaseAPI::new(auth)?;

        Ok(Self {
            apps_api: AppsAPI::new(base.clone()),
            localizations_api: LocalizationsAPI::new(base.clone()),
            versions_api: VersionsAPI::new(base.clone()),
            media_api: MediaAPI::new(base.clone()),
            categories_api: CategoriesAPI::new(base.clone()),
            base,
        })
    }

    pub async fn from_env() -> Result<Self, AppStoreConnectError> {
        Self::from_env_with_prefix("ASC").await
    }

    pub async fn from_env_with_prefix(prefix: &str) -> Result<Self, AppStoreConnectError> {
        let key_id = env::var(format!("{}_KEY_ID", prefix))?;
        let issuer_id = env::var(format!("{}_ISSUER_ID", prefix))?;
        let private_key_path = env::var(format!("{}_PRIVATE_KEY_PATH", prefix))?;

        Self::new(key_id, issuer_id, private_key_path).await
    }

    pub fn apps(&self) -> &AppsAPI {
        &self.apps_api
    }

    pub fn localizations(&self) -> &LocalizationsAPI {
        &self.localizations_api
    }

    pub fn versions(&self) -> &VersionsAPI {
        &self.versions_api
    }

    pub fn media(&self) -> &MediaAPI {
        &self.media_api
    }

    pub fn categories(&self) -> &CategoriesAPI {
        &self.categories_api
    }

    pub async fn get_app_by_bundle_id(
        &self,
        bundle_id: &str,
    ) -> Result<Option<Value>, AppStoreConnectError> {
        self.apps().get_by_bundle_id(bundle_id).await
    }

    pub async fn update_app_localizations(
        &self,
        app_id: &str,
        localizations: HashMap<String, Value>,
    ) -> Result<HashMap<String, Value>, AppStoreConnectError> {
        let app_infos = self.apps().get_app_infos(app_id).await?;

        if app_infos.is_empty() {
            return Err(AppStoreConnectError::Api {
                message: format!("No app info found for app {}", app_id),
            });
        }

        let app_info_id = app_infos[0]
            .get("id")
            .and_then(|id| id.as_str())
            .ok_or_else(|| AppStoreConnectError::Api {
                message: "Invalid app info ID".to_string(),
            })?;

        self.localizations()
            .bulk_update(app_info_id, localizations)
            .await
    }

    pub async fn get_current_version(
        &self,
        app_id: &str,
    ) -> Result<Option<Value>, AppStoreConnectError> {
        self.versions().get_current(app_id).await
    }

    pub async fn create_new_version(
        &self,
        app_id: &str,
        version_string: &str,
        platform: Option<&str>,
        copyright: Option<&str>,
        release_type: Option<&str>,
    ) -> Result<Value, AppStoreConnectError> {
        self.versions()
            .create(app_id, version_string, platform, copyright, release_type)
            .await
    }

    pub async fn submit_for_review(&self, version_id: &str) -> Result<Value, AppStoreConnectError> {
        self.versions().submit_for_review(version_id).await
    }
}
