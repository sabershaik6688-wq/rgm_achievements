import streamlit as st
import pandas as pd
import sqlite3
import os
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DATS - Department Achievement Tracking System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LUXURY EXECUTIVE LIGHT/DARK BALANCED STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* FIX FOR LABELS IN FORMS */
    .stTextInput label, .stSelectbox label, .stTextArea label, .stFileUploader label, [data-testid="stForm"] label, [data-testid="stTextInput"] label {
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    
    /* ADAPTIVE INPUT TEXT COLOR (DARK IN LIGHT THEME / WHITE IN DARK THEME) */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] span {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    
    @media (prefers-color-scheme: dark) {
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] span {
            color: #ffffff !important;
        }
    }
    
    /* FIX FOR SIDEBAR TEXT & RADIO BUTTONS */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .hero-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 2.5rem 3rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.15), 0 10px 10px -5px rgba(15, 23, 42, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-title {
        font-size: 2.25rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.025em;
        color: #ffffff;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #cbd5e1;
        margin: 0;
        font-weight: 400;
    }
    
    .metric-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
        border: 1px solid #e2e8f0;
        text-align: center;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 20px -3px rgba(37, 99, 235, 0.1);
        border-color: #3b82f6;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 0.25rem;
    }
    .metric-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    
    div[data-testid="stForm"] {
        background: #ffffff;
        padding: 2.5rem;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.03);
    }
    
    .stButton button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border-radius: 10px;
        font-weight: 700;
        padding: 0.65rem 1.75rem;
        border: none;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE & DIRECTORY INITIALIZATION ---
