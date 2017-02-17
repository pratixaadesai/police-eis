DROP SCHEMA IF EXISTS feedback CASCADE;
CREATE SCHEMA feedback;

-- Table for adding supervisor feedback on the risk scores and risks
CREATE TABLE feedback.officer_feedback (
    model_id                                                                                            int references results.models(model_id), --should be a foreign key to results.models table
    supervisor_id                                                                                       int, -- id of the supervisor/person making the review
    review_time                                                                                         timestamp, -- timestamp when the review was made
    officer_id                                                                                          int, -- officer id, referreing to staging.officers_hub
    department_defined_officer_id                                                                       text, -- officer id hash
    risk_score_agree                                                                                    bool NOT NULL, -- agree or desagree (boolean) with the risk score generated by model_id stored in results.predictions
    risk_1_agree                                                                                        bool, -- agree or desagree (boolean) with the risk_1 in results.individual_importances
    risk_2_agree                                                                                        bool, -- agree or desagree (boolean) with the risk_2 in results.individual_importances
    risk_3_agree                                                                                        bool, -- agree or desagree (boolean) with the risk_3 in results.individual_importances
    risk_4_agree                                                                                        bool, -- agree or desagree (boolean) with the risk_4 in results.individual_importances
    risk_5_agree                                                                                        bool, -- agree or desagree (boolean) with the risk_5 in results.individual_importances
    comments                                                                                            text, -- comments on the risks factors,
    dismiss_reason											text -- reason for dismissal
);

ALTER TABLE  feedback.officer_feedback ADD CONSTRAINT check_dismiss check(risk_score_agree or dismiss_reason NOTNULL);

-- Table of alters results
CREATE TABLE feedback.alert_results (
    model_id                                                                                            int references results.models(model_id), --should be a foreign key to results.models table
    entity_id												BIGINT,
    as_of_date												TIMESTAMP,
    intervention_id                                                                                     int, -- unique identifier for the intervention provided 
    supervisor_id                                                                                       int, -- id of the supervisor/person in charge of giving a result
    result_time                                                                                         timestamp, -- timestamp when the result of the alter was assigned
    intervention                                                                                        bool, -- if an intervention was assigned or not
    intervention_type                                                                                   int references staging.lookup_intervention_types(code), -- intervention category linked to staging.lookup_intervention_types
    reason_no_intervention                                                                              text -- reasons for not assigning an intervention
);

ALTER TABLE feedback.alert_results ADD CONSTRAINT alert_results_eis_unique UNIQUE (intervention_id);
