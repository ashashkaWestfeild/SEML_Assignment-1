import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure the output directory exists
output_dir = r"c:\Users\singh\OneDrive\Documents\BITS WILP\Sem 2\SEML\SEML Assignment 1\diagrams"
os.makedirs(output_dir, exist_ok=True)

# Custom color palette (modern, premium)
C_PRIMARY = "#1a365d"   # Navy Blue
C_SECONDARY = "#2f855a" # Muted Green
C_ACCENT = "#c05621"    # Burnt Orange
C_BG = "#f7fafc"        # Off-white
C_TEXT = "#2d3748"      # Slate Grey
C_BOX_BG = "#ffffff"    # White
C_BORDER = "#cbd5e0"    # Light Grey

def setup_plot(title, figsize=(10, 6)):
    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    ax.set_facecolor(C_BG)
    fig.patch.set_facecolor(C_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    plt.title(title, fontsize=13, fontweight='bold', color=C_PRIMARY, pad=15)
    return fig, ax

def draw_box(ax, x, y, w, h, text, shape="rect", bg_color=C_BOX_BG, border_color=C_PRIMARY, border_style="-", text_color=C_TEXT, font_weight="normal"):
    if shape == "rect":
        patch = patches.Rectangle((x, y), w, h, linewidth=1.5, edgecolor=border_color, facecolor=bg_color, linestyle=border_style, zorder=3)
    elif shape == "round":
        patch = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", linewidth=1.5, edgecolor=border_color, facecolor=bg_color, linestyle=border_style, zorder=3)
    elif shape == "ellipse":
        patch = patches.Ellipse((x + w/2, y + h/2), w, h, linewidth=1.5, edgecolor=border_color, facecolor=bg_color, linestyle=border_style, zorder=3)
    elif shape == "diamond":
        pts = [[x + w/2, y], [x + w, y + h/2], [x + w/2, y + h], [x, y + h/2]]
        patch = patches.Polygon(pts, linewidth=1.5, edgecolor=border_color, facecolor=bg_color, linestyle=border_style, zorder=3)
    elif shape == "cylinder":
        patch = patches.Rectangle((x, y + h*0.1), w, h*0.8, linewidth=1.5, edgecolor=border_color, facecolor=bg_color, linestyle=border_style, zorder=3)
        top_ellipse = patches.Ellipse((x + w/2, y + h*0.9), w, h*0.2, linewidth=1.5, edgecolor=border_color, facecolor=bg_color, zorder=4)
        bot_ellipse = patches.Ellipse((x + w/2, y + h*0.1), w, h*0.2, linewidth=1.5, edgecolor=border_color, facecolor=bg_color, zorder=4)
        ax.add_patch(top_ellipse)
        ax.add_patch(bot_ellipse)
    else:
        patch = patches.Rectangle((x, y), w, h, linewidth=1.5, edgecolor=border_color, facecolor=bg_color, linestyle=border_style, zorder=3)
        
    ax.add_patch(patch)
    ax.text(x + w/2, y + h/2, text, color=text_color, fontsize=8, fontweight=font_weight, ha='center', va='center', wrap=True, zorder=5)

def draw_arrow(ax, x1, y1, x2, y2, text="", color=C_PRIMARY, style="->"):
    ax.annotate(text, xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, linewidth=1.2, shrinkA=5, shrinkB=5),
                fontsize=7, color=C_TEXT, ha='center', va='center', zorder=2)

