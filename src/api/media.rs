use crate::base::BaseAPI;
use crate::error::AppStoreConnectError;
use serde_json::{json, Value};
use std::collections::HashMap;

#[derive(Clone)]
pub struct MediaAPI {
    base: BaseAPI,
}

impl MediaAPI {
    pub fn new(base: BaseAPI) -> Self {
        Self { base }
    }

    pub async fn get_screenshots(
        &self,
        localization_id: &str,
        display_type: Option<&str>,
    ) -> Result<Vec<Value>, AppStoreConnectError> {
        let mut endpoint = format!(
            "appStoreVersionLocalizations/{}/appScreenshotSets",
            localization_id
        );

        if let Some(display_type) = display_type {
            endpoint.push_str(&format!("?filter[screenshotDisplayType]={}", display_type));
        }

        let response = self.base.get(&endpoint, None).await?;
        let empty_vec = vec![];
        let screenshot_sets = response
            .get("data")
            .and_then(|d| d.as_array())
            .unwrap_or(&empty_vec);

        let mut all_screenshots = Vec::new();
        for set_data in screenshot_sets {
            if let Some(set_id) = set_data.get("id").and_then(|id| id.as_str()) {
                let screenshots_response = self
                    .base
                    .get(
                        &format!("appScreenshotSets/{}/appScreenshots", set_id),
                        None,
                    )
                    .await?;

                if let Some(screenshots) =
                    screenshots_response.get("data").and_then(|d| d.as_array())
                {
                    for mut screenshot in screenshots.iter().cloned() {
                        if let Some(display_type) = set_data
                            .get("attributes")
                            .and_then(|a| a.get("screenshotDisplayType"))
                        {
                            if let Some(screenshot_obj) = screenshot.as_object_mut() {
                                screenshot_obj
                                    .insert("displayType".to_string(), display_type.clone());
                            }
                        }
                        all_screenshots.push(screenshot);
                    }
                }
            }
        }

        Ok(all_screenshots)
    }

    pub async fn create_screenshot_set(
        &self,
        localization_id: &str,
        display_type: &str,
    ) -> Result<Value, AppStoreConnectError> {
        let data = json!({
            "data": {
                "type": "appScreenshotSets",
                "attributes": {
                    "screenshotDisplayType": display_type
                },
                "relationships": {
                    "appStoreVersionLocalization": {
                        "data": {
                            "type": "appStoreVersionLocalizations",
                            "id": localization_id
                        }
                    }
                }
            }
        });

        let response = self.base.post("appScreenshotSets", data).await?;
        response
            .get("data")
            .cloned()
            .ok_or_else(|| AppStoreConnectError::Api {
                message: "Invalid response format".to_string(),
            })
    }

    pub async fn upload_screenshot(
        &self,
        screenshot_set_id: &str,
        file_name: &str,
        file_size: u64,
        width: u32,
        height: u32,
    ) -> Result<Value, AppStoreConnectError> {
        let data = json!({
            "data": {
                "type": "appScreenshots",
                "attributes": {
                    "fileSize": file_size,
                    "fileName": file_name,
                    "sourceFileChecksum": "",
                    "imageAsset": {
                        "width": width,
                        "height": height
                    }
                },
                "relationships": {
                    "appScreenshotSet": {
                        "data": {
                            "type": "appScreenshotSets",
                            "id": screenshot_set_id
                        }
                    }
                }
            }
        });

        let response = self.base.post("appScreenshots", data).await?;
        response
            .get("data")
            .cloned()
            .ok_or_else(|| AppStoreConnectError::Api {
                message: "Invalid response format".to_string(),
            })
    }

    pub async fn delete_screenshot(&self, screenshot_id: &str) -> Result<(), AppStoreConnectError> {
        self.base
            .delete(&format!("appScreenshots/{}", screenshot_id))
            .await?;
        Ok(())
    }

    pub fn get_display_types() -> HashMap<&'static str, Vec<&'static str>> {
        let mut types = HashMap::new();

        types.insert(
            "iphone",
            vec![
                "APP_IPHONE_65",
                "APP_IPHONE_61",
                "APP_IPHONE_58",
                "APP_IPHONE_55",
                "APP_IPHONE_47",
                "APP_IPHONE_40",
                "APP_IPHONE_35",
            ],
        );

        types.insert(
            "ipad",
            vec![
                "APP_IPAD_PRO_129",
                "APP_IPAD_PRO_3GEN_129",
                "APP_IPAD_PRO_3GEN_11",
                "APP_IPAD_105",
                "APP_IPAD_97",
            ],
        );

        types.insert("apple_tv", vec!["APP_APPLE_TV"]);

        types.insert(
            "apple_watch",
            vec![
                "APP_WATCH_ULTRA",
                "APP_WATCH_SERIES_7",
                "APP_WATCH_SERIES_4",
                "APP_WATCH_SERIES_3",
            ],
        );

        types.insert("mac", vec!["APP_DESKTOP"]);

        types
    }
}
