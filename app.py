import base64
import html
import importlib.util
from pathlib import Path
import sys
import urllib.parse

import streamlit as st
from openai import OpenAIError

import artifact_generator


ASSET_DIR = Path(__file__).parent / "assets"


def load_project_module(module_name):
    module_path = Path(__file__).with_name(f"{module_name}.py")
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {module_name} from {module_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


databot = load_project_module("databot")


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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap');

        :root {
            --primary: #2563EB;
            --accent: #14B8A6;
            --ink: #0F172A;
            --muted: #64748B;
            --paper: #F8FAFC;
            --white: #FFFFFF;
            --line: #D8E0EA;
            --line-strong: #CBD5E1;
            --primary-soft: #DBEAFE;
            --accent-soft: #CCFBF1;
        }

        html, body, [class*="css"] {
            font-family: "Inter", sans-serif;
            color: var(--ink);
            font-weight: 400;
        }


        html {
            overflow-x: hidden;
        }

        body,
        .stApp {
            overflow-x: hidden;
        }

        img,
        svg,
        video,
        canvas,
        iframe {
            max-width: 100%;
        }
        *,
        *::before,
        *::after {
            box-sizing: border-box;
        }

        a,
        .project-card,
        .tool-card,
        .platform-logo,
        .callout,
        [data-testid="stMarkdownContainer"] {
            overflow-wrap: anywhere;
            word-break: normal;
        }

        .stApp { background: var(--paper); }
        header[data-testid="stHeader"] { background: rgba(248, 250, 252, .94); }
        [data-testid="stAppViewBlockContainer"],
        [data-testid="stMainBlockContainer"],
        .main .block-container,
        section.main > div {
            max-width: 1180px;
            padding: .9rem 2rem 2.5rem !important;
        }

        [data-testid="stMainBlockContainer"] {
            gap: .65rem !important;
        }h1, h2, h3 {
            font-family: "Poppins", "Inter", sans-serif;
            letter-spacing: 0;
            color: var(--ink);
            font-weight: 700;
        }

        h1 { font-size: clamp(2.2rem, 5vw, 4.7rem); line-height: 1.02; }
        h2 { font-size: clamp(1.7rem, 3vw, 2.6rem); }
        p { line-height: 1.7; color: var(--muted); }

        [data-testid="stNavigation"] {
            border-bottom: 1px solid var(--line);
            background: rgba(255, 255, 255, .96);
        }

        [data-testid="stNavigation"] span {
            color: var(--ink);
            font-family: "Inter", sans-serif;
            font-weight: 600;
        }

        .home-hero-spacer {
            display: block !important;
            height: .45rem !important;
            min-height: .45rem !important;
            line-height: 0 !important;
            font-size: 0 !important;
            visibility: hidden;
        }

        [data-testid="stElementContainer"]:has(.hero) {
            margin-top: .4rem !important;
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
            box-shadow: 0 18px 50px rgba(15, 23, 42, .12);
        }

        .hero::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, rgba(15, 23, 42, .94) 0%, rgba(37, 99, 235, .78) 45%, rgba(20, 184, 166, .12) 78%);
        }

        .hero-copy {
            position: relative;
            z-index: 1;
            max-width: 630px;
            color: white;
        }

        .hero h1 { color: white; margin: .35rem 0 .7rem; }
        .hero p { font-size: 1.08rem; max-width: 650px; color: #EAF2FF; }
        .hero .hero-title {
            color: white;
            display: flex;
            align-items: baseline;
            flex-wrap: wrap;
            font-family: "Poppins", "Inter", sans-serif;
            font-size: clamp(1.1rem, 2.1vw, 1.5rem);
            font-weight: 700;
            gap: .4rem;
            line-height: 1.35;
            margin: 0 0 .7rem;
            min-height: 2em;
        }

        .role-prefix,
        .role-separator {
            color: rgba(255, 255, 255, .92);
        }

        .role-rotator {
            color: var(--accent);
            display: inline-grid;
            min-width: 18ch;
            overflow: hidden;
            position: relative;
            vertical-align: bottom;
        }

        .role-rotator span {
            animation: roleFade 9s ease-in-out infinite;
            grid-area: 1 / 1;
            opacity: 0;
            transform: translateY(.45em);
            white-space: nowrap;
        }

        .role-rotator span:nth-child(2) {
            animation-delay: 3s;
        }

        .role-rotator span:nth-child(3) {
            animation-delay: 6s;
        }

        @keyframes roleFade {
            0%, 8% {
                opacity: 0;
                transform: translateY(.45em);
            }
            12%, 30% {
                opacity: 1;
                transform: translateY(0);
            }
            36%, 100% {
                opacity: 0;
                transform: translateY(-.45em);
            }
        }
        .eyebrow {
            color: var(--accent);
            font-family: "Poppins", "Inter", sans-serif;
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
            font-family: "Poppins", "Inter", sans-serif;
            font-weight: 600;
            text-decoration: none !important;
        }
        .hero-link.primary { background: var(--primary); color: white !important; }
        .hero-link.secondary { border: 1px solid rgba(255,255,255,.7); color: white !important; }

        .section-intro { max-width: 720px; margin: 1.2rem 0 1rem; }
        .section-intro h1,
        .section-intro h2 {
            margin: .35rem 0 .65rem;
        }
        .section-intro p { color: var(--muted); font-size: 1.06rem; }
        .home-about {
            display: grid;
            grid-template-columns: minmax(220px, 320px) 1fr;
            gap: clamp(1.25rem, 4vw, 2.5rem);
            align-items: center;
            background: var(--white);
            border: 1px solid var(--line);
            border-radius: 6px;
            margin: 2rem 0 .75rem;
            padding: clamp(1rem, 3vw, 1.6rem);
            box-shadow: 0 14px 35px rgba(15, 23, 42, .06);
        }

        .profile-frame {
            aspect-ratio: 4 / 5;
            background: linear-gradient(145deg, var(--primary-soft), var(--accent-soft));
            border: 1px solid var(--line-strong);
            border-radius: 6px;
            overflow: hidden;
            position: relative;
        }

        .profile-frame img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }

        .profile-placeholder {
            height: 100%;
            display: grid;
            place-items: center;
            text-align: center;
            padding: 1.2rem;
        }

        .profile-placeholder strong {
            color: var(--ink);
            display: block;
            font-family: "Poppins", "Inter", sans-serif;
            font-size: clamp(2.2rem, 8vw, 4rem);
            line-height: 1;
            margin-bottom: .75rem;
        }

        .profile-placeholder span {
            color: var(--muted);
            display: block;
            font-size: .9rem;
            font-weight: 600;
            line-height: 1.45;
        }

        .home-about-copy h2 {
            margin-top: .35rem;
        }

        .home-about-copy p {
            max-width: 700px;
        }

        .metric-strip {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            margin-top: 1rem;
            border-top: 1px solid var(--line);
            border-bottom: 1px solid var(--line);
            background: rgba(255, 255, 255, .72);
        }
        .metric { padding: 1rem 1.15rem; border-right: 1px solid var(--line); }
        .metric:last-child { border-right: 0; }
        .metric strong {
            display: block;
            font-family: "Poppins", "Inter", sans-serif;
            color: var(--ink);
            font-size: 1.1rem;
            font-weight: 700;
        }
        .metric span { color: var(--muted); font-size: .9rem; }

        .visual-band {
            display: grid;
            grid-template-columns: minmax(0, .92fr) minmax(280px, 1.08fr);
            gap: clamp(1.1rem, 4vw, 2rem);
            align-items: center;
            background: var(--white);
            border: 1px solid var(--line);
            border-radius: 6px;
            margin: 1.35rem 0;
            padding: clamp(1rem, 3vw, 1.55rem);
            box-shadow: 0 14px 35px rgba(15, 23, 42, .06);
        }

        .visual-band.dark {
            background: var(--ink);
        }

        .visual-band.dark h2,
        .visual-band.dark strong {
            color: white;
        }

        .visual-band.dark p {
            color: #E2E8F0;
        }

        .visual-copy h2 {
            margin: .35rem 0 .65rem;
        }

        .visual-copy p {
            margin-bottom: 0;
            max-width: 650px;
        }

        .visual-media {
            border: 1px solid var(--line);
            border-radius: 6px;
            overflow: hidden;
            background: var(--paper);
        }

        .visual-media img {
            display: block;
            width: 100%;
            height: auto;
        }

        .skills-section {
            margin: 1.35rem 0 1.9rem;
        }

        .skills-section .section-intro {
            margin-bottom: 1rem;
        }

        .toolkit-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: .85rem;
        }

        .tool-card {
            align-items: center;
            background: var(--white);
            border: 1px solid var(--line);
            border-radius: 6px;
            display: grid;
            gap: .75rem;
            grid-template-columns: 48px 1fr;
            min-height: 112px;
            padding: .9rem;
            box-shadow: 0 10px 25px rgba(15, 23, 42, .05);
        }

        .tool-icon {
            align-items: center;
            background: var(--primary-soft);
            border: 1px solid #BFDBFE;
            border-radius: 6px;
            color: var(--primary);
            display: inline-flex;
            flex: 0 0 48px;
            font-family: "Poppins", "Inter", sans-serif;
            font-size: .82rem;
            font-weight: 800;
            height: 48px;
            justify-content: center;
            width: 48px;
        }

        .tool-icon svg {
            display: block;
            height: 26px;
            width: 26px;
        }

        .tool-card:nth-child(even) .tool-icon {
            background: var(--accent-soft);
            border-color: #99F6E4;
            color: #0F766E;
        }

        .tool-card strong {
            color: var(--ink);
            display: block;
            font-family: "Poppins", "Inter", sans-serif;
            font-size: .98rem;
            margin-bottom: .25rem;
        }

        .tool-card span {
            color: var(--muted);
            display: block;
            font-size: .84rem;
            line-height: 1.42;
        }

        .social-proof {
            background: var(--white);
            border: 1px solid var(--line);
            border-radius: 6px;
            display: grid;
            gap: 1.1rem;
            grid-template-columns: minmax(0, .9fr) minmax(280px, 1.1fr);
            margin: 1.35rem 0 2rem;
            padding: clamp(1rem, 3vw, 1.45rem);
            box-shadow: 0 14px 35px rgba(15, 23, 42, .06);
        }

        .platform-logos {
            display: grid;
            gap: .65rem;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            margin-top: .95rem;
        }

        .platform-logo {
            align-items: center;
            background: var(--paper);
            border: 1px solid var(--line);
            border-radius: 6px;
            color: var(--ink);
            display: flex;
            gap: .65rem;
            min-height: 58px;
            padding: .72rem .8rem;
        }

        .platform-logo img {
            display: block;
            height: 28px;
            width: 28px;
        }

        .platform-logo strong {
            color: var(--ink);
            display: block;
            font-family: "Poppins", "Inter", sans-serif;
            font-size: .92rem;
        }

        .github-stats-card {
            align-self: stretch;
            background: linear-gradient(135deg, var(--primary-soft), var(--accent-soft));
            border: 1px solid var(--line-strong);
            border-radius: 6px;
            display: grid;
            min-height: 220px;
            overflow: hidden;
            padding: .8rem;
            place-items: center;
        }

        .github-stats-card img {
            background: rgba(255, 255, 255, .78);
            border-radius: 6px;
            display: block;
            height: auto;
            max-width: 100%;
            width: 100%;
        }

        .project-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            margin-top: .25rem;
        }

        .project-card {
            background: var(--white);
            border: 1px solid var(--line);
            border-radius: 6px;
            display: flex;
            flex-direction: column;
            min-height: 100%;
            overflow: hidden;
            box-shadow: 0 14px 35px rgba(15, 23, 42, .06);
            transition: border-color .2s ease, box-shadow .2s ease, transform .2s ease;
        }

        .project-card:hover,
        .project-card:focus-within {
            border-color: rgba(37, 99, 235, .45);
            box-shadow: 0 22px 46px rgba(15, 23, 42, .13);
            transform: translateY(-6px);
        }

        .project-card-media {
            background: var(--paper);
            border-bottom: 1px solid var(--line);
            aspect-ratio: 16 / 10;
            overflow: hidden;
        }

        .project-card-media img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
            transition: transform .24s ease;
        }

        .project-card:hover .project-card-media img,
        .project-card:focus-within .project-card-media img {
            transform: scale(1.035);
        }

        .project-card-body {
            display: flex;
            flex: 1;
            flex-direction: column;
            padding: 1rem;
        }

        .project-card h3 {
            margin: .35rem 0 .55rem;
            font-size: 1.25rem;
        }

        .project-card p {
            font-size: .96rem;
            line-height: 1.58;
            margin-bottom: .85rem;
        }

        .project-card-actions {
            display: flex;
            flex-wrap: wrap;
            gap: .55rem;
            margin-top: auto;
            padding-top: .95rem;
        }

        .project-action {
            border: 1px solid var(--line-strong);
            border-radius: 4px;
            color: var(--ink) !important;
            font-family: "Poppins", "Inter", sans-serif;
            font-size: .84rem;
            font-weight: 600;
            padding: .5rem .68rem;
            text-decoration: none !important;
        }

        .project-action.primary {
            background: var(--primary);
            border-color: var(--primary);
            color: white !important;
        }

        .project-story {
            background: var(--white);
            border: 1px solid var(--line);
            border-radius: 6px;
            margin-top: 1rem;
            padding: clamp(1rem, 3vw, 1.45rem);
            box-shadow: 0 14px 35px rgba(15, 23, 42, .06);
        }

        .project-story-header {
            display: grid;
            gap: .85rem;
            grid-template-columns: minmax(0, 1fr) auto;
            align-items: start;
            border-bottom: 1px solid var(--line);
            margin-bottom: 1rem;
            padding-bottom: .9rem;
        }

        .project-story-header h2 {
            margin: .25rem 0 .45rem;
        }

        .project-story-header p {
            max-width: 760px;
            margin-bottom: 0;
        }

        .project-story-grid {
            display: grid;
            gap: .85rem;
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .story-block {
            background: var(--paper);
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: .9rem;
        }

        .story-block h3 {
            font-size: 1rem;
            margin: .2rem 0 .45rem;
        }

        .story-block p,
        .story-block li {
            color: var(--muted);
            font-size: .92rem;
            line-height: 1.52;
        }

        .story-block ul {
            margin: .35rem 0 0;
            padding-left: 1.05rem;
        }

        .story-block.value {
            background: linear-gradient(135deg, var(--primary-soft), var(--accent-soft));
            border-color: var(--line-strong);
        }

        .story-block.value strong {
            color: var(--ink);
            display: block;
            font-family: "Poppins", "Inter", sans-serif;
            font-size: 1.55rem;
            line-height: 1.1;
            margin-bottom: .25rem;
        }
        .project {
            border-top: 1px solid var(--line);
            padding: 1.35rem 0;
        }
        .project-label {
            color: var(--primary);
            font-family: "Poppins", "Inter", sans-serif;
            font-weight: 700;
            font-size: .82rem;
        }
        .project h3 { margin: .45rem 0 .7rem; }
        .project p { color: var(--muted); max-width: 700px; }
        .tags { display: flex; flex-wrap: wrap; gap: .45rem; margin-top: .7rem; }
        .tag {
            background: var(--primary-soft);
            color: var(--primary);
            border-radius: 3px;
            padding: .3rem .55rem;
            font-size: .78rem;
            font-weight: 600;
        }

        .tag:nth-child(even) {
            background: var(--accent-soft);
            color: #0F766E;
        }

        .callout {
            background: var(--ink);
            color: white;
            padding: clamp(1.2rem, 3vw, 2rem);
            border-radius: 6px;
            margin-top: 2rem;
        }
        .callout h2 { color: white; margin-top: 0; }
        .callout p { color: #E2E8F0; max-width: 680px; }

        [data-testid="stChatMessage"] {
            background: var(--white);
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: .25rem .65rem;
        }

        [data-testid="stChatMessageContent"] {
            overflow-wrap: anywhere;
            word-break: break-word;
        }


        .about-timeline {
            display: grid;
            gap: .75rem;
            margin-top: 1rem;
        }

        .timeline-item {
            background: var(--white);
            border: 1px solid var(--line);
            border-left: 4px solid var(--accent);
            border-radius: 6px;
            padding: .95rem 1rem;
            box-shadow: 0 10px 25px rgba(15, 23, 42, .05);
        }

        .timeline-year {
            color: var(--primary);
            display: block;
            font-family: "Poppins", "Inter", sans-serif;
            font-size: .82rem;
            font-weight: 800;
            margin-bottom: .25rem;
        }

        .timeline-item strong {
            color: var(--ink);
            display: block;
            font-family: "Poppins", "Inter", sans-serif;
            font-size: 1rem;
            margin-bottom: .25rem;
        }

        .timeline-item span:last-child {
            color: var(--muted);
            display: block;
            font-size: .84rem;
            font-weight: 700;
            letter-spacing: .04em;
            text-transform: uppercase;
        }
        .contact-shell {
            display: grid;
            grid-template-columns: minmax(0, .9fr) minmax(280px, 1.1fr);
            gap: 1rem;
            align-items: stretch;
            margin-top: 1.2rem;
        }

        .contact-panel,
        .contact-card {
            background: var(--white);
            border: 1px solid var(--line);
            border-radius: 6px;
            box-shadow: 0 14px 35px rgba(15, 23, 42, .06);
        }

        .contact-panel {
            padding: clamp(1rem, 3vw, 1.45rem);
        }

        .contact-panel h2,
        .contact-card h3 {
            margin: .25rem 0 .55rem;
        }

        .contact-actions {
            display: grid;
            gap: .65rem;
            margin-top: 1rem;
        }

        .contact-link {
            align-items: center;
            background: var(--paper);
            border: 1px solid var(--line);
            border-radius: 6px;
            color: var(--ink) !important;
            display: flex;
            font-family: "Poppins", "Inter", sans-serif;
            font-weight: 700;
            justify-content: space-between;
            padding: .78rem .9rem;
            text-decoration: none !important;
        }

        .contact-link.primary {
            background: var(--primary);
            border-color: var(--primary);
            color: white !important;
        }

        .contact-link span {
            color: inherit;
            font-size: .82rem;
            opacity: .78;
        }

        .contact-card-grid {
            display: grid;
            gap: 1rem;
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .contact-card {
            padding: 1rem;
        }

        .contact-card p {
            font-size: .94rem;
            line-height: 1.55;
            margin-bottom: 0;
        }

        .contact-note {
            background: var(--ink);
            border-radius: 6px;
            color: white;
            margin-top: 1rem;
            padding: 1rem;
        }

        .contact-note strong {
            color: white;
            display: block;
            font-family: "Poppins", "Inter", sans-serif;
            margin-bottom: .35rem;
        }

        .contact-note p {
            color: #E2E8F0;
            margin-bottom: 0;
        }

        .mobile-nav {
            display: none;
        }


        [data-testid="stElementContainer"]:has(.mobile-nav) {
            height: 0 !important;
            margin: 0 !important;
            min-height: 0 !important;
            overflow: hidden !important;
            padding: 0 !important;
        }
        footer { visibility: hidden; }

        @media (max-width: 900px) {
            [data-testid="stAppViewBlockContainer"] {
                padding-top: .65rem;
                padding-left: 1.25rem;
                padding-right: 1.25rem;
            }

            .section-intro {
                margin: 1rem 0 .8rem;
            }
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 0 !important;
            }

            .home-about,
            .visual-band,
            .social-proof {
                grid-template-columns: 1fr;
            }

            .toolkit-grid,
            .project-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .home-hero-spacer {
                height: .5rem !important;
                min-height: .5rem !important;
            }

            [data-testid="stElementContainer"]:has(.hero) {
                margin-top: .35rem !important;
            }
        }

        @media (max-width: 700px) {
            [data-testid="stAppViewBlockContainer"] {
                padding: .25rem .85rem 3.25rem;
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
            [data-testid="stElementContainer"]:has(.mobile-nav) {
                height: auto !important;
                margin: 0 0 .25rem !important;
                min-height: 0 !important;
                overflow: visible !important;
                padding: 0 !important;
            }

            .mobile-nav {
                display: flex;
                gap: .45rem;
                margin: 0 0 .45rem;
                overflow-x: auto;
                padding: 0 0 .35rem;
                scrollbar-width: none;
                -webkit-overflow-scrolling: touch;
            }

            .mobile-nav::-webkit-scrollbar {
                display: none;
            }

            .mobile-nav a {
                flex: 0 0 auto;
                background: var(--primary);
                border: 1px solid var(--primary);
                border-radius: 4px;
                color: white !important;
                font-size: .88rem;
                font-weight: 700;
                line-height: 1;
                padding: .62rem .72rem;
                text-decoration: none !important;
            }

            .hero {
                border-radius: 0;
                min-height: 430px;
                padding: 1rem .95rem;
                align-items: flex-end;
                background-position: 62% center;
                margin-left: -.85rem;
                margin-right: -.85rem;
            }

            .hero::before {
                background: linear-gradient(0deg, rgba(15, 23, 42, .96) 0%, rgba(37, 99, 235, .72) 70%, rgba(20, 184, 166, .18) 100%);
            }

            .hero h1 {
                margin-bottom: .55rem;
            }

            .hero p {
                font-size: .96rem;
                line-height: 1.45;
            }
            .hero .hero-title {
                display: grid;
                gap: .18rem;
                min-height: 3.5em;
            }

            .role-separator {
                display: none;
            }

            .role-rotator {
                min-width: 0;
                width: 100%;
            }

            .role-rotator span {
                white-space: normal;
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

            .home-about {
                grid-template-columns: 1fr;
                gap: .9rem;
                margin: .9rem 0 .45rem;
                padding: .85rem;
            }

            .profile-frame {
                max-width: 240px;
                width: 100%;
            }

            .metric-strip { grid-template-columns: 1fr; }
            .metric {
                border-right: 0;
                border-bottom: 1px solid var(--line);
                padding: .55rem 0;
            }
            .metric:last-child { border-bottom: 0; }

            .visual-band {
                grid-template-columns: 1fr;
                margin: .9rem 0;
                padding: .85rem;
            }

            .skills-section {
                margin: .9rem 0 1rem;
            }

            .toolkit-grid {
                grid-template-columns: 1fr;
                gap: .55rem;
            }

            .tool-card {
                grid-template-columns: 42px 1fr;
                min-height: 88px;
                padding: .75rem;
            }
            .tool-icon {
                height: 42px;
                width: 42px;
            }


            .social-proof {
                grid-template-columns: 1fr;
                margin: .9rem 0 1rem;
                padding: .85rem;
            }

            .platform-logos {
                grid-template-columns: 1fr;
            }

            .github-stats-card {
                min-height: 170px;
                padding: .55rem;
            }

            .project-grid {
                grid-template-columns: 1fr;
            }

            .project-card-body {
                padding: .85rem;
            }


            .project-story {
                margin-top: .75rem;
                padding: .85rem;
            }

            .project-story-header,
            .project-story-grid {
                grid-template-columns: 1fr;
            }

            .project-story-header {
                gap: .55rem;
                margin-bottom: .75rem;
                padding-bottom: .75rem;
            }

            .story-block {
                padding: .8rem;
            }
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



            .about-timeline {
                gap: .55rem;
            }

            .timeline-item {
                padding: .85rem;
            }
            .contact-shell,
            .contact-card-grid {
                grid-template-columns: 1fr;
            }

            .contact-shell {
                gap: .75rem;
                margin-top: .8rem;
            }

            .contact-panel,
            .contact-card,
            .contact-note {
                padding: .85rem;
            }

            .contact-link {
                align-items: flex-start;
                flex-direction: column;
                gap: .25rem;
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
            [data-testid="stTabs"] [role="tablist"] {
                overflow-x: auto;
                scrollbar-width: none;
                white-space: nowrap;
                -webkit-overflow-scrolling: touch;
            }

            [data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar {
                display: none;
            }

            [data-testid="stForm"] {
                overflow-x: hidden;
            }

            [data-testid="stDownloadButton"] button,
            [data-testid="stButton"] button,
            [data-testid="stLinkButton"] a {
                min-height: 42px;
                white-space: normal;
            }

            .project-card-actions {
                display: grid;
                grid-template-columns: 1fr;
                width: 100%;
            }

            .project-action {
                display: block;
                text-align: center;
                width: 100%;
            }

            .story-block ul {
                padding-left: .95rem;
            }
        }

        @media (max-width: 390px) {
            [data-testid="stAppViewBlockContainer"] {
                padding-left: .6rem;
                padding-right: .6rem;
            }

            .mobile-nav a {
                font-size: .8rem;
                padding: .56rem .62rem;
            }

            .hero {
                min-height: 410px;
                padding: .9rem .7rem;
                margin-left: -.6rem;
                margin-right: -.6rem;
            }

            h1 {
                font-size: 1.8rem;
            }

            .platform-logo,
            .tool-card {
                gap: .55rem;
            }

            .github-stats-card {
                min-height: 145px;
            }
            .project-action,
            .contact-link,
            [data-testid="stDownloadButton"] button,
            [data-testid="stButton"] button,
            [data-testid="stLinkButton"] a {
                font-size: .82rem;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: .001ms !important;
                animation-iteration-count: 1 !important;
                scroll-behavior: auto !important;
                transition-duration: .001ms !important;
            }

            .role-rotator span {
                opacity: 0;
                transform: none;
            }

            .role-rotator span:first-child {
                opacity: 1;
            }

            .project-card:hover,
            .project-card:focus-within,
            .project-card:hover .project-card-media img,
            .project-card:focus-within .project-card-media img {
                transform: none;
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
            <a href="/servicebot-project" target="_self">ServiceBot</a>
            <a href="/projects" target="_self">Projects</a>
            <a href="/contact" target="_self">Contact</a>
        </nav>
        """,
        unsafe_allow_html=True,
    )


def image_data_uri(path):
    mime_type = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".svg": "image/svg+xml",
        ".webp": "image/webp",
    }.get(path.suffix.lower(), "image/png")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def profile_photo_markup():
    profile_path = next(
        (
            ASSET_DIR / filename
            for filename in (
                "profile-headshot.png",
                "profile-headshot.jpg",
                "profile-headshot.jpeg",
                "profile-headshot.webp",
            )
            if (ASSET_DIR / filename).exists()
        ),
        None,
    )
    if profile_path:
        profile_image = image_data_uri(profile_path)
        return f'<img src="{profile_image}" alt="Professional headshot of Clinton Njoku">'

    return """
        <div class="profile-placeholder" aria-label="Professional headshot placeholder">
            <div>
                <strong>CN</strong>
                <span>Professional headshot space<br>assets/profile-headshot.png</span>
            </div>
        </div>
    """

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
    hero_image = image_data_uri(ASSET_DIR / "ai-portfolio-hero.png")
    visual_data_ai_workflow = image_data_uri(ASSET_DIR / "visual-data-ai-workflow.svg")
    visual_ai_systems = image_data_uri(ASSET_DIR / "visual-ai-systems.svg")
    st.markdown(
        f"""
        <section class="hero" style="background-image: url('{hero_image}')">
            <div class="hero-copy">
                <div class="eyebrow">Data Science · Prompt Engineering · AI Systems</div>
                <h1>Engr. Clinton Njoku,</h1>
                <div class="hero-title" aria-label="Data Scientist, Prompt Engineer, AI System Builder">
                    <span class="role-prefix">Data Scientist</span>
                    <span class="role-separator">|</span>
                    <span class="role-rotator" aria-hidden="true">
                        <span>Prompt Engineer</span>
                        <span>AI System Builder</span>
                        <span>Data Scientist</span>
                    </span>
                </div>
                <p>I build intelligent data and AI applications that help users analyse information, automate decisions, and interact with data through conversational AI.</p>
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
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <section class="visual-band" aria-label="Data and AI workflow visual">
            <div class="visual-copy">
                <div class="eyebrow">From data to decisions</div>
                <h2>Visual systems for analysis, automation, and AI-assisted insight.</h2>
                <p>The portfolio now connects the work with visual signals: dashboards, model workflows, conversational interfaces, and decision-support systems.</p>
            </div>
            <div class="visual-media"><img src="{visual_data_ai_workflow}" alt="Data visualisation and AI workflow illustration"></div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <section class="home-about" aria-label="About Clinton Njoku">
            <div class="profile-frame">{profile_photo_markup()}</div>
            <div class="home-about-copy">
                <div class="eyebrow">About Me</div>
                <h2>Data and AI work with practical delivery.</h2>
                <p>I design data products, AI assistants, and prompt-driven systems that make analysis easier to understand and easier to act on. This space is prepared for a clear professional headshot so the portfolio feels more personal and credible.</p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <section class="skills-section" aria-label="Skills and tools">
            <div class="section-intro">
                <div class="eyebrow">Skills and tools</div>
                <h2>AI and data stack.</h2>
                <p>A practical toolkit for building, analysing, testing, and deploying intelligent data applications.</p>
            </div>
            <div class="toolkit-grid">
                <div class="tool-card"><div class="tool-icon">Py</div><div><strong>Python</strong><span>Core analysis and application logic.</span></div></div>
                <div class="tool-card"><div class="tool-icon">G4</div><div><strong>GPT-4</strong><span>Advanced reasoning and AI workflows.</span></div></div>
                <div class="tool-card"><div class="tool-icon">OA</div><div><strong>OpenAI</strong><span>Chat, vision, and assistant integrations.</span></div></div>
                <div class="tool-card"><div class="tool-icon">A</div><div><strong>Anthropic</strong><span>LLM evaluation and prompt design awareness.</span></div></div>
                <div class="tool-card"><div class="tool-icon">GH</div><div><strong>GitHub</strong><span>Version control and project delivery.</span></div></div>
                <div class="tool-card"><div class="tool-icon">ST</div><div><strong>Streamlit</strong><span>Interactive data apps and prototypes.</span></div></div>
                <div class="tool-card"><div class="tool-icon">Pd</div><div><strong>Pandas</strong><span>Data cleaning, transformation, and analysis.</span></div></div>
                <div class="tool-card"><div class="tool-icon">Sk</div><div><strong>Scikit-learn</strong><span>Machine learning models and evaluation.</span></div></div>
                <div class="tool-card"><div class="tool-icon">SQL</div><div><strong>SQL</strong><span>Querying, joins, validation, and reporting.</span></div></div>
                <div class="tool-card"><div class="tool-icon">Fl</div><div><strong>Flask</strong><span>Web APIs, chatbot routes, and support tools.</span></div></div>
                <div class="tool-card"><div class="tool-icon">Cx</div><div><strong>Codex</strong><span>AI-assisted development and iteration.</span></div></div>
                <div class="tool-card"><div class="tool-icon">Viz</div><div><strong>Data Visualisation</strong><span>Charts, dashboards, and insight storytelling.</span></div></div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <section class="social-proof" aria-label="Tools, platforms, and GitHub activity">
            <div>
                <div class="eyebrow">Social proof</div>
                <h2>Platforms and ecosystems I build with.</h2>
                <p>My work sits inside the modern AI and data ecosystem, combining model APIs, research platforms, notebooks, repositories, and deployable apps.</p>
                <div class="platform-logos">
                    <div class="platform-logo"><img src="https://cdn.simpleicons.org/openai/0F172A" alt="OpenAI logo"><strong>OpenAI</strong></div>
                    <div class="platform-logo"><img src="https://cdn.simpleicons.org/anthropic/0F172A" alt="Anthropic logo"><strong>Anthropic</strong></div>
                    <div class="platform-logo"><img src="https://cdn.simpleicons.org/huggingface/0F172A" alt="Hugging Face logo"><strong>Hugging Face</strong></div>
                    <div class="platform-logo"><img src="https://cdn.simpleicons.org/kaggle/2563EB" alt="Kaggle logo"><strong>Kaggle</strong></div>
                </div>
            </div>
            <div class="github-stats-card">
                <img src="https://github-readme-stats.vercel.app/api?username=ClintonNjoku2020&show_icons=true&theme=transparent&hide_border=true&title_color=0F172A&text_color=64748B&icon_color=14B8A6&ring_color=2563EB" alt="GitHub activity stats for ClintonNjoku2020">
            </div>
        </section>        <div class="section-intro">
            <div class="eyebrow">Selected work</div>
            <h2>Building at the intersection of data and people</h2>
            <p>My work focuses on approachable tools, reproducible analysis, and machine learning systems designed around real user needs.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    databot_preview = image_data_uri(ASSET_DIR / "project-databot.svg")
    servicebot_preview = image_data_uri(ASSET_DIR / "project-servicebot.svg")
    capstone_preview = image_data_uri(ASSET_DIR / "project-capstone-3.svg")
    st.markdown(
        f"""
        <div class="project-grid">
            <article class="project-card">
                <div class="project-card-media"><img src="{databot_preview}" alt="DataBot app preview"></div>
                <div class="project-card-body">
                    <div class="project-label">01 · AI DATA ASSISTANT</div>
                    <h3>DataBot</h3>
                    <p>A conversational data science assistant for Python, SQL, statistics, model debugging, web research, image review, and report artifact generation.</p>
                    <div class="tags"><span class="tag">Python</span><span class="tag">Streamlit</span><span class="tag">GPT-4o-mini</span><span class="tag">OpenAI API</span><span class="tag">Codex</span></div>
                    <div class="project-card-actions">
                        <a class="project-action primary" href="/databot" target="_self">Live demo</a>
                        <a class="project-action" href="https://github.com/ClintonNjoku2020/databot" target="_blank">GitHub</a>
                    </div>
                </div>
            </article>
            <article class="project-card">
                <div class="project-card-media"><img src="{servicebot_preview}" alt="ServiceBot app preview"></div>
                <div class="project-card-body">
                    <div class="project-label">02 · CUSTOMER SUPPORT AI</div>
                    <h3>ServiceBot</h3>
                    <p>A support chatbot with file uploads, context tracking, frustration detection, call booking, live call links, feedback, and agent escalation handoff pages.</p>
                    <div class="tags"><span class="tag">Python</span><span class="tag">Flask</span><span class="tag">GPT-4o-mini</span><span class="tag">OpenAI API</span><span class="tag">Codex</span></div>
                    <div class="project-card-actions">
                        <a class="project-action primary" href="https://clintonnjoku.com/servicebot/" target="_blank">Live demo</a>
                        <a class="project-action" href="https://github.com/ClintonNjoku2020/servicebot" target="_blank">GitHub</a>
                    </div>
                </div>
            </article>
            <article class="project-card">
                <div class="project-card-media"><img src="{capstone_preview}" alt="Capstone 3 analytics dashboard preview"></div>
                <div class="project-card-body">
                    <div class="project-label">03 · CAPSTONE PROJECT</div>
                    <h3>Capstone 3</h3>
                    <p>An analytics capstone focused on turning customer, revenue, adoption, and churn signals into clear business insight and decision-ready recommendations.</p>
                    <div class="tags"><span class="tag">Python</span><span class="tag">Pandas</span><span class="tag">Streamlit</span><span class="tag">Data Analysis</span><span class="tag">Codex</span></div>
                    <div class="project-card-actions">
                        <a class="project-action primary" href="/projects" target="_self">Live demo</a>
                        <a class="project-action" href="https://github.com/ClintonNjoku2020" target="_blank">GitHub</a>
                    </div>
                </div>
            </article>
        </div>
        <section class="visual-band dark" aria-label="AI systems visual">
            <div class="visual-copy">
                <div class="eyebrow">AI systems</div>
                <h2>Built around prompts, context, workflows, and measurable outputs.</h2>
                <p>Each project shows how data, model reasoning, interface design, and automation fit together in a practical product.</p>
            </div>
            <div class="visual-media"><img src="{visual_ai_systems}" alt="AI technology systems illustration"></div>
        </section>
        <div class="callout">
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
        "Data and AI work grounded in clarity.",
        "I am Clinton Njoku, a data and AI practitioner focused on building practical tools that help people analyse information, automate decisions, and work with conversational AI.",
    )
    st.markdown(
        f"""
        <section class="home-about" aria-label="About Clinton Njoku">
            <div class="profile-frame">{profile_photo_markup()}</div>
            <div class="home-about-copy">
                <div class="eyebrow">Professional profile</div>
                <h2>Engr. Clinton Njoku</h2>
                <p>I build data products, AI assistants, and prompt-driven workflows that turn complex information into clearer decisions. My work combines practical data science, user-focused application design, and modern AI tooling.</p>
                <div class="tags"><span class="tag">Data Scientist</span><span class="tag">Prompt Engineer</span><span class="tag">AI System Builder</span></div>
            </div>
        </section>
        <div class="section-intro">
            <div class="eyebrow">What I build</div>
            <h2>Practical systems for analysis, automation, and AI interaction.</h2>
            <p>I focus on tools that are useful in real workflows, not just technical demonstrations.</p>
        </div>
        <div class="contact-card-grid">
            <article class="contact-card">
                <div class="project-label">01 · DATA PRODUCTS</div>
                <h3>Dashboards and analysis apps</h3>
                <p>Interactive Streamlit tools, visual reports, data cleaning workflows, and decision-support interfaces.</p>
            </article>
            <article class="contact-card">
                <div class="project-label">02 · AI ASSISTANTS</div>
                <h3>Conversational data systems</h3>
                <p>DataBot-style assistants that help users ask better questions, inspect files, and understand outputs.</p>
            </article>
            <article class="contact-card">
                <div class="project-label">03 · PROMPT WORKFLOWS</div>
                <h3>Structured AI reasoning</h3>
                <p>Prompt and system designs for repeatable answers, clearer guardrails, and task-specific model behaviour.</p>
            </article>
            <article class="contact-card">
                <div class="project-label">04 · AUTOMATION</div>
                <h3>Workflow tools</h3>
                <p>Lightweight applications that reduce manual steps and help users move from input to action faster.</p>
            </article>
        </div>
        <section class="visual-band" aria-label="How Clinton works">
            <div class="visual-copy">
                <div class="eyebrow">How I work</div>
                <h2>Simple, reliable, and easy to explain.</h2>
                <p>I start with the real user question, define the data or workflow constraints, then choose the simplest reliable method to deliver the outcome. That means transparent assumptions, clear evaluation, and communication that works for technical and non-technical audiences.</p>
            </div>
            <div class="contact-card-grid">
                <article class="contact-card">
                    <div class="project-label">DISCOVERY</div>
                    <h3>Clarify the problem</h3>
                    <p>Define the question, user need, available data, and success criteria before building.</p>
                </article>
                <article class="contact-card">
                    <div class="project-label">DELIVERY</div>
                    <h3>Build for use</h3>
                    <p>Ship understandable interfaces, tested workflows, and outputs people can act on.</p>
                </article>
            </div>
        </section>
        <section class="skills-section" aria-label="Tools Clinton uses">
            <div class="section-intro">
                <div class="eyebrow">Tools I use</div>
                <h2>AI, data, and application tooling.</h2>
            </div>
            <div class="toolkit-grid">
                <div class="tool-card"><div class="tool-icon">Py</div><div><strong>Python</strong><span>Analysis, automation, and app logic.</span></div></div>
                <div class="tool-card"><div class="tool-icon">OA</div><div><strong>OpenAI</strong><span>LLM workflows and AI assistants.</span></div></div>
                <div class="tool-card"><div class="tool-icon">ST</div><div><strong>Streamlit</strong><span>Interactive data applications.</span></div></div>
                <div class="tool-card"><div class="tool-icon">Pd</div><div><strong>Pandas</strong><span>Data cleaning and transformation.</span></div></div>
                <div class="tool-card"><div class="tool-icon">Sk</div><div><strong>Scikit-learn</strong><span>Machine learning and evaluation.</span></div></div>
                <div class="tool-card"><div class="tool-icon">SQL</div><div><strong>SQL</strong><span>Querying and reporting logic.</span></div></div>
                <div class="tool-card"><div class="tool-icon">GH</div><div><strong>GitHub</strong><span>Version control and delivery.</span></div></div>
                <div class="tool-card"><div class="tool-icon">Cx</div><div><strong>Codex</strong><span>AI-assisted implementation.</span></div></div>
            </div>
        </section>
        <div class="section-intro">
            <div class="eyebrow">Certifications</div>
            <h2>Recent professional credentials.</h2>
        </div>
        <div class="about-timeline" aria-label="Certification timeline">
            <div class="timeline-item"><span class="timeline-year">2025</span><strong>Artificial Intelligence Engineer</strong><span>Artificial Intelligence Board of America</span></div>
            <div class="timeline-item"><span class="timeline-year">2025</span><strong>Certified Data Science Practitioner</strong><span>CertNexus</span></div>
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
    st.markdown(
        """
        <section class="visual-band" aria-label="DataBot modes overview">
            <div class="visual-copy">
                <div class="eyebrow">How to use DataBot</div>
                <h2>Choose the workflow that fits the task.</h2>
                <p>Use Chat when you need data science reasoning, debugging help, file review, image analysis, or source-assisted research. Use Create files when you want downloadable reports, charts, diagrams, or presentations from a short brief.</p>
            </div>
            <div class="contact-card-grid">
                <article class="contact-card">
                    <div class="project-label">CHAT MODE</div>
                    <h3>Ask, upload, analyse</h3>
                    <p>Discuss Python, SQL, statistics, machine learning, files, images, and web sources in one conversational workspace.</p>
                </article>
                <article class="contact-card">
                    <div class="project-label">CREATE FILES</div>
                    <h3>Generate artifacts</h3>
                    <p>Turn a title, brief, key points, and optional CSV into downloadable PDF, SVG, and PowerPoint outputs.</p>
                </article>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
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
        st.markdown(
            """
            <div class="section-intro">
                <div class="eyebrow">Example prompts</div>
                <h2>Start with a focused question.</h2>
                <p>These examples show the kind of structured help DataBot is designed to provide.</p>
            </div>
            <div class="contact-card-grid">
                <article class="contact-card">
                    <div class="project-label">ANALYSIS</div>
                    <h3>Inspect a dataset</h3>
                    <p>Upload a CSV and ask: What patterns, missing values, and outliers should I investigate first?</p>
                </article>
                <article class="contact-card">
                    <div class="project-label">PYTHON</div>
                    <h3>Debug code</h3>
                    <p>Paste a traceback and ask: Explain the error, show the likely cause, and suggest a corrected version.</p>
                </article>
                <article class="contact-card">
                    <div class="project-label">MODELLING</div>
                    <h3>Improve a model</h3>
                    <p>Ask: How should I evaluate this classifier, handle imbalance, and explain the results to stakeholders?</p>
                </article>
                <article class="contact-card">
                    <div class="project-label">RESEARCH</div>
                    <h3>Use sources</h3>
                    <p>Add public URLs and ask: Summarise the evidence, compare claims, and list the sources used.</p>
                </article>
            </div>
            """,
            unsafe_allow_html=True,
        )
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

        with st.expander("Internet research", expanded=False):
            use_web_research = st.checkbox(
                "Fetch internet sources for this question",
                value=False,
                help="DataBot will fetch readable text from the URLs you provide and use it as source context.",
            )
            research_mode = st.selectbox(
                "Analysis type",
                options=["Auto-detect", "Market research", "Sentiment analysis"],
                help="Choose sentiment analysis for public figures, personalities, brands, or companies.",
            )
            research_urls_text = st.text_area(
                "Source URLs",
                placeholder="https://example.com/news\nhttps://example.com/reviews",
                height=92,
                help="Add up to five public web pages, one per line. You can also paste URLs directly into your chat message.",
            )

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        prompt = st.chat_input(
            "Ask a question about your data or a data science topic...",
            accept_file="multiple",
            file_type=["csv", "txt", "md", "json", "py", "sql", "png", "jpg", "jpeg", "webp", "gif"],
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
            image_uploads = [
                uploaded_file
                for uploaded_file in chat_uploaded_files
                if databot.is_supported_image_upload(uploaded_file)
            ]
            text_uploads = [
                uploaded_file
                for uploaded_file in chat_uploaded_files
                if not databot.is_supported_image_upload(uploaded_file)
            ]
            display_input = user_text.strip() or "Uploaded file(s) for DataBot to inspect."
            if chat_file_names:
                display_input = (
                    f"{display_input}\n\n"
                    f"File context: {', '.join(chat_file_names)}"
                )
            if image_uploads:
                display_input = (
                    f"{display_input}\n\n"
                    f"Image analysis enabled for: {', '.join(uploaded_file.name for uploaded_file in image_uploads)}"
                )

            active_file_context = ""
            if text_uploads:
                active_file_context = databot.summarize_uploaded_files(text_uploads)
            model_input = databot.build_user_input_with_file_context(user_text, active_file_context)
            web_sources = []
            direct_answer = None

            source_urls = databot.extract_urls(user_text)
            source_urls.extend(databot.extract_urls(research_urls_text))
            if use_web_research or source_urls:
                source_urls = source_urls[: databot.MAX_WEB_SOURCES]
                if source_urls:
                    with st.spinner("Fetching internet sources..."):
                        web_sources = databot.fetch_web_sources(source_urls)
                    web_context = databot.format_web_research_context(web_sources)
                    analysis_mode = None
                    if research_mode == "Market research":
                        analysis_mode = databot.MARKET_RESEARCH_MODE
                    elif research_mode == "Sentiment analysis":
                        analysis_mode = databot.SENTIMENT_ANALYSIS_MODE
                    selected_analysis_mode = databot.resolve_analysis_mode(
                        analysis_mode,
                        model_input,
                    )
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
                    if (
                        selected_analysis_mode == databot.SENTIMENT_ANALYSIS_MODE
                        and not databot.has_successful_web_sources(web_sources)
                    ):
                        direct_answer = databot.insufficient_sentiment_sources_markdown(web_sources)
                    else:
                        model_input = databot.build_user_input_with_web_context(
                            model_input,
                            web_context,
                            analysis_mode=selected_analysis_mode,
                        )
                elif use_web_research:
                    display_input = (
                        f"{display_input}\n\n"
                        "Internet research was enabled, but no source URLs were provided."
                    )
            model_message_content = databot.build_user_message_content(model_input, image_uploads)

            st.session_state.messages.append({"role": "user", "content": display_input})
            with st.chat_message("user"):
                st.write(display_input)

            with st.chat_message("assistant"):
                with st.spinner("Working on your question..."):
                    api_key = databot.get_api_key()
                    if direct_answer:
                        answer = direct_answer
                    elif not api_key:
                        answer = "DataBot is not configured yet. Add OPENAI_API_KEY to the app secrets."
                    else:
                        try:
                            answer, st.session_state.conversation_history = databot.get_databot_reply(
                                client=databot.create_client(api_key),
                                model=databot.get_vision_model() if image_uploads else databot.get_model(),
                                conversation_history=st.session_state.conversation_history,
                                user_input=model_message_content,
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
        st.markdown(
            """
            <div class="section-intro">
                <div class="eyebrow">Create files</div>
                <h2>Generate polished outputs from a brief.</h2>
                <p>Use this mode when you need a concise report package rather than a conversational answer.</p>
            </div>
            <div class="contact-card-grid">
                <article class="contact-card">
                    <div class="project-label">INPUT</div>
                    <h3>Brief plus key points</h3>
                    <p>Provide the title, the purpose of the report, and the main points you want the files to communicate.</p>
                </article>
                <article class="contact-card">
                    <div class="project-label">OUTPUT</div>
                    <h3>Downloadable artifacts</h3>
                    <p>DataBot creates a PDF summary, chart SVG, diagram SVG, and PowerPoint file for local download.</p>
                </article>
            </div>
            """,
            unsafe_allow_html=True,
        )
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


def servicebot_page():
    page_heading(
        "ServiceBot",
        "AI support workflow assistant.",
        "A customer-support chatbot project designed around fast answers, escalation handling, feedback collection, and clear user handoff paths.",
    )
    servicebot_preview = image_data_uri(ASSET_DIR / "project-servicebot.svg")
    st.markdown(
        f"""
        <section class="visual-band" aria-label="ServiceBot project overview">
            <div class="visual-copy">
                <div class="eyebrow">Customer support AI</div>
                <h2>ServiceBot helps users move from question to resolution.</h2>
                <p>It combines conversational support, uploaded context, frustration detection, call booking, live call links, feedback capture, and escalation pages into one service workflow.</p>
                <div class="project-card-actions">
                    <a class="project-action primary" href="https://clintonnjoku.com/servicebot/" target="_blank">Open ServiceBot app</a>
                    <a class="project-action" href="https://github.com/ClintonNjoku2020/servicebot" target="_blank">View GitHub</a>
                </div>
            </div>
            <div class="visual-media"><img src="{servicebot_preview}" alt="ServiceBot app preview"></div>
        </section>
        <div class="contact-card-grid">
            <article class="contact-card">
                <div class="project-label">01 · CONVERSATION</div>
                <h3>Context-aware support</h3>
                <p>Keeps the support flow focused while helping users describe problems, attach files, and get useful next steps.</p>
            </article>
            <article class="contact-card">
                <div class="project-label">02 · ESCALATION</div>
                <h3>Human handoff paths</h3>
                <p>Detects frustration signals and provides structured escalation options, including booking and live-call flows.</p>
            </article>
            <article class="contact-card">
                <div class="project-label">03 · FEEDBACK</div>
                <h3>Service quality loop</h3>
                <p>Captures feedback so the support experience can be reviewed, improved, and connected to real service outcomes.</p>
            </article>
            <article class="contact-card">
                <div class="project-label">04 · STACK</div>
                <h3>Python AI tooling</h3>
                <p>Built with Python, Flask, GPT-4o-mini, OpenAI API workflows, prompt engineering, and Codex-assisted iteration.</p>
            </article>
        </div>
        <div class="callout">
            <h2>Try the live support flow.</h2>
            <p>Open the live ServiceBot app to try the customer-support workflow in the deployed Flask interface.</p>
            <a class="hero-link primary" href="https://clintonnjoku.com/servicebot/" target="_blank">Open ServiceBot app</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

def projects():
    page_heading(
        "Projects",
        "Selected AI and data projects.",
        "Each project is framed around the problem, solution, stack, key features, technical decisions, and practical value delivered.",
    )
    databot_preview = image_data_uri(ASSET_DIR / "project-databot.svg")
    servicebot_preview = image_data_uri(ASSET_DIR / "project-servicebot.svg")
    capstone_preview = image_data_uri(ASSET_DIR / "project-capstone-3.svg")
    st.markdown(
        f"""
        <div class="project-grid">
            <article class="project-card">
                <div class="project-card-media"><img src="{databot_preview}" alt="DataBot app preview"></div>
                <div class="project-card-body">
                    <div class="project-label">01 · AI DATA ASSISTANT</div>
                    <h3>DataBot</h3>
                    <p>A conversational data science assistant for file context, web research, image review, and artifact generation.</p>
                    <div class="tags"><span class="tag">Python</span><span class="tag">Streamlit</span><span class="tag">GPT-4o-mini</span><span class="tag">OpenAI API</span><span class="tag">Codex</span></div>
                    <div class="project-card-actions"><a class="project-action primary" href="/databot" target="_self">Live demo</a><a class="project-action" href="https://github.com/ClintonNjoku2020/databot" target="_blank">GitHub</a></div>
                </div>
            </article>
            <article class="project-card">
                <div class="project-card-media"><img src="{servicebot_preview}" alt="ServiceBot app preview"></div>
                <div class="project-card-body">
                    <div class="project-label">02 · CUSTOMER SUPPORT AI</div>
                    <h3>ServiceBot</h3>
                    <p>A support chatbot workflow for context tracking, uploads, escalation bundles, call booking, feedback, and agent review.</p>
                    <div class="tags"><span class="tag">Python</span><span class="tag">Flask</span><span class="tag">GPT-4o-mini</span><span class="tag">OpenAI API</span><span class="tag">Codex</span></div>
                    <div class="project-card-actions"><a class="project-action primary" href="https://clintonnjoku.com/servicebot/" target="_blank">Live demo</a><a class="project-action" href="https://github.com/ClintonNjoku2020/servicebot" target="_blank">GitHub</a></div>
                </div>
            </article>
            <article class="project-card">
                <div class="project-card-media"><img src="{capstone_preview}" alt="Capstone 3 analytics dashboard preview"></div>
                <div class="project-card-body">
                    <div class="project-label">03 · CAPSTONE ANALYTICS</div>
                    <h3>Capstone 3</h3>
                    <p>An analytics capstone for turning customer, revenue, adoption, and churn signals into recommendations.</p>
                    <div class="tags"><span class="tag">Python</span><span class="tag">Pandas</span><span class="tag">Scikit-learn</span><span class="tag">Streamlit</span><span class="tag">Analysis</span></div>
                    <div class="project-card-actions"><a class="project-action primary" href="/projects" target="_self">View details</a><a class="project-action" href="https://github.com/ClintonNjoku2020" target="_blank">GitHub</a></div>
                </div>
            </article>
        </div>

        <section class="project-story" aria-label="DataBot detailed project story">
            <div class="project-story-header"><div><div class="project-label">01 · DATABOT</div><h2>Data science help inside a conversational workspace.</h2><p>DataBot supports users who need help interpreting datasets, debugging code, checking sources, reviewing visuals, and turning analysis into shareable outputs.</p></div><div class="project-card-actions"><a class="project-action primary" href="/databot" target="_self">Live demo</a><a class="project-action" href="https://github.com/ClintonNjoku2020/databot" target="_blank">GitHub</a></div></div>
            <div class="project-story-grid">
                <div class="story-block"><h3>Problem</h3><p>Data learners and practitioners often switch between chat, notebooks, search, file viewers, image inspection, and report tools to solve one analysis task.</p></div>
                <div class="story-block"><h3>Solution</h3><p>A Streamlit chatbot that combines data science reasoning, uploaded file context, optional web research, image analysis, and artifact generation in one interface.</p></div>
                <div class="story-block"><h3>Key features</h3><ul><li>File upload support for CSV, text, code, SQL, JSON, and markdown.</li><li>Web research with URL extraction and source references.</li><li>Image analysis for screenshots, charts, diagrams, and visual debugging.</li><li>Artifact generation for PDF, SVG chart, SVG diagram, and PowerPoint outputs.</li></ul></div>
                <div class="story-block"><h3>Technical decisions</h3><ul><li>Streamlit provides fast interaction and deployment.</li><li>Session state preserves conversation continuity.</li><li>Vision or text models are selected based on uploaded content.</li><li>Downloads are generated locally through a separate artifact module.</li></ul></div>
                <div class="story-block"><h3>Stack</h3><p>Python, Streamlit, OpenAI API, GPT-4o-mini, prompt engineering, file parsing, image input handling, artifact generation, Codex.</p></div>
                <div class="story-block value"><h3>Measurable value</h3><strong>4 output formats</strong><p>Users can move from question to chat answer, PDF summary, chart SVG, diagram SVG, and PowerPoint deliverable.</p></div>
            </div>
        </section>

        <section class="project-story" aria-label="ServiceBot detailed project story">
            <div class="project-story-header"><div><div class="project-label">02 · SERVICEBOT</div><h2>Support automation with human handoff built in.</h2><p>ServiceBot focuses on customer-support moments where users need quick help, preserved context, and a clean escalation path when automation is not enough.</p></div><div class="project-card-actions"><a class="project-action primary" href="https://clintonnjoku.com/servicebot/" target="_blank">Live demo</a><a class="project-action" href="https://github.com/ClintonNjoku2020/servicebot" target="_blank">GitHub</a></div></div>
            <div class="project-story-grid">
                <div class="story-block"><h3>Problem</h3><p>Support users often repeat context, provide evidence separately, and struggle to reach a human agent with enough background for resolution.</p></div>
                <div class="story-block"><h3>Solution</h3><p>A Flask-based AI support flow that tracks support context, handles uploads, detects frustration, and prepares escalation bundles for agent review.</p></div>
                <div class="story-block"><h3>Key features</h3><ul><li>Support context tracking across the conversation.</li><li>Upload handling for customer files and issue evidence.</li><li>Escalation bundles for structured handoff.</li><li>Call booking and live-call link support.</li><li>Feedback collection after support interactions.</li><li>Agent review pages for escalated cases.</li></ul></div>
                <div class="story-block"><h3>Technical decisions</h3><ul><li>Flask supports a lightweight multi-route workflow.</li><li>Escalation state is separated from the customer chat path.</li><li>Feedback and agent review surfaces make the support loop inspectable.</li><li>Prompt instructions focus responses on resolution and escalation readiness.</li></ul></div>
                <div class="story-block"><h3>Stack</h3><p>Python, Flask, OpenAI API, GPT-4o-mini, prompt engineering, upload handling, support workflow routing, Codex.</p></div>
                <div class="story-block value"><h3>Measurable value</h3><strong>6 support capabilities</strong><p>Context tracking, upload handling, escalation bundles, call booking, feedback, and agent review reduce friction between chatbot support and human follow-up.</p></div>
            </div>
        </section>

        <section class="project-story" aria-label="Capstone 3 detailed project story">
            <div class="project-story-header"><div><div class="project-label">03 · CAPSTONE 3</div><h2>Business analytics shaped for decision-making.</h2><p>Capstone 3 presents analysis work as a decision-support story: define the business question, transform the data, identify patterns, and communicate action.</p></div><div class="project-card-actions"><a class="project-action primary" href="/projects" target="_self">View details</a><a class="project-action" href="https://github.com/ClintonNjoku2020" target="_blank">GitHub</a></div></div>
            <div class="project-story-grid">
                <div class="story-block"><h3>Problem</h3><p>Business datasets can contain churn, revenue, customer, and adoption signals, but value is lost when insights are not tied to decisions.</p></div>
                <div class="story-block"><h3>Solution</h3><p>An analytics workflow that profiles data, surfaces patterns, visualises key signals, and turns findings into recommendations.</p></div>
                <div class="story-block"><h3>Key features</h3><ul><li>Data preparation and validation workflow.</li><li>Exploratory analysis of customer, revenue, adoption, and churn signals.</li><li>Visual storytelling through charts and dashboard-style summaries.</li><li>Recommendation-focused reporting for stakeholders.</li></ul></div>
                <div class="story-block"><h3>Technical decisions</h3><ul><li>Pandas supports transparent data cleaning and transformation.</li><li>Scikit-learn supports model-ready analysis patterns.</li><li>Streamlit makes insights interactive and easy to review.</li><li>Visual summaries keep the project understandable for non-technical readers.</li></ul></div>
                <div class="story-block"><h3>Stack</h3><p>Python, Pandas, Scikit-learn, Streamlit, data visualisation, exploratory analysis, reporting, Codex.</p></div>
                <div class="story-block value"><h3>Measurable value</h3><strong>4 insight areas</strong><p>Customer, revenue, adoption, and churn analysis provide a clear structure for explaining risk and opportunity.</p></div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

def contact():
    page_heading(
        "Contact",
        "Let's build something useful.",
        "Reach out for data science, prompt engineering, AI assistant, automation, dashboard, or collaboration projects.",
    )
    contact_email = "clinton.njoku@gmail.com"
    linkedin_url = "https://www.linkedin.com/in/clinton-njoku-6775752b4/"
    github_url = "https://github.com/ClintonNjoku2020"
    st.markdown(
        f"""
        <section class="contact-shell" aria-label="Contact options">
            <div class="contact-panel">
                <div class="eyebrow">Contact channels</div>
                <h2>Start with the project context.</h2>
                <p>Share the problem, the data or workflow involved, and the outcome you want users to get from the solution.</p>
                <div class="contact-actions">
                    <a class="contact-link primary" href="mailto:{contact_email}">Email <span>{contact_email}</span></a>
                    <a class="contact-link" href="{linkedin_url}" target="_blank">LinkedIn <span>Clinton Njoku</span></a>
                    <a class="contact-link" href="{github_url}" target="_blank">GitHub <span>ClintonNjoku2020</span></a>
                    <a class="contact-link" href="https://github.com/ClintonNjoku2020/databot" target="_blank">DataBot repository <span>AI data assistant project</span></a>
                </div>
                <div class="contact-note">
                    <strong>Best-fit enquiries</strong>
                    <p>Data analysis apps, AI assistants, prompt workflows, dashboards, automation tools, and product prototypes.</p>
                </div>
            </div>
            <div class="contact-card-grid">
                <article class="contact-card">
                    <div class="project-label">01 · DATA PRODUCTS</div>
                    <h3>Dashboards and analysis tools</h3>
                    <p>Interactive Streamlit apps, data workflows, exploratory analysis, reporting, and decision-support interfaces.</p>
                </article>
                <article class="contact-card">
                    <div class="project-label">02 · AI ASSISTANTS</div>
                    <h3>Conversational AI systems</h3>
                    <p>DataBot-style assistants, prompt design, retrieval-aware workflows, guardrails, and user-facing AI experiences.</p>
                </article>
                <article class="contact-card">
                    <div class="project-label">03 · AUTOMATION</div>
                    <h3>Workflow improvement</h3>
                    <p>Tools that reduce manual steps, structure repeatable decisions, and connect users to clearer information.</p>
                </article>
                <article class="contact-card">
                    <div class="project-label">04 · COLLABORATION</div>
                    <h3>Technical project support</h3>
                    <p>Capstone projects, prototypes, portfolio systems, and practical implementation help across Python and AI tooling.</p>
                </article>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-intro">
            <div class="eyebrow">Let's Connect</div>
            <h2>Prefer a direct channel?</h2>
            <p>I am open to data science, prompt engineering, AI assistant, and automation opportunities. You can connect through LinkedIn, GitHub, or email.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    quick_link_cols = st.columns(3)
    with quick_link_cols[0]:
        st.link_button("LinkedIn", linkedin_url, icon=":material/link:", use_container_width=True)
    with quick_link_cols[1]:
        st.link_button("GitHub", github_url, icon=":material/code:", use_container_width=True)
    with quick_link_cols[2]:
        st.link_button("Email", f"mailto:{contact_email}", icon=":material/mail:", use_container_width=True)

    st.markdown(
        """
        <div class="section-intro">
            <div class="eyebrow">Inquiry form</div>
            <h2>Prepare a project email.</h2>
            <p>This form creates an email draft in your mail app. It does not store submissions on the website.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.form("contact_inquiry_form"):
        inquiry_name = st.text_input("Name")
        inquiry_email = st.text_input("Email")
        inquiry_type = st.selectbox(
            "Project type",
            [
                "Data science project",
                "AI assistant",
                "Prompt engineering",
                "Dashboard or Streamlit app",
                "Automation workflow",
                "Collaboration",
            ],
        )
        inquiry_message = st.text_area(
            "Project details",
            placeholder="Briefly describe the problem, available data or workflow, timeline, and desired outcome.",
            height=140,
        )
        submitted = st.form_submit_button("Create email draft", icon=":material/mail:")

    if submitted:
        if not inquiry_name.strip() or not inquiry_email.strip() or not inquiry_message.strip():
            st.warning("Please add your name, email, and project details before creating the email draft.")
        else:
            subject = f"Portfolio inquiry: {inquiry_type}"
            body = (
                f"Name: {inquiry_name.strip()}\n"
                f"Email: {inquiry_email.strip()}\n"
                f"Project type: {inquiry_type}\n\n"
                f"Project details:\n{inquiry_message.strip()}"
            )
            mailto_url = "mailto:" + contact_email + "?" + urllib.parse.urlencode(
                {"subject": subject, "body": body}
            )
            st.success("Your email draft is ready.")
            st.markdown(
                f'<a class="contact-link primary" href="{html.escape(mailto_url, quote=True)}">Open email draft <span>{contact_email}</span></a>',
                unsafe_allow_html=True,
            )

load_css()
mobile_navigation()

pages = {
    "Portfolio": [
        st.Page(home, title="Home", icon=":material/home:", url_path="", default=True),
        st.Page(about, title="About Me", icon=":material/person:", url_path="about"),
        st.Page(databot_page, title="DataBot", icon=":material/smart_toy:", url_path="databot"),
        st.Page(servicebot_page, title="ServiceBot", icon=":material/support_agent:", url_path="servicebot-project"),
        st.Page(projects, title="Projects", icon=":material/work:", url_path="projects"),
        st.Page(contact, title="Contact", icon=":material/mail:", url_path="contact"),
    ]
}

navigation = st.navigation(pages, position="top")
navigation.run()
