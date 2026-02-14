#!/usr/bin/env python3
"""
CFP Idea Generator - Streamlit App
Generate novel talk/workshop/speech ideas for conferences.
"""

import random
from dataclasses import dataclass
from typing import Optional

import streamlit as st


# Conference database with tracks
CONFERENCES = {
    "PyCon US": {
        "tracks": [
            "Python Language",
            "Web Development",
            "Data Science & ML",
            "DevOps & Infrastructure",
            "Testing & Quality",
            "Community & Education",
            "Security",
        ],
        "formats": ["talk", "tutorial", "lightning", "poster"],
    },
    "KubeCon": {
        "tracks": [
            "Application Development",
            "CI/CD & GitOps",
            "Customization & Extensibility",
            "Observability",
            "Operations & Performance",
            "Platform Engineering",
            "Security & Identity",
            "Serverless & Edge",
        ],
        "formats": ["talk", "tutorial", "lightning"],
    },
    "AWS re:Invent": {
        "tracks": [
            "Architecture",
            "Compute",
            "Containers",
            "Data & Analytics",
            "Databases",
            "DevOps",
            "Machine Learning",
            "Networking",
            "Security",
            "Serverless",
        ],
        "formats": ["talk", "workshop", "chalk talk"],
    },
    "Google Cloud Next": {
        "tracks": [
            "AI & Machine Learning",
            "Application Development",
            "Data Analytics",
            "Infrastructure & Operations",
            "Security",
            "Collaboration & Productivity",
        ],
        "formats": ["talk", "workshop", "lightning"],
    },
    "Strange Loop": {
        "tracks": [
            "Programming Languages",
            "Distributed Systems",
            "Databases",
            "Security",
            "Developer Experience",
            "Emerging Technology",
        ],
        "formats": ["talk", "lightning"],
    },
    "DjangoCon": {
        "tracks": [
            "Django Internals",
            "Web Development",
            "APIs & Services",
            "Testing & Debugging",
            "Deployment & DevOps",
            "Community & Career",
        ],
        "formats": ["talk", "tutorial", "lightning"],
    },
    "ReactConf": {
        "tracks": [
            "React Core",
            "State Management",
            "Performance",
            "Testing",
            "React Native",
            "Tooling & DX",
        ],
        "formats": ["talk", "lightning"],
    },
    "DockerCon": {
        "tracks": [
            "Container Fundamentals",
            "Docker Compose & Swarm",
            "CI/CD Pipelines",
            "Security & Compliance",
            "Developer Workflows",
            "Production Best Practices",
        ],
        "formats": ["talk", "workshop", "lightning"],
    },
    "Other / Custom": {
        "tracks": [],
        "formats": ["talk", "workshop", "lightning"],
    },
}


@dataclass
class UserProfile:
    """User's profile for generating relevant CFP ideas."""

    name: str
    expertise_areas: list[str]
    recent_projects: list[str]
    interests: list[str]
    target_audience: str
    conference_name: Optional[str] = None
    conference_track: Optional[str] = None
    talk_format: str = "talk"


# Idea generation templates
ANGLES = [
    "lessons learned from",
    "the unexpected benefits of",
    "common mistakes in",
    "a beginner's journey into",
    "scaling challenges with",
    "the future of",
    "demystifying",
    "beyond the basics of",
    "real-world applications of",
    "the hidden complexity of",
    "rethinking",
    "what nobody tells you about",
    "a deep dive into",
    "practical tips for",
    "the evolution of",
]

FORMATS = {
    "talk": [
        "A {duration}-minute exploration of {topic}",
        "Case study: {topic}",
        "From zero to hero: {topic}",
        "{topic}: A practitioner's perspective",
        "The art and science of {topic}",
    ],
    "workshop": [
        "Hands-on {topic}: Build your first {artifact}",
        "Workshop: Mastering {topic} in 90 minutes",
        "Interactive session: {topic} for teams",
        "From theory to practice: {topic} workshop",
        "Build, break, learn: {topic}",
    ],
    "tutorial": [
        "Tutorial: {topic} from scratch",
        "Step-by-step guide to {topic}",
        "Building with {topic}: A hands-on tutorial",
        "{topic} bootcamp",
    ],
    "lightning": [
        "5 things I wish I knew about {topic}",
        "{topic} in 5 minutes",
        "Quick wins with {topic}",
        "The one thing about {topic} that changed everything",
        "{topic}: A lightning tour",
    ],
    "chalk talk": [
        "Architecture deep dive: {topic}",
        "Whiteboard session: Designing {topic}",
        "Interactive discussion: {topic} patterns",
    ],
    "poster": [
        "Visualizing {topic}",
        "{topic}: A visual guide",
    ],
}