# ==========================================
# 1. GR4ML BUSINESS VIEW
# ==========================================
def create_business_view():
    fig, ax = setup_plot("GR4ML Business View — Loan Approval Decision System")
    
    # Draw Actors
    draw_box(ax, 0.5, 4.5, 1.8, 0.8, "Actor: Credit Officer\n(Reviews flags, finalizes credit)", "ellipse", bg_color=C_PRIMARY, border_color=C_PRIMARY, text_color="white", font_weight="bold")
    draw_box(ax, 0.5, 1.5, 1.8, 0.8, "Actor: Loan Applicant\n(Submits financial details)", "ellipse", bg_color=C_PRIMARY, border_color=C_PRIMARY, text_color="white", font_weight="bold")
    
    # Draw Strategic Goals
    draw_box(ax, 3.0, 4.5, 2.0, 0.8, "Strategic Goal:\nMinimize Loan Defaults\n(Risk Management)", "round", bg_color=C_BOX_BG, border_color=C_SECONDARY, border_style="--")
    draw_box(ax, 3.0, 1.5, 2.0, 0.8, "Strategic Goal:\nAutomate Underwriting\n(Operational Efficiency)", "round", bg_color=C_BOX_BG, border_color=C_SECONDARY, border_style="--")
    
    # Draw Decision Goals
    draw_box(ax, 5.8, 3.0, 1.8, 0.8, "Decision Goal:\nApprove / Deny / Review\nLoan Application", "rect", bg_color=C_BOX_BG, border_color=C_ACCENT, font_weight="bold")
    
    # Draw Question Goals
    draw_box(ax, 8.0, 4.5, 1.8, 0.8, "Question Goal:\nIs applicant's credit\nrisk within acceptable limits?", "diamond", bg_color=C_BOX_BG, border_color=C_PRIMARY)
    draw_box(ax, 8.0, 1.5, 1.8, 0.8, "Indicator Goal:\nDefault Rate < 2.5%\nAuto-approval Rate > 80%\nResponse Time < 150ms", "ellipse", bg_color=C_BOX_BG, border_color=C_SECONDARY)
    
    # Draw Arrows
    draw_arrow(ax, 2.3, 4.9, 3.0, 4.9)
    draw_arrow(ax, 2.3, 1.9, 3.0, 1.9)
    
    draw_arrow(ax, 5.0, 4.9, 5.8, 3.4, "supports")
    draw_arrow(ax, 5.0, 1.9, 5.8, 3.4, "supports")
    
    draw_arrow(ax, 7.6, 3.4, 8.0, 4.9, "decides via")
    draw_arrow(ax, 7.6, 3.4, 8.0, 1.9, "measured by")
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "gr4ml_business_view.png"), dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Saved gr4ml_business_view.png")

# ==========================================
# 2. GR4ML ANALYTICS DESIGN VIEW
# ==========================================
def create_analytics_design_view():
    fig, ax = setup_plot("GR4ML Analytics Design View — Model Choices & Softgoals")
    
    # Analytics Goal
    draw_box(ax, 4.0, 4.8, 2.2, 0.8, "Analytics Goal:\nPredict Default Risk\n(Binary Classification)", "rect", bg_color=C_PRIMARY, border_color=C_PRIMARY, text_color="white", font_weight="bold")
    
    # Algorithms
    draw_box(ax, 1.5, 3.2, 2.0, 0.7, "Algorithm:\nRandom Forest Classifier\n(Handles non-linear relationships)", "round", bg_color=C_BOX_BG, border_color=C_SECONDARY)
    draw_box(ax, 6.5, 3.2, 2.0, 0.7, "Algorithm:\nLogistic Regression\n(Fast, explainable baseline)", "round", bg_color=C_BOX_BG, border_color=C_SECONDARY)
    
    # Softgoals
    draw_box(ax, 0.5, 0.8, 1.8, 0.8, "Softgoal: Accuracy\n(Precision & Recall\non default class)", "ellipse", bg_color=C_BOX_BG, border_color=C_ACCENT, border_style="--")
    draw_box(ax, 2.8, 0.8, 1.8, 0.8, "Softgoal: Performance\n(Inference Latency\n< 150ms)", "ellipse", bg_color=C_BOX_BG, border_color=C_ACCENT, border_style="--")
    draw_box(ax, 5.1, 0.8, 1.8, 0.8, "Softgoal: Explainability\n(Feature Importance\nfor auditing approvals)", "ellipse", bg_color=C_BOX_BG, border_color=C_ACCENT, border_style="--")
    draw_box(ax, 7.4, 0.8, 1.8, 0.8, "Softgoal: Reliability\n(Pydantic constraints\non client inputs)", "ellipse", bg_color=C_BOX_BG, border_color=C_ACCENT, border_style="--")
    
    # Arrows & Influences
    draw_arrow(ax, 2.5, 3.2, 4.0, 4.8, "achieves")
    draw_arrow(ax, 7.5, 3.2, 6.2, 4.8, "achieves")
    
    draw_arrow(ax, 2.5, 3.2, 1.4, 1.6, "+ positive")
    draw_arrow(ax, 2.5, 3.2, 3.7, 1.6, "+ positive")
    draw_arrow(ax, 2.5, 3.2, 6.0, 1.6, "++ strong")
    
    draw_arrow(ax, 7.5, 3.2, 3.7, 1.6, "++ strong")
    draw_arrow(ax, 7.5, 3.2, 8.3, 1.6, "+ positive")
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "gr4ml_analytics_design_view.png"), dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Saved gr4ml_analytics_design_view.png")

