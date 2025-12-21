#-------------------------------------------
# LOADING LIBRARIES ----
#-------------------------------------------
library(DBI)
library(RPostgres)
library(sf)
library(tidyverse)
library(ggplot2)
library(grid)
library(pROC)
library(qs)
library(randomForest)
library(caret)
library(scales)
library(purrr)
library(patchwork)

#-------------------------------------------
# CONFIGURATION ----
#-------------------------------------------
config <- list(
  model_name = "RandomForest_v1",
  train_year_max = 2015,
  rf_ntree = 500,
  hotspot_threshold = 0.5,
  seed = 123
)

#-------------------------------------------
# CONNECT TO POSTGRESQL ----
#-------------------------------------------
pguser     <- Sys.getenv("PGUSER")
pgpassword <- Sys.getenv("PGPASSWORD")
pghost     <- Sys.getenv("PGHOST")
pgport     <- Sys.getenv("PGPORT")
pgdatabase <- Sys.getenv("PGDATABASE")

if (!all(nzchar(c(pguser, pgpassword, pghost, pgport, pgdatabase)))) {
  stop("One or more PostgreSQL environment variables are missing")
}

con <- dbConnect(
  Postgres(),
  dbname   = pgdatabase,
  host     = pghost,
  port     = as.integer(pgport),
  user     = pguser,
  password = pgpassword
)

#-------------------------------------------
# PULL ML FEATURES TABLE ----
#-------------------------------------------
ml_data <- suppressMessages(
  st_read(con, query = "SELECT * FROM analysis.ml_features")
)

# Train/test split by year
train_data <- ml_data %>% filter(year <= config$train_year_max)
test_data  <- ml_data %>% filter(year >  config$train_year_max)

# Feature matrices
train_x <- train_data %>%
  st_drop_geometry() %>%
  select(mean_depth, mean_sst, mean_ssh, mean_chlor_a)
train_y <- train_data$hotspot_class

test_x <- test_data %>%
  st_drop_geometry() %>%
  select(mean_depth, mean_sst, mean_ssh, mean_chlor_a)
test_y <- test_data$hotspot_class

#-------------------------------------------
# TRAIN RANDOM FOREST ----
#-------------------------------------------
set.seed(config$seed)
rf_model <- randomForest(
  x = train_x,
  y = as.factor(train_y),
  ntree = config$rf_ntree,
  importance = TRUE
)

#-------------------------------------------
# PREDICTIONS (Optimized) ----
#-------------------------------------------
pred_prob <- predict(
  rf_model,
  test_x,
  type = "prob"
)[, "1"]  # probability of hotspot

# Attach probabilities and binary predictions
test_data$hotspot_prob <- pred_prob
test_data$pred_hotspot <- ifelse(pred_prob >= config$hotspot_threshold, 1, 0)

# Create readable class labels
test_data$hotspot_label <- factor(
  ifelse(test_data$pred_hotspot == 1, "Hotspot", "Non-hotspot"),
  levels = c("Non-hotspot", "Hotspot")
)

#-------------------------------------------
# ROC CURVES ----
#-------------------------------------------

# Compute per-year ROC objects safely
roc_by_year <- test_data %>%
  group_by(year) %>%
  summarise(
    roc_obj = list({
      # Only calculate ROC if both classes (0 and 1) are present
      if (length(unique(hotspot_class)) == 2) {
        roc(hotspot_class, hotspot_prob)
      } else {
        NULL
      }
    }),
    .groups = "drop"
  )


roc_data_all <- do.call(rbind, lapply(1:nrow(roc_by_year), function(i) {
  df <- as.data.frame(coords(roc_by_year$roc_obj[[i]], "all"))
  df$year <- roc_by_year$year[i]
  df
}))

overall_roc <- roc(test_data$hotspot_class, test_data$hotspot_prob)
overall_auc <- auc(overall_roc)

roc_curve_plot <- ggplot() +
  geom_line(data = roc_data_all, aes(x = 1 - specificity, y = sensitivity, color = factor(year)), linewidth = 1) +
  geom_line(data = as.data.frame(coords(overall_roc, "all")), aes(x = 1 - specificity, y = sensitivity),
            color = "black", linewidth = 1.5) +
  geom_abline(linetype = "dashed", color = "grey50") +
  theme_minimal() +
  labs(
    title = "ROC Curves for Hotspot Predictions (Jan–June, 2016-2020)",
    subtitle = paste("Overall AUC =", round(overall_auc, 3)),
    x = "False Positive Rate (FPR)",
    y = "True Positive Rate (TPR)",
    color = "Year"
  )

ggsave("outputs/roc_curve_by_year.png", plot = roc_curve_plot, width = 8, height = 6, dpi = 96)

# Save AUCs for reference
auc_by_year <- roc_by_year %>%
  mutate(
    AUC = map_dbl(roc_obj, ~ if (!is.null(.x)) auc(.x) else NA_real_)
  ) %>%
  select(year, AUC)

