use crate::base::BaseAPI;
use crate::error::AppStoreConnectError;
use serde_json::{json, Value};
use std::collections::HashMap;

#[derive(Clone)]
pub struct LocalizationsAPI {
    base: BaseAPI,
}

impl LocalizationsAPI {
    pub fn new(base: BaseAPI) -> Self {
        Self { base }
    }

    pub async fn get_all(&self, app_info_id: &str) -> Result<Vec<Value>, AppStoreConnectError> {
        let response = self
            .base
            .get(
                &format!("appInfos/{}/appInfoLocalizations", app_info_id),
                None,
            )
            .await?;

        if let Some(data) = response.get("data").and_then(|d| d.as_array()) {
            Ok(data.clone())
        } else {
            Ok(Vec::new())
        }
    }

    pub async fn get(&self, localization_id: &str) -> Result<Value, AppStoreConnectError> {
        let response = self
            .base
            .get(&format!("appInfoLocalizations/{}", localization_id), None)
            .await?;

        response
            .get("data")
            .cloned()
            .ok_or_else(|| AppStoreConnectError::Api {
                message: "Invalid response format".to_string(),
            })
    }

    pub async fn create(
        &self,
        app_info_id: &str,
        locale: &str,
        name: Option<&str>,
        subtitle: Option<&str>,
        privacy_policy_url: Option<&str>,
        privacy_policy_text: Option<&str>,
    ) -> Result<Value, AppStoreConnectError> {
        let mut attributes = json!({ "locale": locale });

        if let Some(name) = name {
            attributes["name"] = json!(name);
        }
        if let Some(subtitle) = subtitle {
            attributes["subtitle"] = json!(subtitle);
        }
        if let Some(url) = privacy_policy_url {
            attributes["privacyPolicyUrl"] = json!(url);
        }
        if let Some(text) = privacy_policy_text {
            attributes["privacyPolicyText"] = json!(text);
        }

        let data = json!({
            "data": {
                "type": "appInfoLocalizations",
                "attributes": attributes,
                "relationships": {
                    "appInfo": {
                        "data": {
                            "type": "appInfos",
                            "id": app_info_id
                        }
                    }
                }
            }
        });

        let response = self.base.post("appInfoLocalizations", data).await?;
        response
            .get("data")
            .cloned()
            .ok_or_else(|| AppStoreConnectError::Api {
                message: "Invalid response format".to_string(),
            })
    }

    pub async fn update(
        &self,
        localization_id: &str,
        name: Option<&str>,
        subtitle: Option<&str>,
        privacy_policy_url: Option<&str>,
        privacy_policy_text: Option<&str>,
    ) -> Result<Value, AppStoreConnectError> {
        let mut attributes = json!({});

        if let Some(name) = name {
            attributes["name"] = json!(name);
        }
        if let Some(subtitle) = subtitle {
            attributes["subtitle"] = json!(subtitle);
        }
        if let Some(url) = privacy_policy_url {
            attributes["privacyPolicyUrl"] = json!(url);
        }
        if let Some(text) = privacy_policy_text {
            attributes["privacyPolicyText"] = json!(text);
        }

        let data = json!({
            "data": {
                "type": "appInfoLocalizations",
                "id": localization_id,
                "attributes": attributes
            }
        });

        let response = self
            .base
            .patch(&format!("appInfoLocalizations/{}", localization_id), data)
            .await?;

        response
            .get("data")
            .cloned()
            .ok_or_else(|| AppStoreConnectError::Api {
                message: "Invalid response format".to_string(),
            })
    }

    pub async fn delete(&self, localization_id: &str) -> Result<(), AppStoreConnectError> {
        self.base
            .delete(&format!("appInfoLocalizations/{}", localization_id))
            .await?;
        Ok(())
    }

    pub async fn bulk_update(
        &self,
        app_info_id: &str,
        localizations: HashMap<String, Value>,
    ) -> Result<HashMap<String, Value>, AppStoreConnectError> {
        let existing = self.get_all(app_info_id).await?;
        let mut existing_by_locale = HashMap::new();

        for loc in existing {
            if let (Some(locale), Some(id)) = (
                loc.get("attributes")
                    .and_then(|a| a.get("locale"))
                    .and_then(|l| l.as_str()),
                loc.get("id").and_then(|i| i.as_str()),
            ) {
                existing_by_locale.insert(locale.to_string(), (id.to_string(), loc));
            }
        }

        let mut results = HashMap::new();

        for (locale, attributes) in localizations {
            let result = if let Some((localization_id, _)) = existing_by_locale.get(&locale) {
                match self.update_from_value(localization_id, &attributes).await {
                    Ok(data) => json!({
                        "success": true,
                        "action": "updated",
                        "data": data
                    }),
                    Err(e) => json!({
                        "success": false,
                        "error": e.to_string()
                    }),
                }
            } else {
                match self
                    .create_from_value(app_info_id, &locale, &attributes)
                    .await
                {
                    Ok(data) => json!({
                        "success": true,
                        "action": "created",
                        "data": data
                    }),
                    Err(e) => json!({
                        "success": false,
                        "error": e.to_string()
                    }),
                }
            };

            results.insert(locale, result);
        }

        Ok(results)
    }

    async fn update_from_value(
        &self,
        localization_id: &str,
        attributes: &Value,
    ) -> Result<Value, AppStoreConnectError> {
        let name = attributes.get("name").and_then(|n| n.as_str());
        let subtitle = attributes.get("subtitle").and_then(|s| s.as_str());
        let privacy_policy_url = attributes.get("privacyPolicyUrl").and_then(|u| u.as_str());
        let privacy_policy_text = attributes.get("privacyPolicyText").and_then(|t| t.as_str());

        self.update(
            localization_id,
            name,
            subtitle,
            privacy_policy_url,
            privacy_policy_text,
        )
        .await
    }

    async fn create_from_value(
        &self,
        app_info_id: &str,
        locale: &str,
        attributes: &Value,
    ) -> Result<Value, AppStoreConnectError> {
        let name = attributes.get("name").and_then(|n| n.as_str());
        let subtitle = attributes.get("subtitle").and_then(|s| s.as_str());
        let privacy_policy_url = attributes.get("privacyPolicyUrl").and_then(|u| u.as_str());
        let privacy_policy_text = attributes.get("privacyPolicyText").and_then(|t| t.as_str());

        self.create(
            app_info_id,
            locale,
            name,
            subtitle,
            privacy_policy_url,
            privacy_policy_text,
        )
        .await
    }
}