# ==========================================
# 3. GR4ML DATA PREPARATION VIEW
# ==========================================
def create_data_prep_view():
    fig, ax = setup_plot("GR4ML Data Preparation View — Loan Feature Engineering")
    
    # Raw Data Entities
    draw_box(ax, 0.5, 4.8, 2.0, 0.7, "Entity: Application Data\n(Age, income, loan size,\ndependents, education)", "cylinder", bg_color=C_BOX_BG, border_color=C_PRIMARY)
    draw_box(ax, 0.5, 2.8, 2.0, 0.7, "Entity: Credit History\n(Credit score, defaults,\ninquiries, bankruptcies)", "cylinder", bg_color=C_BOX_BG, border_color=C_PRIMARY)
    draw_box(ax, 0.5, 0.8, 2.0, 0.7, "Entity: Asset Registry\n(Total assets, total liabilities,\nsavings account balance)", "cylinder", bg_color=C_BOX_BG, border_color=C_PRIMARY)
    
    # Data Prep Tasks
    draw_box(ax, 4.0, 4.8, 2.2, 0.8, "Prep Task: Data Cleansing\n(Impute empty values,\nvalidate fields in schemas)", "round", bg_color=C_BOX_BG, border_color=C_SECONDARY)
    draw_box(ax, 4.0, 2.8, 2.2, 0.8, "Prep Task: Feature Extraction\n(Asset-to-Liability Ratio,\nNet Worth, Debt Service)", "round", bg_color=C_BOX_BG, border_color=C_SECONDARY)
    draw_box(ax, 4.0, 0.8, 2.2, 0.8, "Prep Task: Class Imbalance\n(SMOTE oversampling on\ndefault class)", "round", bg_color=C_BOX_BG, border_color=C_SECONDARY)
    
    # Operators & Outputs
    draw_box(ax, 7.5, 3.8, 2.0, 0.8, "Operators:\nSimpleImputer\nStandardScaler\nPydantic validator", "rect", bg_color=C_BOX_BG, border_color=C_ACCENT)
    draw_box(ax, 7.5, 1.8, 2.0, 0.8, "Target Output Dataset:\nCleaned feature array\n(np.ndarray, shape=[1, 10])", "ellipse", bg_color=C_BOX_BG, border_color=C_PRIMARY)
    
    # Arrows
    draw_arrow(ax, 2.5, 5.15, 4.0, 5.15)
    draw_arrow(ax, 2.5, 3.15, 4.0, 3.15)
    draw_arrow(ax, 2.5, 1.15, 4.0, 1.15)
    
    draw_arrow(ax, 6.2, 5.2, 7.5, 4.2)
    draw_arrow(ax, 6.2, 3.2, 7.5, 2.2)
    draw_arrow(ax, 6.2, 1.2, 7.5, 2.2)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "gr4ml_data_prep_view.png"), dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Saved gr4ml_data_prep_view.png")