qsave(
  list(overall_auc = as.numeric(overall_auc),
       auc_by_year = auc_by_year),
  file = "outputs/auc_results.qs"
)

# Plotting AUC by Year
auc_plot <- ggplot(auc_by_year, aes(x = year, y = AUC)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  geom_text(aes(label = round(AUC, 3)), vjust = -0.3, size = 3) +
  theme_minimal() +
  labs(
    title = "AUC for Hotspot Predictions by Year (Jan–June)",
    x = "Year",
    y = "AUC"
  ) +
  theme(legend.position = "none")

ggsave("outputs/auc_by_year.png", plot = auc_plot, width = 8, height = 6, dpi = 96)


# ----------------------------------------
# MODEL PERFORMANCE SUMMARY ----
# ----------------------------------------

# Overall confusion matrix
overall_cm <- confusionMatrix(
  data = test_data$hotspot_label,
  reference = factor(
    test_data$hotspot_class,
    levels = c(0, 1),
    labels = c("Non-hotspot", "Hotspot")
  )
)

overall_metrics <- tibble(
  model_name = config$model_name,
  dataset = paste0("Test (", min(test_data$year), "–", max(test_data$year), ")"),
  AUC = as.numeric(overall_auc),
  Accuracy = overall_cm$overall["Accuracy"],
  Kappa = overall_cm$overall["Kappa"],
  Precision = overall_cm$byClass["Pos Pred Value"],
  Recall = overall_cm$byClass["Sensitivity"],
  Specificity = overall_cm$byClass["Specificity"],
  F1 = overall_cm$byClass["F1"]
)

# AUC by year (wide → tidy)
auc_year_metrics <- auc_by_year %>%
  mutate(metric = paste0("AUC_", year)) %>%
  select(metric, value = AUC)

# Combine into one summary table
model_performance_summary <- overall_metrics %>%
  pivot_longer(
    cols = -c(model_name, dataset),
    names_to = "metric",
    values_to = "value"
  ) %>%
  bind_rows(
    auc_year_metrics %>%
      mutate(
        model_name = config$model_name,
        dataset = paste0("Test (", min(test_data$year), "–", max(test_data$year), ")")
      ) %>%
      select(model_name, dataset, metric, value)
  ) %>%
  select(-cell_geom)  # <- drop geometry column


# Save CSV
write.csv(
  model_performance_summary,
  "outputs/model_performance_summary.csv",
  row.names = FALSE
)


#-------------------------------------------
# CALIBRATION CURVE ----
#-------------------------------------------
calibration_df <- test_data %>%
  mutate(
    prob_bin = cut(
      hotspot_prob,
      breaks = seq(0, 1, by = 0.1),
      include.lowest = TRUE
    )
  ) %>%
  group_by(year, prob_bin) %>%
  summarise(
    mean_pred_prob = mean(hotspot_prob, na.rm = TRUE),
    observed_rate  = mean(hotspot_class, na.rm = TRUE),
    n = n(),
    .groups = "drop"
  )

qsave(calibration_df, file = "outputs/calibration_data.qs")

calibration_plot <- ggplot(calibration_df, aes(x = mean_pred_prob, y = observed_rate)) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "grey50") +
  geom_point(size = 2, color = "steelblue") +
  geom_line(color = "steelblue") +
  facet_wrap(~ year) +
  coord_equal() +
  theme_minimal() +
  theme(panel.spacing = unit(1.5, "lines")) +
  labs(
    title = "Calibration Curve for Hotspot Probability",
    subtitle = "Model trained and evaluated on Jan–June data (2016–2020)",
    x = "Mean Predicted Probability",
    y = "Observed Hotspot Frequency"
  )

ggsave("outputs/calibration_curve_by_year.png", plot = calibration_plot, width = 10, height = 6, dpi = 96)
qsave(calibration_plot, "outputs/calibration_curve_by_year.qs")

#-------------------------------------------
# HOTSPOT PROBABILITY MAPS ----
#-------------------------------------------
p_prob <- ggplot(test_data) +
  geom_sf(aes(fill = hotspot_prob), color = NA) +
  scale_fill_viridis_c(option = "plasma", name = "Hotspot Probability") +
  facet_wrap(~ year) +
  theme_minimal() +
  theme(panel.spacing = unit(1.5, "lines")) +
  labs(
    title = "Predicted Probability of Squid Catch Hotspots",
    subtitle = "Random Forest model applied to unseen years (Jan–June, 2016–2020)",
    caption = "Geotentacles | ML-based hotspot probability"
  )

ggsave("outputs/hotspot_probability_by_year.png", plot = p_prob, width = 12, height = 8, dpi = 96)
qsave(p_prob, "outputs/hotspot_probability_by_year.qs")

