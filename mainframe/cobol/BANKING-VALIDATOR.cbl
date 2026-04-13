       IDENTIFICATION DIVISION.
       PROGRAM-ID. BANKING-VALIDATOR.
       AUTHOR. AI Data Validation Team.
       DATE-WRITTEN. April 12, 2026.
       
      * ================================================================
      * BANKING VALIDATOR - COBOL Program for Banking Data Validation
      * ================================================================
      * Purpose:
      *   This program validates banking customer data by checking
      *   AGE and INCOME against predefined business rules.
      *
      * Input Parameters:
      *   - AGE: Customer age (must be 18-65)
      *   - INCOME: Annual income in dollars (must be > 0)
      *
      * Output:
      *   - Validation result: VALID or INVALID
      *   - Detailed error messages if validation fails
      *
      * Business Rules:
      *   Rule 1: Age must be minimum 18 years (adult)
      *   Rule 2: Age must be maximum 65 years (retirement age)
      *   Rule 3: Income must be greater than $0.00
      *   Rule 4: Income precision: two decimal places (cents)
      *
      * Example Validations:
      *   Input: AGE=35, INCOME=75000.00  → Output: VALID
      *   Input: AGE=16, INCOME=50000.00  → Output: INVALID (too young)
      *   Input: AGE=70, INCOME=60000.00  → Output: INVALID (too old)
      *   Input: AGE=40, INCOME=-5000.00  → Output: INVALID (negative income)
      *
      * Version: 2.0.0
      * Last Modified: April 12, 2026
      * ================================================================
      
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
      * No special configuration required for this program
       
       INPUT-OUTPUT SECTION.
      * No file I/O required - accepts inline parameters
       
       DATA DIVISION.
       FILE SECTION.
      * No files are used in this program
       
       WORKING-STORAGE SECTION.
      
      * ================================================================
      * INPUT VARIABLES - Received from caller
      * ================================================================
       01 WS-INPUT-PARAMETERS.
           05 WS-CUSTOMER-AGE         PIC 9(3) VALUE 0.
           05 WS-CUSTOMER-INCOME      PIC 9(10)V99 VALUE 0.
       
      * ================================================================
      * VALIDATION VARIABLES - Used during validation checks
      * ================================================================
       01 WS-VALIDATION-FLAGS.
           05 WS-VALIDATION-STATUS   PIC X(10) VALUE 'INVALID'.
               88 VALIDATION-VALID     VALUE 'VALID'.
               88 VALIDATION-INVALID   VALUE 'INVALID'.
           05 WS-ERROR-COUNT          PIC 9(2) VALUE 0.
           05 WS-ERROR-MESSAGE        PIC X(500) VALUE SPACES.
       
      * ================================================================
      * RULE CHECKING VARIABLES
      * ================================================================
       01 WS-AGE-VALIDATION.
           05 MIN-AGE                 PIC 9(3) VALUE 18.
           05 MAX-AGE                 PIC 9(3) VALUE 65.
           05 WS-AGE-VALID            PIC X(1) VALUE 'Y'.
           05 WS-AGE-ERROR            PIC X(100) VALUE SPACES.
       
       01 WS-INCOME-VALIDATION.
           05 MIN-INCOME              PIC 9(10)V99 VALUE 0.
           05 WS-INCOME-VALID         PIC X(1) VALUE 'Y'.
           05 WS-INCOME-ERROR         PIC X(100) VALUE SPACES.
       
      * ================================================================
      * OUTPUT VARIABLES - Results and messages
      * ================================================================
       01 WS-OUTPUT-RESULTS.
           05 WS-RESULT-MESSAGE       PIC X(100) VALUE SPACES.
           05 WS-DETAIL-MESSAGE       PIC X(500) VALUE SPACES.
           05 WS-FORMATTED-AGE        PIC Z(2)9.
           05 WS-FORMATTED-INCOME     PIC Z(9)9.99.
       
      * ================================================================
      * PROGRAM CONTROL VARIABLES
      * ================================================================
       01 WS-PROGRAM-CONTROL.
           05 WS-TIMESTAMP            PIC X(26) VALUE SPACES.
           05 WS-PROGRAM-STATUS       PIC X(1) VALUE 'Y'.
       
       PROCEDURE DIVISION.
       
      * ================================================================
      * MAIN PROGRAM FLOW
      * ================================================================
       PROGRAM-START.
           PERFORM DISPLAY-PROGRAM-HEADER.
           PERFORM GET-INPUT-DATA.
           PERFORM VALIDATE-BANKING-DATA.
           PERFORM DISPLAY-VALIDATION-RESULTS.
           PERFORM PROGRAM-TERMINATION.
           STOP RUN.
       
      * ================================================================
      * SECTION: DISPLAY-PROGRAM-HEADER
      * Purpose: Display program title and initialization message
      * ================================================================
       DISPLAY-PROGRAM-HEADER.
           DISPLAY "====================================================".
           DISPLAY "BANKING VALIDATOR - Data Validation Program".
           DISPLAY "Version: 2.0.0 (Phase 7)".
           DISPLAY "Date: April 12, 2026".
           DISPLAY "====================================================".
           DISPLAY " ".
           DISPLAY "Program initialized successfully".
           DISPLAY "Maximum Age Allowed: 65 years".
           DISPLAY "Minimum Age Required: 18 years".
           DISPLAY "Minimum Income Required: $0.01".
           DISPLAY " ".
       
      * ================================================================
      * SECTION: GET-INPUT-DATA
      * Purpose: Accept AGE and INCOME from user input
      * ================================================================
       GET-INPUT-DATA.
           DISPLAY "====================================================".
           DISPLAY "Enter Customer Information:".
           DISPLAY "====================================================".
           
      *    Prompt and accept age
           DISPLAY "Enter Customer Age (18-65): " 
               WITH NO ADVANCING.
           ACCEPT WS-CUSTOMER-AGE.
           
      *    Prompt and accept income
           DISPLAY "Enter Annual Income ($0.00+): " 
               WITH NO ADVANCING.
           ACCEPT WS-CUSTOMER-INCOME.
           
           DISPLAY " ".
       
      * ================================================================
      * SECTION: VALIDATE-BANKING-DATA
      * Purpose: Perform all validation checks against business rules
      * ================================================================
       VALIDATE-BANKING-DATA.
           DISPLAY "====================================================".
           DISPLAY "Performing Validation Checks...".
           DISPLAY "====================================================".
           DISPLAY " ".
           
      *    Initialize validation status to VALID (optimistic approach)
           MOVE 'VALID' TO WS-VALIDATION-STATUS.
           MOVE 0 TO WS-ERROR-COUNT.
           MOVE SPACES TO WS-ERROR-MESSAGE.
           
      *    Rule 1: Check minimum age (18 years)
           PERFORM CHECK-MINIMUM-AGE.
           
      *    Rule 2: Check maximum age (65 years)
           PERFORM CHECK-MAXIMUM-AGE.
           
      *    Rule 3: Check income is positive (greater than $0.00)
           PERFORM CHECK-INCOME-POSITIVE.
           
      *    Rule 4: Build error message if any validation failed
           PERFORM BUILD-VALIDATION-MESSAGE.
       
      * ================================================================
      * SECTION: CHECK-MINIMUM-AGE
      * Purpose: Verify customer age is at least 18 years
      * Business Rule: Age must not be less than 18
      * ================================================================
       CHECK-MINIMUM-AGE.
           DISPLAY "Checking Rule 1: Minimum Age (18 years)".
           
           IF WS-CUSTOMER-AGE < MIN-AGE
               MOVE 'N' TO WS-AGE-VALID
               MOVE 'INVALID' TO WS-VALIDATION-STATUS
               STRING "Age must be at least " MIN-AGE " (actual: " 
                   WS-CUSTOMER-AGE ")"
                   DELIMITED BY SIZE INTO WS-AGE-ERROR
               DISPLAY "  ✗ FAILED - " WS-AGE-ERROR
               ADD 1 TO WS-ERROR-COUNT
           ELSE
               DISPLAY "  ✓ PASSED - Age is valid (>= 18)"
           END-IF.
           
           DISPLAY " ".
       
      * ================================================================
      * SECTION: CHECK-MAXIMUM-AGE
      * Purpose: Verify customer age does not exceed 65 years
      * Business Rule: Age must not exceed 65
      * ================================================================
       CHECK-MAXIMUM-AGE.
           DISPLAY "Checking Rule 2: Maximum Age (65 years)".
           
           IF WS-CUSTOMER-AGE > MAX-AGE
               MOVE 'N' TO WS-AGE-VALID
               MOVE 'INVALID' TO WS-VALIDATION-STATUS
               STRING "Age must not exceed " MAX-AGE " (actual: " 
                   WS-CUSTOMER-AGE ")"
                   DELIMITED BY SIZE INTO WS-AGE-ERROR
               DISPLAY "  ✗ FAILED - " WS-AGE-ERROR
               ADD 1 TO WS-ERROR-COUNT
           ELSE
               DISPLAY "  ✓ PASSED - Age is within range (<= 65)"
           END-IF.
           
           DISPLAY " ".
       
      * ================================================================
      * SECTION: CHECK-INCOME-POSITIVE
      * Purpose: Verify customer income is greater than $0.00
      * Business Rule: Income must be positive value
      * ================================================================
       CHECK-INCOME-POSITIVE.
           DISPLAY "Checking Rule 3: Income Amount (> $0.00)".
           
           IF WS-CUSTOMER-INCOME <= MIN-INCOME
               MOVE 'N' TO WS-INCOME-VALID
               MOVE 'INVALID' TO WS-VALIDATION-STATUS
               STRING "Income must be greater than $0.00 (actual: $" 
                   WS-CUSTOMER-INCOME ")"
                   DELIMITED BY SIZE INTO WS-INCOME-ERROR
               DISPLAY "  ✗ FAILED - " WS-INCOME-ERROR
               ADD 1 TO WS-ERROR-COUNT
           ELSE
               DISPLAY "  ✓ PASSED - Income is positive (> $0.00)"
           END-IF.
           
           DISPLAY " ".
       
      * ================================================================
      * SECTION: BUILD-VALIDATION-MESSAGE
      * Purpose: Construct detailed validation result message
      * ================================================================
       BUILD-VALIDATION-MESSAGE.
           MOVE WS-CUSTOMER-AGE TO WS-FORMATTED-AGE.
           MOVE WS-CUSTOMER-INCOME TO WS-FORMATTED-INCOME.
           
           STRING "Customer Age: " WS-FORMATTED-AGE " | "
                  "Annual Income: $" WS-FORMATTED-INCOME
                   DELIMITED BY SIZE INTO WS-DETAIL-MESSAGE.
       
      * ================================================================
      * SECTION: DISPLAY-VALIDATION-RESULTS
      * Purpose: Display final validation status and summary
      * ================================================================
       DISPLAY-VALIDATION-RESULTS.
           DISPLAY "====================================================".
           DISPLAY "VALIDATION RESULTS".
           DISPLAY "====================================================".
           DISPLAY " ".
           
      *    Display customer information
           DISPLAY WS-DETAIL-MESSAGE.
           DISPLAY " ".
           
      *    Display validation status in prominent format
           DISPLAY "Status: " WS-VALIDATION-STATUS.
           DISPLAY " ".
           
      *    Display detailed results based on validation status
           IF WS-VALIDATION-STATUS = 'VALID'
               DISPLAY "✓ All validation rules passed successfully!"
               DISPLAY "  This customer profile is APPROVED for banking"
               DISPLAY "  services."
           ELSE
               DISPLAY "✗ Validation FAILED - See details below:".
               DISPLAY " "
               DISPLAY "Error Summary:"
               DISPLAY "  Total Errors Found: " WS-ERROR-COUNT
               
      *        Display age validation error if applicable
               IF WS-AGE-VALID = 'N'
                   DISPLAY "  • Age Validation Error:"
                   DISPLAY "    " WS-AGE-ERROR
               END-IF
               
      *        Display income validation error if applicable
               IF WS-INCOME-VALID = 'N'
                   DISPLAY "  • Income Validation Error:"
                   DISPLAY "    " WS-INCOME-ERROR
               END-IF
               
               DISPLAY " "
               DISPLAY "  Recommendation: Please verify customer"
               DISPLAY "  information and resubmit."
           END-IF.
           
           DISPLAY " ".
       
      * ================================================================
      * SECTION: PROGRAM-TERMINATION
      * Purpose: Display closing messages and exit program
      * ================================================================
       PROGRAM-TERMINATION.
           DISPLAY "====================================================".
           DISPLAY "Program execution completed successfully".
           DISPLAY "Thank you for using Banking Validator".
           DISPLAY "====================================================".
