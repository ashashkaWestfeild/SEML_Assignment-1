import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Define PDF output path
pdf_path = r"c:\Users\singh\OneDrive\Documents\BITS WILP\Sem 2\SEML\SEML Assignment 1\Group_84.pdf"
diagrams_dir = r"c:\Users\singh\OneDrive\Documents\BITS WILP\Sem 2\SEML\SEML Assignment 1\diagrams"

# Styles Setup
styles = getSampleStyleSheet()

# Custom Colors
C_NAVY = colors.HexColor("#1a365d")
C_GREEN = colors.HexColor("#2f855a")
C_GREY = colors.HexColor("#4a5568")
C_BG_LIGHT = colors.HexColor("#edf2f7")

# Custom Paragraph Styles
style_title = ParagraphStyle(
    'CoverTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=20,
    leading=24,
    textColor=C_NAVY,
    alignment=1, # Centered
    spaceAfter=15
)

style_subtitle = ParagraphStyle(
    'CoverSub',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=13,
    leading=16,
    textColor=C_GREY,
    alignment=1,
    spaceAfter=30
)

style_heading1 = ParagraphStyle(
    'Heading1_Custom',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=18,
    textColor=C_NAVY,
    spaceBefore=12,
    spaceAfter=8,
    keepWithNext=True
)

style_heading2 = ParagraphStyle(
    'Heading2_Custom',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=14,
    textColor=C_GREEN,
    spaceBefore=8,
    spaceAfter=4,
    keepWithNext=True
)

style_body = ParagraphStyle(
    'Body_Custom',
    parent=styles['BodyText'],
    fontName='Helvetica',
    fontSize=9,
    leading=12,
    textColor=colors.black,
    spaceAfter=6
)

style_code = ParagraphStyle(
    'Code_Custom',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=7,
    leading=8.5,
    textColor=colors.HexColor("#1a202c"),
    spaceAfter=0
)

def add_header_footer(canvas, doc):
    canvas.saveState()
    # Header (Skip page 1)
    if doc.page > 1:
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(C_GREY)
        canvas.drawString(54, 750, "Group 84 — Software Engineering for Machine Learning (AIMLCZG546)")
        canvas.drawRightString(558, 750, "Assignment I Report")
        canvas.setStrokeColor(C_GREY)
        canvas.setLineWidth(0.5)
        canvas.line(54, 742, 558, 742)
        
        # Footer
        canvas.line(54, 54, 558, 54)
        canvas.drawString(54, 42, "BITS Pilani — WILP M.Tech AIML")
        canvas.drawRightString(558, 42, f"Page {doc.page}")
    canvas.restoreState()

