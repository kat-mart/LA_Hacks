import streamlit as st

def show_landing_page():
    st.markdown("""
    <div style="text-align:center; margin-top:2.5rem; margin-bottom:3rem;">
        <span style="
            font-family:'Lato',serif;
            font-size:1.25rem;
            font-weight:700;
            letter-spacing:0.12em;
            text-transform:uppercase;
            color:var(--text-muted, #b09a80);
        ">Prompt<span style="color:var(--accent,#c8813a);">2</span>Project</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        # Hero heading
        st.markdown("""
        <div style="
            text-align:center;
            font-family:'Playfair Display',serif;
            font-size:3.4rem; font-weight:600;
            color:var(--text-primary,#3b2f1e);
            line-height:1.2; margin-bottom:1rem;
        ">From idea to <em style="color:var(--accent,#c8813a);">action</em>,<br>in minutes.</div>
        """, unsafe_allow_html=True)

        # Subheading
        st.markdown("""
        <p style="
            text-align:center; font-size:1rem;
            color:var(--text-secondary,#7a6650);
            line-height:1.75; margin-bottom:2rem;
        ">
            Describe your team, set your constraints, and let AI suggest the right project
            and break it into tasks your team can actually work towards.
        </p>
        """, unsafe_allow_html=True)

        # CTA button
        if st.button("Get Started →", type="primary", use_container_width=True):
            st.switch_page(st.session_state.page_1)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="height:1px;background:linear-gradient(to right,transparent,var(--border,#e0d4bb),transparent);margin:1.5rem 0;"></div>', unsafe_allow_html=True)

        # How it works — 3 steps
        st.markdown("""
        <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:0.85rem; margin-bottom:2rem;">
            <div style="
                background:var(--bg-card,#fff9f0);
                border:1.5px solid var(--border-soft,#ede4d0);
                border-radius:14px; padding:1rem; text-align:center;
                box-shadow:0 2px 8px rgba(100,70,30,0.08);
            ">
                <div style="font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:600;color:var(--accent,#c8813a);">01</div>
                <div style="font-size:0.78rem;font-weight:700;letter-spacing:0.05em;text-transform:uppercase;color:var(--text-secondary,#7a6650);margin:0.3rem 0;">Build your team</div>
                <div style="font-size:0.82rem;color:var(--text-muted,#b09a80);line-height:1.5;">Add members and map out everyone's skills.</div>
            </div>
            <div style="
                background:var(--bg-card,#fff9f0);
                border:1.5px solid var(--border-soft,#ede4d0);
                border-radius:14px; padding:1rem; text-align:center;
                box-shadow:0 2px 8px rgba(100,70,30,0.08);
            ">
                <div style="font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:600;color:var(--accent,#c8813a);">02</div>
                <div style="font-size:0.78rem;font-weight:700;letter-spacing:0.05em;text-transform:uppercase;color:var(--text-secondary,#7a6650);margin:0.3rem 0;">Get ideas</div>
                <div style="font-size:0.82rem;color:var(--text-muted,#b09a80);line-height:1.5;">AI suggests projects for your timeline and difficulty.</div>
            </div>
            <div style="
                background:var(--bg-card,#fff9f0);
                border:1.5px solid var(--border-soft,#ede4d0);
                border-radius:14px; padding:1rem; text-align:center;
                box-shadow:0 2px 8px rgba(100,70,30,0.08);
            ">
                <div style="font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:600;color:var(--accent,#c8813a);">03</div>
                <div style="font-size:0.78rem;font-weight:700;letter-spacing:0.05em;text-transform:uppercase;color:var(--text-secondary,#7a6650);margin:0.3rem 0;">Start working</div>
                <div style="font-size:0.82rem;color:var(--text-muted,#b09a80);line-height:1.5;">Tasks auto-assigned. Track everyone's progress live.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quote strip
        st.markdown("""
        <div style="
            background:var(--accent-soft,#f0d9bc);
            border:1.5px dashed var(--border,#e0d4bb);
            border-radius:14px; padding:1.2rem 1.5rem; text-align:center;
            margin-bottom:2rem;
        ">
            <p style="
                font-family:'Playfair Display',serif; font-style:italic;
                font-size:1rem; color:var(--text-primary,#3b2f1e); line-height:1.6;
            ">"Stop deliberating, start delivering"</p>
            <small style="
                display:block; margin-top:0.4rem;
                font-size:0.75rem; letter-spacing:0.05em; text-transform:uppercase;
                color:var(--text-muted,#b09a80);
            ">Prompt2Project — built for builders</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)