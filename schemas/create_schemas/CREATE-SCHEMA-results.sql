/*
This schema is used for is used for testing and evaluating models
*/

DROP SCHEMA IF EXISTS results CASCADE;
CREATE SCHEMA results;

-- model group table for uniquely identifying similar models run at different time periods
CREATE TABLE results.model_groups
(
  model_group_id   SERIAL PRIMARY KEY,
  model_type       TEXT,
  model_parameters JSONB,
  feature_list     TEXT [],
  model_config     JSONB
);

-- experiments configurations
CREATE TABLE results.experiments (
   experiment_hash    TEXT PRIMARY KEY ,
   config             JSONB
);

CREATE INDEX ON results.experiments (experiment_hash);

-- model table containing each of the models run.
CREATE TABLE results.models (
  model_id          SERIAL PRIMARY KEY,
  model_group_id    INT REFERENCES results.model_groups (model_group_id),
  run_time          TIMESTAMP,
  batch_run_time    TIMESTAMP,
  model_type        TEXT,
  model_parameters  JSONB,
  model_comment     TEXT,
  batch_comment     TEXT,
  config            JSONB,
  test              BOOL,
  model_hash        VARCHAR(36) UNIQUE,
  train_matrix_uuid VARCHAR(36),
  train_end_time    TIMESTAMP,
  experiment_hash   TEXT REFERENCES results.experiments (experiment_hash)
);
CREATE INDEX ON results.models (train_end_time);

-- predictions corresponding to each model.
CREATE TABLE results.predictions (
  model_id    INT REFERENCES results.models (model_id),
  as_of_date  TIMESTAMP,
  entity_id   BIGINT,
  score       REAL,
  label_value INT,
  rank_abs    INT,
  rank_pct    REAL,
  matrix_uuid VARCHAR(36)
);

CREATE INDEX ON results.predictions (model_id);
CREATE INDEX ON results.predictions (as_of_date);
CREATE INDEX ON results.predictions (model_id, as_of_date);

-- evaluation table containing metrics for each of the models run.
CREATE TABLE results.evaluations
(
    model_id INT,
    metric VARCHAR,
    parameter VARCHAR,
    value REAL,
    comment VARCHAR,
    evaluation_start_time TIMESTAMP,
    evaluation_end_time TIMESTAMP,
    prediction_frequency INTERVAL,
    CONSTRAINT evaluations_model_id_fkey FOREIGN KEY (model_id) REFERENCES results.models (model_id)
);
CREATE INDEX evaluations_model_id_as_of_date_idx ON results.evaluations (model_id, evaluation_start_time);
CREATE INDEX evaluations_parameter_metric_model_id_idx ON results.evaluations (parameter, metric, model_id);
CREATE INDEX evaluations_as_of_date_idx ON results.evaluations (evaluation_start_time);



-- feature_importance table for storing a json with feature importances
CREATE TABLE results.feature_importances (
  model_id           INT REFERENCES results.models (model_id),
  feature            TEXT,
  feature_importance REAL,
  rank_abs           INT,
  rank_pct           REAL
);

CREATE INDEX ON results.feature_importances (model_id);

-- individual feature importance

DROP TABLE IF EXISTS results.individual_importances;
CREATE TABLE results.individual_importances(
  model_id    INT REFERENCES results.models (model_id),
  as_of_date  TIMESTAMP,
  entity_id   BIGINT,
  risk_1      TEXT,
  risk_2      TEXT,
  risk_3      TEXT,
  risk_4      TEXT,
  risk_5      TEXT
);

CREATE INDEX ON results.individual_importances (as_of_date);
CREATE INDEX ON results.individual_importances (entity_id,as_of_date);