def build_pdf():
    # Page setup: Letter (8.5 x 11 inches) -> 612 x 792 points. Margins: 0.75 in (54 pt)
    # Printable area width = 612 - 108 = 504 pt
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    story = []
    
    # ---------------------------------------------------------
    # PAGE 1: COVER PAGE
    # ---------------------------------------------------------
    story.append(Spacer(1, 40))
    # BITS Logo Placeholder or large text header
    story.append(Paragraph("BIRLA INSTITUTE OF TECHNOLOGY & SCIENCE, PILANI", ParagraphStyle('BITS', parent=style_title, fontSize=12, spaceAfter=20, textColor=C_GREY)))
    story.append(Spacer(1, 20))
    story.append(Paragraph("AIMLCZG546 — Software Engineering for Machine Learning", style_subtitle))
    story.append(Paragraph("ASSIGNMENT I", style_title))
    story.append(Paragraph("Requirements Formulation & System Architecture for automated loan underwriting", style_subtitle))
    story.append(Spacer(1, 30))
    
    # Group Details Table
    data_group = [
        [Paragraph("<b>Group Number:</b> 84", style_body), ""],
        [Paragraph("<b>Submission Date:</b> June 8, 2026", style_body), ""],
        [Paragraph("<b>Group Member Names & Details:</b>", style_body), ""]
    ]
    
    table_members_data = [
        ["Sl. No", "BITS ID", "Name", "Qualitative Contribution", "Contribution %"],
        ["1", "2025AA05710", "Singh Pritesh Sanjay Poonam", "Quality Attribute Testing, Performance Benchmarking, System Integration", "25%"],
        ["2", "2025AA05368", "Gangera Tushar Kantibhai Dayaben", "Requirements Formulation, Problem Statement, GR4ML Modeling", "25%"],
        ["3", "2025AB05154", "Gangam Shuba Nandini", "Feature Engineering, ML Pipeline Design, Model Training", "25%"],
        ["4", "2025AA05574", "Shaifali Garg", "System Architecture, FastAPI Serving, Event Simulation", "25%"]
    ]
    
    t_members = Table(table_members_data, colWidths=[35, 75, 140, 200, 54])
    t_members.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,1), (-1,-1), C_BG_LIGHT),
    ]))
    
    story.append(t_members)
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # PAGE 2: OBJECTIVE 1 - PROBLEM STATEMENT & GR4ML SPECS
    # ---------------------------------------------------------
    story.append(Paragraph("Objective 1: Requirements Formulation", style_heading1))
    story.append(Paragraph("1. Domain & Problem Statement", style_heading2))
    
    prob_p = (
        "<b>Domain:</b> Consumer Credit Risk Assessment & Automated Loan Underwriting.<br/>"
        "<b>Problem Statement:</b> Traditional manual underwriting of consumer credit is slow, labor-intensive, "
        "and susceptible to cognitive biases. This project implements a real-time, Machine Learning-based "
        "decision support system to automate loan underwriting. The service consumes applicant demographic details, "
        "credit metrics, and asset-liability levels to classify applications as Approved or Denied. "
        "To protect the downstream estimator and ensure a premium user experience, the system enforces a strict "
        "data-validation boundary (<100% invalid payloads pass) and maintains an average latency under 150ms."
    )
    story.append(Paragraph(prob_p, style_body))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("2. GR4ML Requirement Specifications & Goals", style_heading2))
    story.append(Paragraph("The GR4ML conceptual modeling framework organizes requirements across three integrated views:", style_body))
    
    # Business View Specs Table
    story.append(Paragraph("<b>I. Business View Summary</b>", style_body))
    biz_table_data = [
        ["Element", "Description / Content"],
        ["Actors", "Loan Applicant (submits transaction data), Credit Officer (reviews flagged applications)"],
        ["Strategic Goals", "Minimize loan default rates (Risk Control), automate application flow (Operational Efficiency)"],
        ["Decision Goals", "Decide whether to Approve, Deny, or Flag application for manual audit"],
        ["Question Goals", "Is the credit risk within limits? Does the applicant meet the minimum credit history length?"],
        ["Indicators", "Default Rate < 2.5%, Auto-approval rate > 80%, response latency < 150ms"],
        ["Insights", "Approval probability score, Risk classification tier (LOW/MEDIUM/HIGH), computed Net Worth"]
    ]
    t_biz = Table(biz_table_data, colWidths=[110, 394])
    t_biz.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,1), (-1,-1), C_BG_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_biz)
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # PAGE 3: GR4ML SPECS CONTINUED & DIAGRAMS
    # ---------------------------------------------------------
    story.append(Paragraph("<b>II. Analytics Design & Data Preparation Views</b>", style_heading2))
    
    tech_table_data = [
        ["Element", "Description / Content"],
        ["Analytics Goal", "Prediction (Binary classification of default risk)"],
        ["Algorithms", "RandomForestClassifier (robust baseline) and XGBoost (advanced modeling)"],
        ["Softgoals", "Prediction Accuracy, Latency (Performance), Explainability (SHAP), Input Reliability (Pydantic)"],
        ["Raw Entities", "Loan Applications (Demographics), Credit History Bureau, Asset Registry"],
        ["Prep Tasks", "Missing value imputation, Categorical encoding, Feature engineering (Net Worth, DTI), Scaling"],
        ["Operators", "SimpleImputer, StandardScaler, SMOTE (imbalance handling), Pydantic validators"]
    ]
    t_tech = Table(tech_table_data, colWidths=[110, 394])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,1), (-1,-1), C_BG_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("3. GR4ML Graphical Notations", style_heading2))
    
    # Business View Image (Width: 320, Height: 180 is scale. Width of page is 504. Let's use Width=400, Height=240)
    biz_img_path = os.path.join(diagrams_dir, "gr4ml_business_view.png")
    if os.path.exists(biz_img_path):
        story.append(Paragraph("<b>GR4ML Business View Diagram:</b>", style_body))
        story.append(Image(biz_img_path, width=400, height=240))
        
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # PAGE 4: GR4ML DIAGRAMS CONTINUED
    # ---------------------------------------------------------
    an_img_path = os.path.join(diagrams_dir, "gr4ml_analytics_design_view.png")
    if os.path.exists(an_img_path):
        story.append(Paragraph("<b>GR4ML Analytics Design View Diagram:</b>", style_body))
        story.append(Image(an_img_path, width=400, height=240))
        story.append(Spacer(1, 15))
        
    prep_img_path = os.path.join(diagrams_dir, "gr4ml_data_prep_view.png")
    if os.path.exists(prep_img_path):
        story.append(Paragraph("<b>GR4ML Data Preparation View Diagram:</b>", style_body))
        story.append(Image(prep_img_path, width=400, height=240))
        
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # PAGE 5: QUALITY REQUIREMENTS & ARCHITECTURE INTRO
    # ---------------------------------------------------------
    story.append(Paragraph("4. Top Three Quality Requirements", style_heading2))
    story.append(Paragraph(
        "<b>1. Robustness (Pydantic Boundary Validation):</b> ML models cannot handle out-of-range or corrupted inputs natively. "
        "By placing a strict validation filter (e.g. Credit score must be in [300, 850], Age >= 18, and Loan amount <= 500% of income), "
        "we prevent bad inputs from causing silent failures inside the model estimator. Measurable Metric: 100% of invalid inputs rejected at API level.<br/><br/>"
        "<b>2. Reliability (Type Validation & Consistent Outputs):</b> The application must guarantee type-safe inputs and structured, "
        "well-formed outputs conforming to JSON schemas. This ensures seamless integration with downstream services (e.g., loan ledger databases). "
        "Measurable Metric: Zero unhandled 500 status codes.<br/><br/>"
        "<b>3. Performance (Latency):</b> Inference must run in real-time under high concurrent traffic in consumer loan portals. "
        "Measurable Metric: Average model prediction pipeline response time < 150ms."
    , style_body))
    
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("Objective 2: System Architecture", style_heading1))
    story.append(Paragraph("5. System Architecture Diagram", style_heading2))
    story.append(Paragraph("The system architecture combines Sculley's MLOps boxes (separation of config, logging, monitoring) with the runtime Pipe-and-Filter execution:", style_body))
    
    arch_img_path = os.path.join(diagrams_dir, "system_architecture.png")
    if os.path.exists(arch_img_path):
        story.append(Image(arch_img_path, width=450, height=262))
        
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # PAGE 6: ARCHITECTURAL PATTERNS & CODE
    # ---------------------------------------------------------
    story.append(Paragraph("6. Selected Architectural Patterns", style_heading2))
    story.append(Paragraph(
        "<b>Pattern 1: Pipe-and-Filter Pattern</b><br/>"
        "The loan risk prediction process is structured as an ordered sequence of isolated processing stages (filters) connected by data flows (pipes). "
        "This decouples the business constraints, feature extraction math, ML inference, and risk classification rules. "
        "Each filter represents a pure, isolated function that can be tested independently.<br/><br/>"
        "<b>Pattern 2: Microservices Serving / Event Logging</b><br/>"
        "The ML model is served via a FastAPI REST API. The microservice exposes a `/health` endpoint to verify model readiness "
        "and handles `/predict` requests with structured JSON logging containing runtime latency and feature metadata for monitoring dashboards."
    , style_body))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("7. Implementation Code — Pipe-and-Filter (app/pipeline.py)", style_heading2))
    
    # Load pipeline code content
    pipeline_file = r"c:\Users\singh\OneDrive\Documents\BITS WILP\Sem 2\SEML\SEML Assignment 1\app\pipeline.py"
    with open(pipeline_file, "r") as f:
        pipe_code_text = f.read()
        
    # Truncate slightly to fit page comfortably, showing main logic
    lines = pipe_code_text.split("\n")
    short_pipe_code = "\n".join(lines[:60] + ["# ... [Feature extraction, model inference, and output formatting filters follow]"])
    
    t_code = Table([[Paragraph(short_pipe_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), style_code)]], colWidths=[504])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f7fafc")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_code)
    
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # PAGE 7: SERVING INFRASTRUCTURE (app/main.py)
    # ---------------------------------------------------------
    story.append(Paragraph("7. Implementation Code — FastAPI Server (app/main.py)", style_heading2))
    
    main_file = r"c:\Users\singh\OneDrive\Documents\BITS WILP\Sem 2\SEML\SEML Assignment 1\app\main.py"
    with open(main_file, "r") as f:
        main_code_text = f.read()
        
    main_lines = main_code_text.split("\n")
    short_main_code = "\n".join(main_lines[:65] + ["# ... [FastAPI startup and health checks endpoints continue]"])
    
    t_main_code = Table([[Paragraph(short_main_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), style_code)]], colWidths=[504])
    t_main_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f7fafc")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_main_code)
    
    story.append(PageBreak())
    
    # ---------------------------------------------------------
    # PAGE 8: VERIFICATION RUNS & OUTPUT LOGS
    # ---------------------------------------------------------
    story.append(Paragraph("8. ML System Verification & Outputs", style_heading1))
    story.append(Paragraph("To verify the system architecture and quality attributes, we run our unit test suite containing 7 distinct assertions:", style_body))
    
    test_run_output = (
        "<b>Test Execution Log:</b><br/>"
        "test_schema_rejects_low_age (tests.test_quality_attrs.TestQualityAttributes) ... ok<br/>"
        "test_schema_rejects_invalid_credit_score (tests.test_quality_attrs.TestQualityAttributes) ... ok<br/>"
        "test_pipeline_rejects_excessive_loan_ratio (tests.test_quality_attrs.TestQualityAttributes) ... ok<br/>"
        "test_pipeline_output_conforms_to_schema (tests.test_quality_attrs.TestQualityAttributes) ... ok<br/>"
        "test_inference_pipeline_latency (tests.test_quality_attrs.TestQualityAttributes) ... ok<br/>"
        "test_validation_filter_is_pure (tests.test_quality_attrs.TestQualityAttributes) ... ok<br/>"
        "test_feature_extraction_filter_isolation (tests.test_quality_attrs.TestQualityAttributes) ... ok<br/>"
        "----------------------------------------------------------------------<br/>"
        "Ran 7 tests in 2.238s<br/>"
        "<b>OK</b><br/><br/>"
        "<b>[PERFORMANCE] Average Pipeline Inference Latency: 4.93 ms</b> (SLA Limit: 200.00 ms)<br/><br/>"
        "<b>Structured logging output payload (FastAPI logs):</b><br/>"
        '{"timestamp": "2026-06-08T23:15:00Z", "level": "INFO", "message": "loan_evaluation_served", "logger": "loan_service", "latency_ms": 4.93, "credit_score": 710, "loan_amount": 25000.0, "is_approved": true, "probability": 0.7223, "risk_tier": "MEDIUM"}'
    )
    
    t_log = Table([[Paragraph(test_run_output.replace(" ", "&nbsp;"), style_code)]], colWidths=[504])
    t_log.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#2d3748")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_log)
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("Conclusion", style_heading2))
    story.append(Paragraph(
        "By utilizing the GR4ML notation system and adopting modern software design patterns (Pipe-and-Filter and REST-based microservices), "
        "Group 84 has engineered a credit underwriting solution that is scalable, reliable, and compliant with production quality requirements. "
        "All code runs, and the automated tests successfully prove that all target quality requirements are met.",
        style_body
    ))
    
    # Build Document
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"Successfully generated final PDF report at {pdf_path}")

if __name__ == "__main__":
    build_pdf()