CONNECTORS = [
    "meets",
    "for",
    "in the age of",
    "through the lens of",
    "powered by",
    "without",
    "beyond",
    "reimagined with",
]

AUDIENCE_HOOKS = {
    "beginners": ["getting started", "fundamentals", "first steps", "introduction to"],
    "intermediate": ["leveling up", "best practices", "patterns and antipatterns", "practical"],
    "advanced": ["deep dive", "internals", "edge cases", "advanced techniques"],
    "mixed": ["for everyone", "from basics to advanced", "comprehensive guide", "all levels"],
}


def generate_ideas(profile: UserProfile, count: int = 10) -> list[dict]:
    """Generate novel CFP ideas based on user profile."""
    ideas = []
    all_topics = profile.expertise_areas + profile.interests

    if not all_topics:
        all_topics = ["technology", "software development", "best practices"]

    # Strategy 1: Angle + Topic combinations
    for _ in range(count // 3 + 1):
        topic = random.choice(all_topics)
        angle = random.choice(ANGLES)
        title = f"{angle.title()} {topic}"
        ideas.append({
            "title": title,
            "type": "angle-based",
            "topic": topic,
        })

    # Strategy 2: Cross-pollination (combining two topics)
    if len(all_topics) >= 2:
        for _ in range(count // 3 + 1):
            topics = random.sample(all_topics, 2)
            connector = random.choice(CONNECTORS)
            title = f"{topics[0].title()} {connector} {topics[1]}"
            ideas.append({
                "title": title,
                "type": "cross-pollination",
                "topic": f"{topics[0]} + {topics[1]}",
            })

    # Strategy 3: Project-based stories
    for project in profile.recent_projects[:3]:
        angle = random.choice(
            ["How we", "Why we", "What we learned when we", "The story of how we"]
        )
        title = f"{angle} {project}"
        ideas.append({
            "title": title,
            "type": "experience-based",
            "topic": project,
        })

    # Strategy 4: Format-specific titles
    format_templates = FORMATS.get(profile.talk_format, FORMATS["talk"])
    for _ in range(count // 4 + 1):
        topic = random.choice(all_topics)
        template = random.choice(format_templates)
        title = template.format(
            topic=topic,
            duration=random.choice([30, 45]) if profile.talk_format == "talk" else 90,
            artifact=f"{topic} project",
        )
        ideas.append({
            "title": title,
            "type": "format-specific",
            "topic": topic,
        })

    # Strategy 5: Audience-targeted
    hooks = AUDIENCE_HOOKS.get(profile.target_audience, AUDIENCE_HOOKS["mixed"])
    for _ in range(count // 4 + 1):
        topic = random.choice(all_topics)
        hook = random.choice(hooks)
        title = f"{topic.title()}: {hook.title()}"
        ideas.append({
            "title": title,
            "type": "audience-targeted",
            "topic": topic,
        })

    # Strategy 6: Track-aligned ideas
    if profile.conference_track:
        for topic in all_topics[:3]:
            title = f"{topic.title()} for {profile.conference_track}"
            ideas.append({
                "title": title,
                "type": "track-aligned",
                "topic": topic,
            })
            # Also create inverse
            title2 = f"{profile.conference_track}: A {topic.title()} Perspective"
            ideas.append({
                "title": title2,
                "type": "track-aligned",
                "topic": topic,
            })

    # Shuffle and deduplicate
    random.shuffle(ideas)
    seen_titles = set()
    unique_ideas = []
    for idea in ideas:
        title_lower = idea["title"].lower()
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            unique_ideas.append(idea)

    return unique_ideas[:count]


def generate_abstract(title: str, profile: UserProfile) -> str:
    """Generate a brief abstract for a talk idea."""
    track_mention = (
        f" in the {profile.conference_track} space" if profile.conference_track else ""
    )
    conf_mention = f" at {profile.conference_name}" if profile.conference_name else ""

    abstracts = [
        f"In this {profile.talk_format}, we'll explore {title.lower()}{track_mention} "
        f"and share practical insights from real-world experience.",
        f"Join us for an engaging session on {title.lower()}. "
        f"Perfect for {profile.target_audience}{conf_mention}.",
        f"This {profile.talk_format} covers {title.lower()}, "
        f"with actionable takeaways you can apply immediately.",
        f"Discover the key concepts behind {title.lower()} "
        f"and learn how to apply them in your own projects{track_mention}.",
    ]
    return random.choice(abstracts)


def create_download_content(ideas: list[dict], profile: UserProfile) -> str:
    """Create text content for download."""
    lines = [
        f"CFP Ideas for {profile.name}",
        f"Format: {profile.talk_format} | Audience: {profile.target_audience}",
    ]
    if profile.conference_name:
        lines.append(f"Conference: {profile.conference_name}")
    if profile.conference_track:
        lines.append(f"Track: {profile.conference_track}")
    lines.append("=" * 50 + "\n")

    for i, idea in enumerate(ideas, 1):
        lines.append(f"Idea #{i}: {idea['title']}")
        lines.append(f"Type: {idea['type']} | Topic: {idea['topic']}")
        lines.append(f"Abstract: {generate_abstract(idea['title'], profile)}")
        lines.append("")

    return "\n".join(lines)


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="CFP Idea Generator",
        page_icon="🎤",
        layout="wide",
    )

    st.title("🎤 CFP Idea Generator")
    st.write("Generate novel talk/workshop ideas for your next conference submission!")

    # Sidebar for inputs
    with st.sidebar:
        st.header("📋 Conference Details")

        # Conference selection
        conference_list = list(CONFERENCES.keys())
        conference = st.selectbox(
            "Select a conference",
            options=conference_list,
            index=len(conference_list) - 1,
        )

        conf_data = CONFERENCES[conference]

        # Track selection
        track = None
        if conf_data["tracks"]:
            track_options = ["No specific track"] + conf_data["tracks"]
            track_selection = st.selectbox("Select a track", options=track_options)
            if track_selection != "No specific track":
                track = track_selection
        else:
            custom_track = st.text_input("Conference theme/track (optional)")
            if custom_track:
                track = custom_track

        # Format selection
        talk_format = st.selectbox(
            "Talk format",
            options=conf_data["formats"],
            format_func=lambda x: x.title(),
        )

        st.divider()
        st.header("👤 Your Profile")

        name = st.text_input("Your name", value="Speaker")

        expertise = st.text_area(
            "Areas of expertise (comma-separated)",
            placeholder="Python, machine learning, DevOps, databases",
        )
        expertise_areas = [e.strip() for e in expertise.split(",") if e.strip()]

        projects = st.text_area(
            "Recent projects/experiences (comma-separated)",
            placeholder="migrated to microservices, built a CLI tool",
        )
        recent_projects = [p.strip() for p in projects.split(",") if p.strip()]

        interests = st.text_area(
            "Topics you're passionate about (comma-separated)",
            placeholder="open source, mentoring, performance",
        )
        interest_list = [i.strip() for i in interests.split(",") if i.strip()]

        target_audience = st.radio(
            "Target audience",
            options=["beginners", "intermediate", "advanced", "mixed"],
            index=3,
            format_func=lambda x: x.title(),
        )

        st.divider()
        idea_count = st.slider("Number of ideas", min_value=1, max_value=20, value=8)

        generate_button = st.button("🚀 Generate Ideas", type="primary", use_container_width=True)

    # Main content area
    if generate_button:
        if not expertise_areas and not interest_list:
            st.warning("Please enter at least some expertise areas or interests.")
        else:
            # Build profile
            profile = UserProfile(
                name=name,
                expertise_areas=expertise_areas,
                recent_projects=recent_projects,
                interests=interest_list,
                target_audience=target_audience,
                conference_name=conference if conference != "Other / Custom" else None,
                conference_track=track,
                talk_format=talk_format,
            )

            # Generate and store ideas
            st.session_state.ideas = generate_ideas(profile, idea_count)
            st.session_state.profile = profile

    # Display results
    if "ideas" in st.session_state and "profile" in st.session_state:
        ideas = st.session_state.ideas
        profile = st.session_state.profile

        st.header(f"🎯 Generated CFP Ideas for {profile.name}")

        # Info bar
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Format", profile.talk_format.title())
        with col2:
            st.metric("Audience", profile.target_audience.title())
        with col3:
            if profile.conference_name:
                st.metric("Conference", profile.conference_name)
            elif profile.conference_track:
                st.metric("Track", profile.conference_track)
            else:
                st.metric("Ideas", len(ideas))

        st.divider()

        # Display ideas
        for i, idea in enumerate(ideas, 1):
            with st.expander(f"💡 Idea #{i}: {idea['title']}", expanded=(i <= 3)):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Type:** {idea['type']}")
                with col_b:
                    st.write(f"**Core topic:** {idea['topic']}")

                st.write("**Draft abstract:**")
                st.info(generate_abstract(idea["title"], profile))

        # Download button
        st.divider()
        st.download_button(
            label="📥 Download Ideas as Text",
            data=create_download_content(ideas, profile),
            file_name=f"cfp_ideas_{profile.name.lower().replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

        # Tips
        with st.expander("✨ Tips for refining your CFP"):
            st.markdown("""
            - Add a personal story or specific example
            - Include 3-5 key takeaways attendees will learn
            - Mention any demos or hands-on components
            """)
            if profile.conference_name:
                st.markdown(f"- Tailor language to **{profile.conference_name}**'s audience")


if __name__ == "__main__":
    main()
