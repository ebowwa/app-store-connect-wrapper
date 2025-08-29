use crate::base::BaseAPI;
use crate::error::AppStoreConnectError;
use serde_json::{json, Value};
use std::collections::HashMap;

#[derive(Clone)]
pub struct CategoriesAPI {
    base: BaseAPI,
}

impl CategoriesAPI {
    pub fn new(base: BaseAPI) -> Self {
        Self { base }
    }

    pub async fn get_app_categories(
        &self,
        app_info_id: &str,
    ) -> Result<Value, AppStoreConnectError> {
        let mut params = HashMap::new();
        params.insert(
            "fields[appInfos]".to_string(),
            "primaryCategory,secondaryCategory,primarySubcategoryOne,primarySubcategoryTwo,secondarySubcategoryOne,secondarySubcategoryTwo".to_string(),
        );
        params.insert(
            "include".to_string(),
            "primaryCategory,secondaryCategory".to_string(),
        );

        let response = self
            .base
            .get(&format!("appInfos/{}", app_info_id), Some(params))
            .await?;

        let app_info = response.get("data").cloned().unwrap_or_default();
        let empty_vec = vec![];
        let included = response
            .get("included")
            .and_then(|i| i.as_array())
            .unwrap_or(&empty_vec);

        let mut category_lookup = HashMap::new();
        for item in included {
            if let (Some(item_type), Some(id), Some(attributes)) = (
                item.get("type").and_then(|t| t.as_str()),
                item.get("id").and_then(|i| i.as_str()),
                item.get("attributes"),
            ) {
                if item_type == "appCategories" {
                    category_lookup.insert(id.to_string(), attributes.clone());
                }
            }
        }

        let relationships = app_info.get("relationships").cloned().unwrap_or_default();
        let attributes = app_info.get("attributes").cloned().unwrap_or_default();

        let mut result = json!({
            "primaryCategory": null,
            "secondaryCategory": null,
            "primarySubcategoryOne": null,
            "primarySubcategoryTwo": null,
            "secondarySubcategoryOne": null,
            "secondarySubcategoryTwo": null
        });

        if let Some(primary_cat) = relationships
            .get("primaryCategory")
            .and_then(|pc| pc.get("data"))
        {
            if let Some(id) = primary_cat.get("id").and_then(|i| i.as_str()) {
                result["primaryCategory"] = json!({
                    "id": id,
                    "attributes": category_lookup.get(id).cloned().unwrap_or_default()
                });
            }
        }

        if let Some(secondary_cat) = relationships
            .get("secondaryCategory")
            .and_then(|sc| sc.get("data"))
        {
            if let Some(id) = secondary_cat.get("id").and_then(|i| i.as_str()) {
                result["secondaryCategory"] = json!({
                    "id": id,
                    "attributes": category_lookup.get(id).cloned().unwrap_or_default()
                });
            }
        }

        result["primarySubcategoryOne"] = attributes
            .get("primarySubcategoryOne")
            .cloned()
            .unwrap_or(Value::Null);
        result["primarySubcategoryTwo"] = attributes
            .get("primarySubcategoryTwo")
            .cloned()
            .unwrap_or(Value::Null);
        result["secondarySubcategoryOne"] = attributes
            .get("secondarySubcategoryOne")
            .cloned()
            .unwrap_or(Value::Null);
        result["secondarySubcategoryTwo"] = attributes
            .get("secondarySubcategoryTwo")
            .cloned()
            .unwrap_or(Value::Null);

        Ok(result)
    }

    pub async fn update_app_categories(
        &self,
        app_info_id: &str,
        primary_category_id: Option<&str>,
        secondary_category_id: Option<&str>,
        primary_subcategory_one: Option<&str>,
        primary_subcategory_two: Option<&str>,
        secondary_subcategory_one: Option<&str>,
        secondary_subcategory_two: Option<&str>,
    ) -> Result<Value, AppStoreConnectError> {
        let mut data = json!({
            "data": {
                "type": "appInfos",
                "id": app_info_id,
                "attributes": {},
                "relationships": {}
            }
        });

        let data_obj = data["data"].as_object_mut().unwrap();

        if let Some(subcategory) = primary_subcategory_one {
            data_obj["attributes"]["primarySubcategoryOne"] = json!(subcategory);
        }
        if let Some(subcategory) = primary_subcategory_two {
            data_obj["attributes"]["primarySubcategoryTwo"] = json!(subcategory);
        }
        if let Some(subcategory) = secondary_subcategory_one {
            data_obj["attributes"]["secondarySubcategoryOne"] = json!(subcategory);
        }
        if let Some(subcategory) = secondary_subcategory_two {
            data_obj["attributes"]["secondarySubcategoryTwo"] = json!(subcategory);
        }

        if let Some(category_id) = primary_category_id {
            data_obj["relationships"]["primaryCategory"] = json!({
                "data": {
                    "type": "appCategories",
                    "id": category_id
                }
            });
        }

        if let Some(category_id) = secondary_category_id {
            data_obj["relationships"]["secondaryCategory"] = json!({
                "data": {
                    "type": "appCategories",
                    "id": category_id
                }
            });
        }

        let response = self
            .base
            .patch(&format!("appInfos/{}", app_info_id), data)
            .await?;

        response
            .get("data")
            .cloned()
            .ok_or_else(|| AppStoreConnectError::Api {
                message: "Invalid response format".to_string(),
            })
    }

