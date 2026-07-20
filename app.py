import base64
import html
from pathlib import Path

import streamlit as st
from openai import OpenAIError

import artifact_generator
import databot


ASSET_DIR = Path(__file__).parent / "assets"


st.set_page_config(
    page_title="Clinton Njoku | Data & AI Portfolio",
    page_icon="CN",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def load_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

        :root {
            --ink: #15211d;
            --muted: #5e6b66;
            --paper: #f7f8f5;
            --white: #ffffff;
            --green: #176b4d;
            --green-dark: #0e4c37;
            --amber: #d89a32;
            --line: #dfe5e1;
        }

        html, body, [class*="css"] {
            font-family: "DM Sans", sans-serif;
            color: var(--ink);
        }

        .stApp { background: var(--paper); }
        header[data-testid="stHeader"] { background: rgba(247, 248, 245, .92); }
        [data-testid="stAppViewBlockContainer"] {
            max-width: 1180px;
            padding: 1.15rem 2rem 2.5rem;
        }

        h1, h2, h3 {
            font-family: "Manrope", sans-serif;
            letter-spacing: 0;
            color: var(--ink);
        }

        h1 { font-size: clamp(2.2rem, 5vw, 4.7rem); line-height: 1.02; }
        h2 { font-size: clamp(1.7rem, 3vw, 2.6rem); }
        p { line-height: 1.7; }

        [data-testid="stNavigation"] {
            border-bottom: 1px solid var(--line);
            background: rgba(247, 248, 245, .96);
        }

        [data-testid="stNavigation"] span { font-weight: 600; }

        .home-hero-spacer {
            display: block !important;
            height: 3rem !important;
            min-height: 3rem !important;
            line-height: 0 !important;
            font-size: 0 !important;
            visibility: hidden;
        }

        [data-testid="stElementContainer"]:has(.hero) {
            margin-top: 1.25rem !important;
        }

        .hero {
            min-height: min(560px, 68vh);
            display: flex;
            align-items: center;
            padding: clamp(1.6rem, 5vw, 3.5rem);
            border-radius: 6px;
            background-size: cover;
            background-position: center;
            position: relative;
            overflow: hidden;
        }

        .hero::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, rgba(10, 20, 16, .93) 0%, rgba(10, 20, 16, .78) 42%, rgba(10, 20, 16, .06) 74%);
        }

        .hero-copy {
            position: relative;
            z-index: 1;
            max-width: 630px;
            color: white;
        }

        .hero h1 { color: white; margin: .35rem 0 .8rem; }
        .hero p { font-size: 1.12rem; max-width: 570px; color: #edf2ef; }
        .eyebrow {
            color: #d9b66f;
            font-size: .78rem;
            font-weight: 700;
            letter-spacing: .12em;
            text-transform: uppercase;
        }

        .hero-actions { display: flex; gap: .75rem; margin-top: 1.15rem; flex-wrap: wrap; }
        .hero-link {
            display: inline-block;
            padding: .72rem 1.05rem;
            border-radius: 4px;
            font-weight: 700;
            text-decoration: none !important;
        }
        .hero-link.primary { background: #f4b84e; color: #172019 !important; }
        .hero-link.secondary { border: 1px solid rgba(255,255,255,.65); color: white !important; }

        .section-intro { max-width: 720px; margin: 2.25rem 0 1.25rem; }
        .section-intro h1,
        .section-intro h2 {
            margin: .35rem 0 .65rem;
        }
        .section-intro p { color: var(--muted); font-size: 1.06rem; }

        .metric-strip {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            margin-top: 1rem;
            border-top: 1px solid var(--line);
            border-bottom: 1px solid var(--line);
        }
        .metric { padding: 1rem 1.15rem; border-right: 1px solid var(--line); }
        .metric:last-child { border-right: 0; }
        .metric strong { display: block; font-family: "Manrope"; font-size: 1.1rem; }
        .metric span { color: var(--muted); font-size: .9rem; }

        .project {
            border-top: 1px solid var(--line);
            padding: 1.35rem 0;
        }
        .project-label { color: var(--green); font-weight: 700; font-size: .82rem; }
        .project h3 { margin: .45rem 0 .7rem; }
        .project p { color: var(--muted); max-width: 700px; }
        .tags { display: flex; flex-wrap: wrap; gap: .45rem; margin-top: .7rem; }
        .tag {
            background: #e8efeb;
            color: #294b3d;
            border-radius: 3px;
            padding: .3rem .55rem;
            font-size: .78rem;
            font-weight: 600;
        }

        .callout {
            background: var(--green-dark);
            color: white;
            padding: clamp(1.2rem, 3vw, 2rem);
            border-radius: 6px;
            margin-top: 2rem;
        }
        .callout h2 { color: white; margin-top: 0; }
        .callout p { color: #dceae4; max-width: 680px; }

        [data-testid="stChatMessage"] {
            background: white;
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: .25rem .65rem;
        }

        [data-testid="stChatMessageContent"] {
            overflow-wrap: anywhere;
            word-break: break-word;
        }

        .contact-link {
            display: block;
            color: var(--green) !important;
            font-weight: 700;
            margin: .7rem 0;
        }

        .mobile-nav {
            display: none;
        }

        footer { visibility: hidden; }

        @media (max-width: 900px) {
            [data-testid="stAppViewBlockContainer"] {
                padding-left: 1.25rem;
                padding-right: 1.25rem;
            }

            .section-intro {
                margin: 1.8rem 0 1rem;
            }

            .home-hero-spacer {
                height: 4.25rem !important;
                min-height: 4.25rem !important;
            }

            [data-testid="stElementContainer"]:has(.hero) {
                margin-top: 2rem !important;
            }
        }

        @media (max-width: 700px) {
            [data-testid="stAppViewBlockContainer"] {
                padding: .35rem .85rem 3.25rem;
            }

            [data-testid="stVerticalBlock"] {
                gap: .45rem;
            }

            [data-testid="stHorizontalBlock"] {
                gap: .65rem;
            }

            [data-testid="stElementContainer"] {
                margin-bottom: .25rem;
            }

            [data-testid="stMarkdownContainer"] p {
                margin-bottom: .55rem;
            }

            h1 {
                font-size: clamp(1.85rem, 11vw, 2.55rem);
                line-height: 1.08;
                margin-bottom: .45rem;
            }

            h2 {
                font-size: 1.35rem;
                line-height: 1.18;
                margin-bottom: .45rem;
            }

            h3 {
                line-height: 1.22;
                margin-bottom: .35rem;
            }

            p {
                line-height: 1.48;
            }

            [data-testid="stNavigation"] {
                display: none;
            }

            .mobile-nav {
                display: flex;
                gap: .45rem;
                margin: 0 0 2.25rem;
                overflow-x: auto;
                padding: 0 0 .45rem;
                scrollbar-width: none;
                -webkit-overflow-scrolling: touch;
            }

            .mobile-nav::-webkit-scrollbar {
                display: none;
            }

            .mobile-nav a {
                flex: 0 0 auto;
                background: var(--green);
                border: 1px solid var(--green);
                border-radius: 4px;
                color: white !important;
                font-size: .88rem;
                font-weight: 700;
                line-height: 1;
                padding: .62rem .72rem;
                text-decoration: none !important;
            }

            .hero {
                min-height: 310px;
                padding: .9rem .85rem;
                align-items: flex-end;
                background-position: 62% center;
            }

            .hero::before {
                background: linear-gradient(0deg, rgba(10,20,16,.96) 0%, rgba(10,20,16,.72) 70%, rgba(10,20,16,.2) 100%);
            }

            .hero h1 {
                margin-bottom: .55rem;
            }

            .hero p {
                font-size: .96rem;
                line-height: 1.45;
            }

            .hero-actions {
                display: grid;
                grid-template-columns: 1fr;
                gap: .45rem;
                margin-top: .65rem;
            }

            .hero-link {
                width: 100%;
                text-align: center;
                padding: .65rem .8rem;
            }

            .section-intro {
                margin: .9rem 0 .45rem;
            }

            .section-intro h1,
            .section-intro h2 {
                margin: .25rem 0 .4rem;
            }

            .section-intro p {
                font-size: .96rem;
            }

            .metric-strip { grid-template-columns: 1fr; }
            .metric {
                border-right: 0;
                border-bottom: 1px solid var(--line);
                padding: .55rem 0;
            }
            .metric:last-child { border-bottom: 0; }

            .project {
                padding: .7rem 0;
            }

            .tags {
                gap: .3rem;
                margin-top: .45rem;
            }

            .tag {
                font-size: .74rem;
                padding: .28rem .45rem;
            }

            .callout {
                padding: .85rem;
                margin-top: .7rem;
            }

            .callout p {
                margin-bottom: .6rem;
            }

            [data-testid="stAlert"] {
                padding: .65rem .8rem;
            }

            [data-testid="stChatMessage"] {
                padding: .15rem .45rem;
            }

            [data-testid="stChatMessage"] p,
            [data-testid="stMarkdownContainer"] li {
                font-size: .96rem;
            }

            [data-testid="stChatInput"] {
                left: .75rem;
                right: .75rem;
                width: auto;
            }
        }

        @media (max-width: 390px) {
            [data-testid="stAppViewBlockContainer"] {
                padding-left: .65rem;
                padding-right: .65rem;
            }

            .hero {
                min-height: 290px;
                padding: .8rem .75rem;
            }

            h1 {
                font-size: 1.8rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def mobile_navigation():
    st.markdown(
        """
        <nav class="mobile-nav" aria-label="Mobile navigation">
            <a href="/" target="_self">Home</a>
            <a href="/about" target="_self">About</a>
            <a class="primary" href="/databot" target="_self">DataBot</a>
            <a href="/projects" target="_self">Projects</a>
            <a href="/contact" target="_self">Contact</a>
        </nav>
        """,
        unsafe_allow_html=True,
    )


def image_data_uri(path):
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def page_heading(kicker, title, description):
    st.markdown(
        f"""
        <div class="section-intro">
            <div class="eyebrow">{html.escape(kicker)}</div>
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(description)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def home():
    hero_image = image_data_uri(ASSET_DIR / "data-workspace-hero.png")
    st.markdown(
        '<div class="home-hero-spacer" aria-hidden="true" style="height: 56px; min-height: 56px;">&nbsp;</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <section class="hero" style="background-image: url('{hero_image}')">
            <div class="hero-copy">
                <div class="eyebrow">Data Science · Machine Learning · AI</div>
                <h1>Clinton Njoku</h1>
                <p>I build practical data products that turn complex questions into clear, useful answers.</p>
                <div class="hero-actions">
                    <a class="hero-link primary" href="/databot" target="_self">Try DataBot</a>
                    <a class="hero-link secondary" href="/projects" target="_self">View projects</a>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="metric-strip">
            <div class="metric"><strong>End-to-end thinking</strong><span>From problem framing to deployment</span></div>
            <div class="metric"><strong>Clear communication</strong><span>Technical work made understandable</span></div>
            <div class="metric"><strong>Responsible AI</strong><span>Useful, scoped, and transparent outputs</span></div>
        </div>
        <div class="section-intro">
            <div class="eyebrow">Selected work</div>
            <h2>Building at the intersection of data and people</h2>
            <p>My work focuses on approachable tools, reproducible analysis, and machine learning systems designed around real user needs.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns([1.4, 1], gap="medium")
    with col1:
        st.markdown(
            """
            <div class="project">
                <div class="project-label">FEATURED PROJECT</div>
                <h3>DataBot</h3>
                <p>An AI assistant for data science questions, debugging, statistics, Python, SQL, and machine learning workflows.</p>
                <div class="tags"><span class="tag">Python</span><span class="tag">OpenAI API</span><span class="tag">Streamlit</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="callout" style="margin-top:0">
                <h2>Have a data problem?</h2>
                <p>Explore the portfolio or start a conversation about a project, collaboration, or technical challenge.</p>
                <a class="hero-link primary" href="/contact" target="_self">Get in touch</a>
            </div>
            """,
            unsafe_allow_html=True,
        )


def about():
    page_heading(
        "About me",
        "Data work grounded in clarity.",
        "I am Clinton Njoku, a data and AI practitioner focused on creating practical tools that help people understand information and make better decisions.",
    )
    left, right = st.columns([1.35, 1], gap="medium")
    with left:
        st.subheader("How I work")
        st.write(
            "I approach projects by defining the real question first, then selecting the simplest reliable method to answer it. "
            "That means careful data preparation, transparent assumptions, meaningful evaluation, and communication that serves both technical and non-technical audiences."
        )
        st.subheader("Current focus")
        st.write(
            "My current work combines Python, machine learning, prompt engineering, APIs, and lightweight web deployment. "
            "DataBot is one example: a focused assistant designed to make data science support more structured and accessible."
        )
    with right:
        st.markdown(
            """
            <div class="callout" style="margin-top:0">
                <div class="eyebrow">Capabilities</div>
                <h2>What I bring</h2>
                <p>Data analysis and preparation<br>
                Machine learning workflows<br>
                Python and SQL<br>
                AI application development<br>
                Prompt and system design<br>
                Clear technical communication</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def databot_page():
    page_heading(
        "AI assistant",
        "Meet DataBot.",
        "Ask focused questions or generate professional PDFs, charts, diagrams, and PowerPoint presentations from a brief or dataset.",
    )
    st.warning(
        "Do not upload or paste confidential, personal, or sensitive data. "
        "DataBot is for educational and data science support purposes."
    )

    chat_tab, artifact_tab = st.tabs(["Chat", "Create files"])

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I am DataBot. Ask me any data science question.",
            }
        ]
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = databot.create_conversation_history()

    with chat_tab:
        toolbar_left, toolbar_right = st.columns([4, 1])
        with toolbar_left:
            st.caption("DataBot may make mistakes. Verify important technical decisions.")
        with toolbar_right:
            if st.button("Clear chat", icon=":material/delete_sweep:", use_container_width=True):
                st.session_state.messages = [
                    {"role": "assistant", "content": "Chat cleared. What would you like to explore?"}
                ]
                st.session_state.conversation_history = databot.create_conversation_history()
                st.rerun()

        with st.expander("Internet market research", expanded=False):
            use_web_research = st.checkbox(
                "Fetch internet sources for this question",
                value=False,
                help="DataBot will fetch readable text from the URLs you provide and use it as source context.",
            )
            research_urls_text = st.text_area(
                "Source URLs",
                placeholder="https://example.com/report\nhttps://example.com/competitor",
                height=92,
                help="Add up to five public web pages, one per line. You can also paste URLs directly into your chat message.",
            )

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        prompt = st.chat_input(
            "Ask a question about your data or a data science topic...",
            accept_file="multiple",
            file_type=["csv", "txt", "md", "json", "py", "sql"],
        )
        if prompt:
            if isinstance(prompt, str):
                user_text = prompt
                chat_uploaded_files = []
            else:
                user_text = prompt.text or ""
                chat_uploaded_files = prompt.files or []

            if not user_text.strip() and not chat_uploaded_files:
                return

            chat_file_names = [uploaded_file.name for uploaded_file in chat_uploaded_files]
            display_input = user_text.strip() or "Uploaded file(s) for DataBot to inspect."
            if chat_file_names:
                display_input = (
                    f"{display_input}\n\n"
                    f"File context: {', '.join(chat_file_names)}"
                )

            active_file_context = ""
            if chat_uploaded_files:
                active_file_context = databot.summarize_uploaded_files(chat_uploaded_files)
            model_input = databot.build_user_input_with_file_context(user_text, active_file_context)
            web_sources = []

            source_urls = databot.extract_urls(user_text)
            source_urls.extend(databot.extract_urls(research_urls_text))
            if use_web_research or source_urls:
                source_urls = source_urls[: databot.MAX_WEB_SOURCES]
                if source_urls:
                    with st.spinner("Fetching internet sources..."):
                        web_sources = databot.fetch_web_sources(source_urls)
                    web_context = databot.format_web_research_context(web_sources)
                    model_input = databot.build_user_input_with_web_context(model_input, web_context)
                    successful_sources = [
                        source.get("final_url") or source.get("url")
                        for source in web_sources
                        if not source.get("error")
                    ]
                    failed_sources = [
                        source.get("url")
                        for source in web_sources
                        if source.get("error")
                    ]
                    if successful_sources:
                        display_input = (
                            f"{display_input}\n\n"
                            f"Internet sources: {', '.join(successful_sources)}"
                        )
                    if failed_sources:
                        display_input = (
                            f"{display_input}\n\n"
                            f"Sources not fetched: {', '.join(failed_sources)}"
                        )
                elif use_web_research:
                    display_input = (
                        f"{display_input}\n\n"
                        "Internet research was enabled, but no source URLs were provided."
                    )

            st.session_state.messages.append({"role": "user", "content": display_input})
            with st.chat_message("user"):
                st.write(display_input)

            with st.chat_message("assistant"):
                with st.spinner("Working on your question..."):
                    api_key = databot.get_api_key()
                    if not api_key:
                        answer = "DataBot is not configured yet. Add OPENAI_API_KEY to the app secrets."
                    else:
                        try:
                            answer, st.session_state.conversation_history = databot.get_databot_reply(
                                client=databot.create_client(api_key),
                                model=databot.get_model(),
                                conversation_history=st.session_state.conversation_history,
                                user_input=model_input,
                            )
                            source_references = databot.source_references_markdown(web_sources)
                            if source_references and "Sources used:" not in answer:
                                answer = f"{answer.rstrip()}\n\n{source_references}"
                            else:
                                unavailable_sources = databot.unavailable_sources_markdown(web_sources)
                                if unavailable_sources and "Sources unavailable:" not in answer:
                                    answer = f"{answer.rstrip()}\n\n{unavailable_sources}"
                        except OpenAIError as error:
                            answer = databot.format_openai_error(error)
                    st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

    with artifact_tab:
        st.caption("Create downloadable files locally from your brief. CSV uploads are used to populate chart values.")
        with st.form("artifact_form"):
            artifact_title = st.text_input("Title", value="Data Analysis Summary")
            artifact_brief = st.text_area(
                "Brief",
                value="Summarize the analysis, highlight the key findings, and recommend next steps.",
                height=95,
            )
            artifact_points = st.text_area(
                "Key points",
                value=(
                    "Clean and profile the dataset\n"
                    "Identify the strongest patterns\n"
                    "Explain business impact\n"
                    "Recommend measurable next steps"
                ),
                height=130,
            )
            artifact_csv = st.file_uploader(
                "Optional CSV for chart data",
                type=["csv"],
                help="DataBot will infer the first usable numeric column for the chart.",
            )
            submitted = st.form_submit_button("Generate files", icon=":material/description:")

        if submitted:
            csv_bytes = artifact_csv.getvalue() if artifact_csv else None
            st.session_state.generated_artifacts = artifact_generator.generate_artifacts(
                artifact_title,
                artifact_brief,
                artifact_points,
                csv_bytes,
            )
            st.session_state.generated_artifact_title = artifact_title

        if "generated_artifacts" in st.session_state:
            artifacts = st.session_state.generated_artifacts
            title = st.session_state.get("generated_artifact_title", "DataBot artifact")
            st.success("Files are ready.")
            preview_left, preview_right = st.columns(2, gap="medium")
            with preview_left:
                st.subheader("Chart")
                st.image(artifacts["chart_svg"].decode("utf-8"))
            with preview_right:
                st.subheader("Diagram")
                st.image(artifacts["diagram_svg"].decode("utf-8"))

            pdf_name = artifact_generator.safe_filename(title, "pdf")
            chart_name = artifact_generator.safe_filename(title + " chart", "svg")
            diagram_name = artifact_generator.safe_filename(title + " diagram", "svg")
            pptx_name = artifact_generator.safe_filename(title, "pptx")
            download_cols = st.columns(4)
            with download_cols[0]:
                st.download_button(
                    "PDF",
                    artifacts["pdf"],
                    file_name=pdf_name,
                    mime="application/pdf",
                    icon=":material/picture_as_pdf:",
                    use_container_width=True,
                )
            with download_cols[1]:
                st.download_button(
                    "Chart",
                    artifacts["chart_svg"],
                    file_name=chart_name,
                    mime="image/svg+xml",
                    icon=":material/bar_chart:",
                    use_container_width=True,
                )
            with download_cols[2]:
                st.download_button(
                    "Diagram",
                    artifacts["diagram_svg"],
                    file_name=diagram_name,
                    mime="image/svg+xml",
                    icon=":material/account_tree:",
                    use_container_width=True,
                )
            with download_cols[3]:
                st.download_button(
                    "PowerPoint",
                    artifacts["pptx"],
                    file_name=pptx_name,
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    icon=":material/slideshow:",
                    use_container_width=True,
                )


def projects():
    page_heading(
        "Projects",
        "Selected work.",
        "A growing collection of practical data and AI projects, designed to solve clear problems and communicate results effectively.",
    )
    st.markdown(
        """
        <article class="project">
            <div class="project-label">01 · AI APPLICATION</div>
            <h2>DataBot</h2>
            <p>A deployed conversational assistant dedicated to data science. DataBot maintains conversation context, handles API failures clearly, and uses a structured system prompt to deliver useful explanations, diagnoses, and code guidance.</p>
            <div class="tags">
                <span class="tag">Python</span><span class="tag">Streamlit</span>
                <span class="tag">OpenAI API</span><span class="tag">Prompt Engineering</span>
                <span class="tag">GitHub</span>
            </div>
        </article>
        <article class="project">
            <div class="project-label">02 · WEB DEVELOPMENT</div>
            <h2>Data & AI Portfolio</h2>
            <p>A responsive, multi-page portfolio built with Streamlit to present technical work and provide direct access to an interactive AI product from one deployment.</p>
            <div class="tags">
                <span class="tag">Streamlit</span><span class="tag">Responsive UI</span>
                <span class="tag">Cloud Deployment</span>
            </div>
        </article>
        """,
        unsafe_allow_html=True,
    )


def contact():
    page_heading(
        "Contact",
        "Let’s discuss the work.",
        "For project enquiries, collaborations, or questions about DataBot, connect with me through GitHub.",
    )
    details, next_step = st.columns([1, 1.35], gap="medium")
    with details:
        st.subheader("Connect")
        st.markdown(
            """
            <a class="contact-link" href="https://github.com/ClintonNjoku2020" target="_blank">GitHub · ClintonNjoku2020 ↗</a>
            <a class="contact-link" href="https://github.com/ClintonNjoku2020/databot" target="_blank">DataBot repository ↗</a>
            """,
            unsafe_allow_html=True,
        )
    with next_step:
        st.markdown(
            """
            <div class="callout" style="margin-top:0">
                <div class="eyebrow">Start a conversation</div>
                <h2>Project or collaboration?</h2>
                <p>Visit my GitHub profile to review my work, follow current development, or open a discussion on the DataBot repository.</p>
                <a class="hero-link primary" href="https://github.com/ClintonNjoku2020" target="_blank">Open GitHub ↗</a>
            </div>
            """,
            unsafe_allow_html=True,
        )


load_css()
mobile_navigation()

pages = {
    "Portfolio": [
        st.Page(home, title="Home", icon=":material/home:", url_path="", default=True),
        st.Page(about, title="About Me", icon=":material/person:", url_path="about"),
        st.Page(databot_page, title="DataBot", icon=":material/smart_toy:", url_path="databot"),
        st.Page(projects, title="Projects", icon=":material/work:", url_path="projects"),
        st.Page(contact, title="Contact", icon=":material/mail:", url_path="contact"),
    ]
}

navigation = st.navigation(pages, position="top")
navigation.run()