# ==========================================
# 4. SYSTEM ARCHITECTURE DIAGRAM
# ==========================================
def create_system_architecture():
    fig, ax = setup_plot("Financial Risk Loan Approval Architecture (Sculley & Pipe-and-Filter)", figsize=(12, 7))
    
    # Draw Background Groups for Layers
    # Ingestion Layer
    ax.add_patch(patches.Rectangle((0.2, 0.2), 2.5, 5.4, fill=True, color="#ebf8ff", alpha=0.5, zorder=1))
    ax.text(1.45, 5.45, "Client & Ingestion Layer", fontsize=9, fontweight="bold", color="#2b6cb0", ha="center")
    
    # FastAPI Application Layer (Pipe-and-Filter)
    ax.add_patch(patches.Rectangle((3.0, 0.2), 4.2, 5.4, fill=True, color="#f0fff4", alpha=0.5, zorder=1))
    ax.text(5.1, 5.45, "FastAPI Inference Service (Pipe-and-Filter Pattern)", fontsize=9, fontweight="bold", color="#276749", ha="center")
    
    # MLOps & Storage Layer
    ax.add_patch(patches.Rectangle((7.5, 0.2), 2.3, 5.4, fill=True, color="#fffaf0", alpha=0.5, zorder=1))
    ax.text(8.65, 5.45, "MLOps & Storage", fontsize=9, fontweight="bold", color="#dd6b20", ha="center")

    # Nodes in Client Layer
    draw_box(ax, 0.4, 4.2, 2.1, 0.7, "API Gateway / Clients\n(Web portal, Partner APIs)", "ellipse", bg_color=C_BOX_BG, border_color="#2b6cb0")
    draw_box(ax, 0.4, 2.6, 2.1, 0.7, "Application Queue / Stream\n(Asynchronous load handling)", "rect", bg_color=C_BOX_BG, border_color="#2b6cb0")
    draw_box(ax, 0.4, 1.0, 2.1, 0.7, "Config Management\n(config.py / YAML parameters)", "round", bg_color=C_BOX_BG, border_color="#2b6cb0")

    # Nodes in FastAPI Application Layer (Pipes & Filters)
    draw_box(ax, 3.2, 4.4, 3.8, 0.65, "Filter 1: validate_input()\n(Pydantic validation on credit score & age)", "round", bg_color=C_BOX_BG, border_color="#276749")
    draw_box(ax, 3.2, 3.4, 3.8, 0.65, "Filter 2: extract_features()\n(Computes Asset-to-Liability & Net Worth)", "round", bg_color=C_BOX_BG, border_color="#276749")
    draw_box(ax, 3.2, 2.4, 3.8, 0.65, "Filter 3: run_model()\n(Inference on loaded Random Forest Model)", "round", bg_color=C_BOX_BG, border_color="#276749")
    draw_box(ax, 3.2, 1.4, 3.8, 0.65, "Filter 4: format_response()\n(Risk tiers & output API formatting)", "round", bg_color=C_BOX_BG, border_color="#276749")
    draw_box(ax, 3.2, 0.4, 3.8, 0.65, "Monitoring & Logging\n(Structured JSON logs / Prometheus metrics)", "rect", bg_color=C_BOX_BG, border_color="#276749")

    # Nodes in MLOps & Storage
    draw_box(ax, 7.7, 4.2, 1.9, 0.7, "Redis Feature Store\n(Real-time customer metrics)", "cylinder", bg_color=C_BOX_BG, border_color="#dd6b20")
    draw_box(ax, 7.7, 2.6, 1.9, 0.7, "Model Registry / MLflow\n(Tracks model.pkl artifact)", "rect", bg_color=C_BOX_BG, border_color="#dd6b20")
    draw_box(ax, 7.7, 1.0, 1.9, 0.7, "Database / Data Warehouse\n(PostgreSQL historical logs)", "cylinder", bg_color=C_BOX_BG, border_color="#dd6b20")

    # Data flows
    # Ingestion -> API
    draw_arrow(ax, 1.45, 4.2, 1.45, 3.3)
    draw_arrow(ax, 2.5, 4.5, 3.2, 4.7, "Payload")
    
    # Pipes between filters
    draw_arrow(ax, 5.1, 4.4, 5.1, 4.05, "Pipe 1: LoanApplicationInput")
    draw_arrow(ax, 5.1, 3.4, 5.1, 3.05, "Pipe 2: np.ndarray (1, 10)")
    draw_arrow(ax, 5.1, 2.4, 5.1, 2.05, "Pipe 3: (bool, float)")
    draw_arrow(ax, 5.1, 1.4, 5.1, 1.05, "Pipe 4: LoanApprovalResult")
    
    # Feature store lookup
    draw_arrow(ax, 7.7, 4.55, 7.0, 3.8, "aggregates", style="<->")
    
    # Model load
    draw_arrow(ax, 7.7, 2.95, 7.0, 2.8, "load model.pkl")
    
    # Config injection
    draw_arrow(ax, 2.5, 1.35, 3.2, 1.7, "inject config")
    
    # Log stream
    draw_arrow(ax, 5.1, 1.4, 5.1, 1.05)
    draw_arrow(ax, 3.2, 0.7, 1.45, 2.6, "alert trigger")
    draw_arrow(ax, 7.0, 0.7, 7.7, 1.35, "log write")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "system_architecture.png"), dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Saved system_architecture.png")

if __name__ == "__main__":
    create_business_view()
    create_analytics_design_view()
    create_data_prep_view()
    create_system_architecture()