    pub async fn get_all_categories(
        &self,
        platform: Option<&str>,
    ) -> Result<Vec<Value>, AppStoreConnectError> {
        let mut params = HashMap::new();
        params.insert(
            "filter[platforms]".to_string(),
            platform.unwrap_or("IOS").to_string(),
        );
        params.insert("limit".to_string(), "200".to_string());

        let response = self.base.get("appCategories", Some(params)).await?;

        if let Some(data) = response.get("data").and_then(|d| d.as_array()) {
            Ok(data.clone())
        } else {
            Ok(Vec::new())
        }
    }

    pub async fn get_category_by_name(
        &self,
        category_name: &str,
        platform: Option<&str>,
    ) -> Result<Option<Value>, AppStoreConnectError> {
        let categories = self.get_all_categories(platform).await?;

        for category in categories {
            if let Some(display_name) = category
                .get("attributes")
                .and_then(|a| a.get("displayName"))
                .and_then(|n| n.as_str())
            {
                if display_name == category_name {
                    return Ok(Some(category));
                }
            }
        }

        Ok(None)
    }

    pub fn get_categories() -> HashMap<&'static str, &'static str> {
        let mut categories = HashMap::new();
        categories.insert("BOOKS", "Books");
        categories.insert("BUSINESS", "Business");
        categories.insert("DEVELOPER_TOOLS", "Developer Tools");
        categories.insert("EDUCATION", "Education");
        categories.insert("ENTERTAINMENT", "Entertainment");
        categories.insert("FINANCE", "Finance");
        categories.insert("FOOD_AND_DRINK", "Food & Drink");
        categories.insert("GAMES", "Games");
        categories.insert("GRAPHICS_AND_DESIGN", "Graphics & Design");
        categories.insert("HEALTH_AND_FITNESS", "Health & Fitness");
        categories.insert("LIFESTYLE", "Lifestyle");
        categories.insert("MAGAZINES_AND_NEWSPAPERS", "Magazines & Newspapers");
        categories.insert("MEDICAL", "Medical");
        categories.insert("MUSIC", "Music");
        categories.insert("NAVIGATION", "Navigation");
        categories.insert("NEWS", "News");
        categories.insert("PHOTO_AND_VIDEO", "Photo & Video");
        categories.insert("PRODUCTIVITY", "Productivity");
        categories.insert("REFERENCE", "Reference");
        categories.insert("SHOPPING", "Shopping");
        categories.insert("SOCIAL_NETWORKING", "Social Networking");
        categories.insert("SPORTS", "Sports");
        categories.insert("TRAVEL", "Travel");
        categories.insert("UTILITIES", "Utilities");
        categories.insert("WEATHER", "Weather");
        categories
    }

    pub fn get_game_subcategories() -> HashMap<&'static str, &'static str> {
        let mut subcategories = HashMap::new();
        subcategories.insert("ACTION", "Action");
        subcategories.insert("ADVENTURE", "Adventure");
        subcategories.insert("ARCADE", "Arcade");
        subcategories.insert("BOARD", "Board");
        subcategories.insert("CARD", "Card");
        subcategories.insert("CASINO", "Casino");
        subcategories.insert("CASUAL", "Casual");
        subcategories.insert("DICE", "Dice");
        subcategories.insert("EDUCATIONAL", "Educational");
        subcategories.insert("FAMILY", "Family");
        subcategories.insert("MUSIC", "Music");
        subcategories.insert("PUZZLE", "Puzzle");
        subcategories.insert("RACING", "Racing");
        subcategories.insert("ROLE_PLAYING", "Role Playing");
        subcategories.insert("SIMULATION", "Simulation");
        subcategories.insert("SPORTS", "Sports");
        subcategories.insert("STRATEGY", "Strategy");
        subcategories.insert("TRIVIA", "Trivia");
        subcategories.insert("WORD", "Word");
        subcategories
    }
}