def init_db():
    os.makedirs("uploads", exist_ok=True)
    conn = sqlite3.connect('dats.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            author_name TEXT NOT NULL,
            academic_year TEXT NOT NULL,
            description TEXT,
            file_path TEXT,
            file_name TEXT
        )
    ''')
    # Safe migration for existing databases
    try:
        cursor.execute("ALTER TABLE achievements ADD COLUMN file_path TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE achievements ADD COLUMN file_name TEXT")
    except sqlite3.OperationalError:
        pass
        
    conn.commit()
    conn.close()

init_db()

def get_all_records():
    conn = sqlite3.connect('dats.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM achievements")
    records = cursor.fetchall()
    conn.close()
    return records

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color: #ffffff; padding-top: 1rem; font-weight: 800;'>🎓 DATS Portal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.85rem; margin-bottom: 2rem;'>Department Achievement Tracking System</p>", unsafe_allow_html=True)
    
    menu = st.radio(
        "Navigation Menu", 
        ["📊 Executive Dashboard", "➕ Add Achievement", "🔍 Filter & Export", "⚙️ Manage Records"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br><br><hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.75rem; line-height: 1.4;'><b>RGMCET - ECE Department</b><br>Autonomous | Estd-1905<br>Project Version 2.0</p>", unsafe_allow_html=True)

categories = ["Publication", "Research Grant", "Award", "Presentation", "Student Achievement"]

# --- VIEW 1: EXECUTIVE DASHBOARD ---
if menu == "📊 Executive Dashboard":
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">Department Executive Dashboard</h1>
            <p class="hero-subtitle">Real-time overview of faculty and student productivity metrics, accreditations, and research milestones.</p>
        </div>
    """, unsafe_allow_html=True)
    
    records = get_all_records()
    total_records = len(records)
    df_metrics = pd.DataFrame(records, columns=["ID", "Title", "Category", "Author", "Year", "Description", "FilePath", "FileName"]) if records else pd.DataFrame(columns=["ID", "Title", "Category", "Author", "Year", "Description", "FilePath", "FileName"])
    
    # Row 1 Metrics (3 columns)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_records}</div>
                <div class="metric-label">Total Achievements</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        pub_count = len(df_metrics[df_metrics['Category'] == 'Publication']) if not df_metrics.empty else 0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{pub_count}</div>
                <div class="metric-label">Publications</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        grant_count = len(df_metrics[df_metrics['Category'] == 'Research Grant']) if not df_metrics.empty else 0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{grant_count}</div>
                <div class="metric-label">Research Grants</div>
            </div>
        """, unsafe_allow_html=True)

    # Row 2 Metrics (3 columns)
    col4, col5, col6 = st.columns(3)
    with col4:
        award_count = len(df_metrics[df_metrics['Category'] == 'Award']) if not df_metrics.empty else 0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{award_count}</div>
                <div class="metric-label">Awards Won</div>
            </div>
        """, unsafe_allow_html=True)
    with col5:
        presentation_count = len(df_metrics[df_metrics['Category'] == 'Presentation']) if not df_metrics.empty else 0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{presentation_count}</div>
                <div class="metric-label">Presentations</div>
            </div>
        """, unsafe_allow_html=True)
    with col6:
        student_count = len(df_metrics[df_metrics['Category'] == 'Student Achievement']) if not df_metrics.empty else 0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{student_count}</div>
                <div class="metric-label">Student Achievements</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if not df_metrics.empty:
        st.subheader("📌 Recent Department Records & Certificates")
        
        display_df = df_metrics[["ID", "Title", "Category", "Author", "Year", "FileName"]].copy()
        display_df.columns = ["ID", "Title", "Category", "Author", "Academic Year", "Attached Document"]
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # --- OPEN & VIEW ATTACHED FILES SECTION ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📂 Open & View Attached Files / Certificates")
        selected_record_id = st.selectbox("Select Record ID to Open/View Document", df_metrics["ID"].tolist(), key="dash_open_doc")
        row = df_metrics[df_metrics["ID"] == selected_record_id].iloc[0]
        
        # Safe extraction of path and name avoiding float/NoneType crashes
        f_path = str(row["FilePath"]) if pd.notna(row["FilePath"]) else None
        f_name = str(row["FileName"]) if pd.notna(row["FileName"]) else None
        
        if f_path and f_name and f_path != "None" and os.path.exists(f_path):
            st.info(f"Viewing document for record: **{row['Title']}** ({f_name})")
            
            # Check file extension to render appropriately
            ext = f_name.lower().split('.')[-1]
            if ext in ['png', 'jpg', 'jpeg']:
                st.image(f_path, caption=f_name, use_container_width=True)
            elif ext == 'pdf':
                with open(f_path, "rb") as pdf_file:
                    PDFbyte = pdf_file.read()
                st.download_button(label="📥 Open / Download PDF File", data=PDFbyte, file_name=f_name, mime='application/pdf')
            else:
                with open(f_path, "rb") as file_to_dl:
                    st.download_button(
                        label=f"⬇️ Download & Open Document: {f_name}",
                        data=file_to_dl,
                        file_name=f_name,
                        mime="application/octet-stream"
                    )
        else:
            st.info("No document attached to this specific record.")
    else:
        st.info("💡 No records logged in the database yet. Click 'Add Achievement' in the sidebar to start recording data.")

# --- VIEW 2: ADD ACHIEVEMENT ---
elif menu == "➕ Add Achievement":
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">Add Department Achievement</h1>
            <p class="hero-subtitle">Record new faculty publications, research grants, awards, and upload certificates securely.</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("achievement_form_aesthetic"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Achievement Title*", placeholder="e.g., Deep Learning in IoT Networks")
            category = st.selectbox("Category*", categories)
            author_name = st.text_input("Author / Faculty / Student Name*", placeholder="e.g., Dr. R. Hanuma Naik")
        with col2:
            academic_year = st.text_input("Academic Year*", placeholder="e.g., 2025-2026")
            description = st.text_area("Brief Description / Summary", placeholder="Enter key highlights, grant value, or publisher details...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Certificate / Report Document (PDF, Image, DOCX)", type=["pdf", "png", "jpg", "jpeg", "docx"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="🚀 Save Achievement & Document")
        
        if submit_button:
            if title and author_name and academic_year:
                file_path = None
                file_name = None
                
                if uploaded_file is not None:
                    file_name = uploaded_file.name
                    unique_prefix = str(int(time.time()))
                    saved_filename = f"{unique_prefix}_{file_name}"
                    file_path = os.path.join("uploads", saved_filename)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                conn = sqlite3.connect('dats.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO achievements (title, category, author_name, academic_year, description, file_path, file_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (title, category, author_name, academic_year, description, file_path, file_name))
                conn.commit()
                conn.close()
                st.success("✨ Achievement and certificate successfully recorded and saved in the system!")
            else:
                st.error("⚠️ Please fill in all required (*) fields before submission.")

# --- VIEW 3: FILTER & EXPORT ---
elif menu == "🔍 Filter & Export":
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">Query & Export Reports</h1>
            <p class="hero-subtitle">Filter departmental records by academic year and category, and view or download associated certificates.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        search_year = st.text_input("Filter by Academic Year (e.g., 2025-2026)")
    with col2:
        selected_category = st.selectbox("Filter by Category", ["All Categories"] + categories)
    
    if st.button("🔍 Generate Query Report"):
        conn = sqlite3.connect('dats.db')
        query = "SELECT * FROM achievements WHERE 1=1"
        params = []
        
        if search_year:
            query += " AND academic_year = ?"
            params.append(search_year)
        if selected_category != "All Categories":
            query += " AND category = ?"
            params.append(selected_category)
            
        cursor = conn.cursor()
        cursor.execute(query, params)
        records = cursor.fetchall()
        conn.close()
        
        if records:
            st.success(f"Found **{len(records)}** matching record(s).")
            df = pd.DataFrame(records, columns=["ID", "Title", "Category", "Author/Name", "Academic Year", "Description", "FilePath", "FileName"])
            
            # Display clean table
            display_df = df[["ID", "Title", "Category", "Author/Name", "Academic Year", "FileName"]].copy()
            display_df.columns = ["ID", "Title", "Category", "Author/Name", "Academic Year", "Attached Certificate"]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Download filtered CSV report
            csv_df = df[["ID", "Title", "Category", "Author/Name", "Academic Year", "Description", "FileName"]]
            csv_data = csv_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Structured CSV Report",
                data=csv_data,
                file_name="department_achievements_report.csv",
                mime="text/csv",
            )
            
            st.markdown("---")
            st.subheader("📂 Open & View Certificate / Report")
            rec_choices = {f"ID {r[0]}: {r[1]} ({r[3]})": r[0] for r in records}
            chosen_rec_key = st.selectbox("Select Record to Open/View Certificate", list(rec_choices.keys()), key="filter_open_doc")
            chosen_id = rec_choices[chosen_rec_key]
            
            matched_row = df[df["ID"] == chosen_id].iloc[0]
            dl_path = str(matched_row["FilePath"]) if pd.notna(matched_row["FilePath"]) else None
            dl_name = str(matched_row["FileName"]) if pd.notna(matched_row["FileName"]) else None
            
            if dl_path and dl_name and dl_path != "None" and os.path.exists(dl_path):
                st.info(f"Viewing document for: **{matched_row['Title']}** ({dl_name})")
                ext = dl_name.lower().split('.')[-1]
                if ext in ['png', 'jpg', 'jpeg']:
                    st.image(dl_path, caption=dl_name, use_container_width=True)
                else:
                    with open(dl_path, "rb") as f_dl:
                        st.download_button(
                            label=f"⬇️ Download & Open File: {dl_name}",
                            data=f_dl,
                            file_name=dl_name,
                            mime="application/octet-stream"
                        )
            else:
                st.info("No certificate document uploaded for this selected record.")
        else:
            st.info("No records found matching your specified filters.")

# --- VIEW 4: MANAGE & DELETE ---
elif menu == "⚙️ Manage Records":
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">Manage & Delete Records</h1>
            <p class="hero-subtitle">Review active database entries, check attached files, and securely remove obsolete records.</p>
        </div>
    """, unsafe_allow_html=True)
    
    conn = sqlite3.connect('dats.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, category, academic_year, author_name, file_path, file_name FROM achievements")
    all_records = cursor.fetchall()
    conn.close()
    
    if all_records:
        df_summary = pd.DataFrame(all_records, columns=["ID", "Title", "Category", "Academic Year", "Author", "FilePath", "FileName"])
        display_summary = df_summary[["ID", "Title", "Category", "Academic Year", "Author", "FileName"]]
        display_summary.columns = ["ID", "Title", "Category", "Academic Year", "Author", "Attached Document"]
        st.dataframe(display_summary, use_container_width=True, hide_index=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            delete_id_input = st.text_input("Enter Record ID to Delete", placeholder="e.g., 1")
            
            if st.button("🗑️ Delete Selected Record", type="primary"):
                if delete_id_input.strip().isdigit():
                    target_id = int(delete_id_input.strip())
                    conn = sqlite3.connect('dats.db')
                    cursor = conn.cursor()
                    
                    # Check if ID exists and remove physical file if exists
                    cursor.execute("SELECT file_path FROM achievements WHERE id = ?", (target_id,))
                    row_data = cursor.fetchone()
                    
                    if row_data:
                        f_path = str(row_data[0]) if row_data[0] is not None else None
                        if f_path and f_path != "None" and os.path.exists(f_path):
                            try:
                                os.remove(f_path)
                            except Exception:
                                pass
                                
                        # 1. Delete the record
                        cursor.execute("DELETE FROM achievements WHERE id = ?", (target_id,))
                        conn.commit()
                        
                        # 2. Re-sequence / Reset IDs for remaining records sequentially (1, 2, 3...)
                        cursor.execute("SELECT title, category, author_name, academic_year, description, file_path, file_name FROM achievements")
                        remaining_rows = cursor.fetchall()
                        
                        cursor.execute("DROP TABLE achievements")
                        cursor.execute('''
                            CREATE TABLE achievements (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                category TEXT NOT NULL,
                                author_name TEXT NOT NULL,
                                academic_year TEXT NOT NULL,
                                description TEXT,
                                file_path TEXT,
                                file_name TEXT
                            )
                        ''')
                        
                        for row in remaining_rows:
                            cursor.execute('''
                                INSERT INTO achievements (title, category, author_name, academic_year, description, file_path, file_name)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', row)
                            
                        conn.commit()
                        conn.close()
                        st.success(f"Record ID {target_id} deleted & IDs successfully re-sequenced! Refreshing view...")
                        st.rerun()
                    else:
                        conn.close()
                        st.error(f"⚠️ Record ID {target_id} does not exist in the database.")
                else:
                    st.error("⚠️ Please enter a valid numeric Record ID.")
    else:
        st.info("Database is currently empty. No records available to manage.")