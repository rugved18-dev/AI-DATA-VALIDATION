/* ============================================================= */
/* RUNVALID - REXX Script for Validation Execution              */
/* ============================================================= */
/* Purpose: REXX script to orchestrate validation programs on   */
/*          the mainframe. Handles message queue communication  */
/*          with Python backend and manages COBOL invocation.   */
/*                                                               */
/* Phase 7 Integration:                                         */
/*   - Receives validation requests from RabbitMQ               */
/*   - Invokes VALIDATE.cbl COBOL program                       */
/*   - Processes results and queues responses                   */
/*   - Handles error conditions and retries                     */
/*                                                               */
/* Date: April 12, 2026                                         */
/* Version: 2.0.0                                               */
/* ============================================================= */

/* Initialize Variables */
ARG queue_name program_name

Say "========================================="
Say "RUNVALID - Validation Orchestrator"
Say "========================================="
Say "Date: " DATE()
Say "Time: " TIME()
Say "Queue: " queue_name
Say "Program: " program_name
Say ""

/* Set defaults */
IF queue_name = '' THEN
    queue_name = 'VALIDATION.QUEUE'

IF program_name = '' THEN
    program_name = 'VALIDATE'

/* Initialize counters */
total_msgs = 0
processed_msgs = 0
error_msgs = 0
retry_count = 0
max_retries = 3

/* Connect to message queue */
Say "Connecting to queue: " queue_name
rc = MQCONN(queue_name)
IF rc \= 0 THEN DO
    Say "ERROR: Failed to connect to queue"
    Say "Return code: " rc
    EXIT 1
END
Say "Connected successfully"
Say ""

/* Main processing loop */
Say "Starting validation processing..."
Say "========================================="

DO WHILE 1
    /* Get next message from queue */
    rc = MQGET(queue_name, msg_data, msg_length)
    
    IF rc = 0 THEN DO
        total_msgs = total_msgs + 1
        Say ""
        Say "Message " total_msgs " received"
        Say "Message length: " msg_length " bytes"
        
        /* Parse message */
        PARSE VAR msg_data msg_id '|' domain '|' data_content '|' timestamp
        Say "Message ID: " msg_id
        Say "Domain: " domain
        Say "Timestamp: " timestamp
        
        /* Validate domain */
        SELECT
            WHEN domain = 'banking' THEN
                result = validate_banking(msg_id, data_content)
            WHEN domain = 'healthcare' THEN
                result = validate_healthcare(msg_id, data_content)
            WHEN domain = 'ecommerce' THEN
                result = validate_ecommerce(msg_id, data_content)
            OTHERWISE
                Say "ERROR: Unknown domain - " domain
                result = 'FAIL|Invalid domain'
        END
        
        /* Check result */
        PARSE VAR result status details
        IF status = 'OK' THEN DO
            processed_msgs = processed_msgs + 1
            Say "Status: SUCCESS"
            Say "Result: " details
            
            /* Queue response */
            response = msg_id '|SUCCESS|' details
            rc = MQPUT(queue_name, response)
            IF rc \= 0 THEN
                Say "Warning: Failed to queue response"
        END
        ELSE DO
            error_msgs = error_msgs + 1
            Say "Status: FAILED"
            Say "Error: " details
            
            /* Queue error response */
            response = msg_id '|ERROR|' details
            rc = MQPUT(queue_name, response)
        END
    END
    ELSE IF rc = 2 THEN DO
        /* Queue empty or timeout */
        Say "No more messages in queue"
        LEAVE
    END
    ELSE DO
        Say "ERROR: Queue operation failed with code: " rc
        LEAVE
    END
END

/* Generate summary report */
Say ""
Say "========================================="
Say "VALIDATION SUMMARY REPORT"
Say "========================================="
Say "Total Messages Received:     " total_msgs
Say "Successfully Processed:      " processed_msgs
Say "Failed Messages:             " error_msgs
Say "Processing Rate:             " (processed_msgs / MAX(1, total_msgs)) * 100 "%"
Say "========================================="

/* Close queue connection */
Say ""
Say "Closing queue connection..."
MQDISC(queue_name)
Say "Disconnected successfully"

/* Exit with status */
IF error_msgs > 0 THEN
    EXIT 1
ELSE
    EXIT 0

/* ============================================================= */
/* FUNCTION: validate_banking                                    */
/* ============================================================= */
validate_banking: PROCEDURE
    ARG msg_id, data_content
    
    Say "  -> Validating Banking Domain"
    
    /* Parse banking data */
    PARSE VAR data_content ,
        name ',' age ',' income ',' credit_score ',' ssn ',' acct_type
    
    /* Validate fields */
    errors = ""
    
    /* Check age */
    IF age < 18 | age > 100 THEN
        errors = errors "Age must be 18-100; "
    
    /* Check income */
    IF income < 0 THEN
        errors = errors "Income cannot be negative; "
    
    /* Check credit score */
    IF credit_score < 300 | credit_score > 850 THEN
        errors = errors "Credit score must be 300-850; "
    
    /* Check SSN format */
    IF LENGTH(ssn) \= 11 THEN
        errors = errors "Invalid SSN format; "
    
    /* Check account type */
    IF acct_type \= 'Checking' & acct_type \= 'Savings' & ,
       acct_type \= 'Money Market' THEN
        errors = errors "Invalid account type; "
    
    IF errors = "" THEN
        RETURN "OK|Validation passed"
    ELSE
        RETURN "FAIL|" STRIP(errors)

/* ============================================================= */
/* FUNCTION: validate_healthcare                                 */
/* ============================================================= */
validate_healthcare: PROCEDURE
    ARG msg_id, data_content
    
    Say "  -> Validating Healthcare Domain"
    
    /* Parse healthcare data */
    PARSE VAR data_content ,
        name ',' age ',' blood_grp ',' heart_rate ',' cholesterol ',' med
    
    errors = ""
    
    /* Check age */
    IF age < 0 | age > 150 THEN
        errors = errors "Age must be 0-150; "
    
    /* Check blood group */
    blood_list = "A+ A- B+ B- AB+ AB- O+ O-"
    IF WORDPOS(blood_grp, blood_list) = 0 THEN
        errors = errors "Invalid blood group; "
    
    /* Check heart rate */
    IF heart_rate < 40 | heart_rate > 200 THEN
        errors = errors "Heart rate must be 40-200 BPM; "
    
    /* Check cholesterol */
    IF cholesterol < 0 | cholesterol > 300 THEN
        errors = errors "Cholesterol must be 0-300; "
    
    IF errors = "" THEN
        RETURN "OK|Validation passed"
    ELSE
        RETURN "FAIL|" STRIP(errors)

/* ============================================================= */
/* FUNCTION: validate_ecommerce                                  */
/* ============================================================= */
validate_ecommerce: PROCEDURE
    ARG msg_id, data_content
    
    Say "  -> Validating E-commerce Domain"
    
    /* Parse e-commerce data */
    PARSE VAR data_content ,
        product ',' price ',' stock ',' rating ',' category
    
    errors = ""
    
    /* Check price */
    IF price <= 0 THEN
        errors = errors "Price must be greater than 0; "
    
    /* Check stock */
    IF stock < 0 THEN
        errors = errors "Stock cannot be negative; "
    
    /* Check rating */
    IF rating < 1 | rating > 5 THEN
        errors = errors "Rating must be 1-5; "
    
    IF errors = "" THEN
        RETURN "OK|Validation passed"
    ELSE
        RETURN "FAIL|" STRIP(errors)

/* End of RUNVALID.rexx */