#-------------------------------------------
# BINARY PREDICTIONS AND CONFUSION MATRICES ----
#-------------------------------------------
conf_by_year <- test_data %>%
  split(.$year) %>%
  lapply(function(df_year) {
    confusionMatrix(
      data = df_year$hotspot_label,
      reference = factor(df_year$hotspot_class, levels = c(0,1), labels = c("Non-hotspot", "Hotspot"))
    )
  })

qsave(conf_by_year, "outputs/confusion_matrices_by_year.qs")

# Heatmaps for each year
conf_plots_by_year <- lapply(names(conf_by_year), function(y) {
  cm_table <- as.data.frame(conf_by_year[[y]]$table)
  ggplot(cm_table, aes(x = Reference, y = Prediction, fill = Freq)) +
    geom_tile(color = "white") +
    geom_text(aes(label = Freq), size = 5) +
    scale_fill_gradient(low = "lightblue", high = "red") +
    theme_minimal() +
    theme(panel.spacing = unit(1.5, "lines")) +
    labs(
      title = paste("Confusion Matrix", y),
      x = "Predicted Class",
      y = "Observed Class",
      fill = "Count"
    )
})
names(conf_plots_by_year) <- names(conf_by_year)
qsave(conf_plots_by_year, "outputs/confusion_plots_by_year.qs")

# Combine all yearly confusion matrix plots into one panel
combined_conf_plot <- wrap_plots(conf_plots_by_year, ncol = 2) + 
  plot_annotation(title = "Confusion Matrices by Year (Jan–June)")

# Save to PNG
ggsave(
  filename = "outputs/combined_confusion_matrices.png",
  plot = combined_conf_plot,
  width = 12,
  height = 8,
  dpi = 96
)

# Predicted hotspot maps
p <- ggplot(test_data) +
  geom_sf(aes(fill = hotspot_label), color = NA) +
  scale_fill_manual(values = c("Non-hotspot" = "lightblue", "Hotspot" = "red"), name = "Predicted Class") +
  facet_wrap(~ year) +
  theme_minimal() +
  theme(panel.spacing = unit(1.5, "lines")) +
  labs(
    title = "Predicted Squid Catch Hotspots by Year",
    subtitle = "Random Forest classification on Jan–June data (2016–2020)",
    caption = "Geotentacles | ML-based hotspot prediction"
  )

ggsave("outputs/predicted_hotspots_by_year.png", plot = p, width = 12, height = 8, dpi = 96)
qsave(p, "outputs/predicted_hotspots_by_year.qs")

#-------------------------------------------
# VALIDATION ----
#-------------------------------------------
validation_df <- test_data %>%
  mutate(
    prob_bin = cut(
      hotspot_prob,
      breaks = c(0, 0.2, 0.4, 0.6, 1),
      labels = c("0–0.2", "0.2–0.4", "0.4–0.6", ">0.6"),
      include.lowest = TRUE
    )
  ) %>%
  group_by(year, prob_bin) %>%
  summarise(
    mean_catch = mean(total_catch_kg, na.rm = TRUE),
    sd_catch   = sd(total_catch_kg, na.rm = TRUE),
    n_cells    = n(),
    se_catch   = sd_catch / sqrt(n_cells),
    .groups = "drop"
  )

ggplot(validation_df, aes(x = prob_bin, y = mean_catch)) +
  geom_col(fill = "steelblue") +
  geom_errorbar(aes(ymin = mean_catch - se_catch, ymax = mean_catch + se_catch), width = 0.2) +
  geom_text(aes(label = paste0("n=", n_cells), y = mean_catch + se_catch), vjust = -0.2, size = 3) +
  facet_wrap(~ year) +
  scale_y_continuous(labels = label_number(scale = 1e-3, suffix = "k")) +
  theme_minimal() +
  theme(panel.spacing = unit(1.5, "lines")) +
  labs(
    title = "Observed Catch by Predicted Hotspot Probability",
    subtitle = "Jan–June data (2016–2020)",
    x = "Predicted Hotspot Probability Bin",
    y = "Mean Observed Catch (thousand kg)"
  )

ggsave("outputs/hotspot_probability_validation.png", width = 12, height = 8, dpi = 96)
qsave(p, "outputs/hotspot_probability_validation.qs")

#-------------------------------------------
# EXPORT TO POSTGRESQL ----
#-------------------------------------------
export_df <- test_data %>%
  mutate(
    hotspot_flag = ifelse(hotspot_prob >= config$hotspot_threshold, 1, 0),
    hotspot_class = ifelse(hotspot_flag == 1, "Hotspot", "Non-hotspot"),
    model_name = config$model_name,
    created_at = Sys.time()
  ) %>%
  select(
    year,
    hotspot_prob,
    hotspot_flag,
    hotspot_class,
    model_name,
    created_at,
    cell_geom
  )

st_write(
  export_df,
  dsn = con,
  layer = DBI::Id(schema = "analysis", table = "predicted_hotspots_ml"),
  delete_layer = TRUE,
  quiet = FALSE
)

