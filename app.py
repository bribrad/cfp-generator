#!/usr/bin/env python3
"""
CFP Idea Generator - Streamlit App
Generate novel talk/workshop/speech ideas for conferences.
"""

import os
import random
from dataclasses import dataclass
from typing import Optional

import streamlit as st
from openai import OpenAI


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


def generate_key_takeaways(title: str, profile: UserProfile) -> list[str]:
    """Generate key takeaways for a talk idea."""
    topic = title.lower()
    audience = profile.target_audience
    
    takeaway_templates = [
        f"Understand the core principles of {topic}",
        f"Learn practical techniques for implementing {topic}",
        f"Identify common pitfalls and how to avoid them",
        f"Gain hands-on experience with real-world examples",
        f"Develop a framework for evaluating {topic} solutions",
        f"Discover best practices used by industry leaders",
        f"Walk away with actionable steps to apply immediately",
        f"Build confidence in working with {topic}",
    ]
    
    if audience == "beginners":
        takeaway_templates.extend([
            "Get a solid foundation in fundamental concepts",
            "Learn the essential vocabulary and mental models",
        ])
    elif audience == "advanced":
        takeaway_templates.extend([
            "Explore edge cases and advanced optimization techniques",
            "Deep dive into internals and architecture decisions",
        ])
    
    return random.sample(takeaway_templates, min(5, len(takeaway_templates)))


def generate_fit_reasons(title: str, profile: UserProfile) -> list[str]:
    """Generate reasons why this talk would be a good fit."""
    reasons = []
    
    if profile.conference_name:
        reasons.append(f"Aligns with {profile.conference_name}'s focus on practical, actionable content")
    
    if profile.conference_track:
        reasons.append(f"Directly relevant to the {profile.conference_track} track")
    
    reasons.extend([
        f"Addresses current industry trends and challenges",
        f"Provides unique insights from hands-on experience",
        f"Suitable for {profile.target_audience} audience with clear learning outcomes",
        f"Combines theoretical foundation with practical application",
        f"Fills a gap in existing conference content",
    ])
    
    if profile.talk_format == "workshop" or profile.talk_format == "tutorial":
        reasons.append("Hands-on format ensures attendees leave with real skills")
    elif profile.talk_format == "lightning":
        reasons.append("Concise format delivers high-impact insights quickly")
    
    return reasons[:5]


def get_openai_client() -> Optional[OpenAI]:
    """Get OpenAI client if API key is available."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return OpenAI(api_key=api_key)
    return None


def chat_with_ai(messages: list[dict], idea: dict, profile: UserProfile) -> str:
    """Chat with AI about the CFP idea."""
    client = get_openai_client()
    if not client:
        return "Please set OPENAI_API_KEY environment variable to use the AI assistant."
    
    system_prompt = f"""You are a helpful CFP (Call for Papers) writing assistant. 
You're helping a speaker named {profile.name} develop their conference talk idea.

Talk Details:
- Title: {idea['title']}
- Format: {profile.talk_format}
- Target Audience: {profile.target_audience}
- Conference: {profile.conference_name or 'Not specified'}
- Track: {profile.conference_track or 'Not specified'}
- Speaker's Expertise: {', '.join(profile.expertise_areas) or 'Not specified'}

Help them refine their abstract, develop talking points, suggest examples, 
and improve their submission. Be encouraging but also provide constructive feedback."""
    
    full_messages = [{"role": "system", "content": system_prompt}] + messages
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=full_messages,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error communicating with AI: {str(e)}"


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


def render_generator_page():
    """Render the idea generator page."""
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
            st.rerun()

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

        # Display ideas as selectable cards
        st.write("**Click on an idea to expand and refine it:**")
        
        for i, idea in enumerate(ideas):
            col_card, col_btn = st.columns([5, 1])
            with col_card:
                st.write(f"💡 **{idea['title']}**")
                st.caption(f"{idea['type']} • {idea['topic']}")
            with col_btn:
                if st.button("Expand →", key=f"select_{i}", use_container_width=True):
                    st.session_state.selected_idea_index = i
                    st.session_state.chat_messages = []
                    st.rerun()
            st.divider()

        # Download button
        st.download_button(
            label="📥 Download Ideas as Text",
            data=create_download_content(ideas, profile),
            file_name=f"cfp_ideas_{profile.name.lower().replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )


def render_detail_page():
    """Render the CFP detail/refinement page."""
    ideas = st.session_state.ideas
    profile = st.session_state.profile
    selected_index = st.session_state.selected_idea_index
    selected_idea = ideas[selected_index]
    
    # Initialize chat messages if not present
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    # Sidebar with all ideas
    with st.sidebar:
        st.header("📝 Your CFP Ideas")
        
        # Back button
        if st.button("← Back to Generator", use_container_width=True):
            del st.session_state.selected_idea_index
            st.rerun()
        
        st.divider()
        
        # List all ideas
        for i, idea in enumerate(ideas):
            is_selected = i == selected_index
            button_type = "primary" if is_selected else "secondary"
            
            if st.button(
                f"{'✅ ' if is_selected else ''}{idea['title'][:40]}{'...' if len(idea['title']) > 40 else ''}",
                key=f"sidebar_idea_{i}",
                use_container_width=True,
                type=button_type,
            ):
                st.session_state.selected_idea_index = i
                st.session_state.chat_messages = []
                st.rerun()
        
        st.divider()
        st.caption(f"**Conference:** {profile.conference_name or 'Custom'}")
        st.caption(f"**Format:** {profile.talk_format.title()}")
        st.caption(f"**Audience:** {profile.target_audience.title()}")
    
    # Main content
    st.title(f"💡 {selected_idea['title']}")
    st.caption(f"Type: {selected_idea['type']} • Core topic: {selected_idea['topic']}")
    
    # Create tabs for different sections
    tab_abstract, tab_takeaways, tab_fit, tab_chat = st.tabs([
        "📄 Abstract", "🎯 Key Takeaways", "✨ Why It's a Good Fit", "🤖 AI Assistant"
    ])
    
    with tab_abstract:
        st.subheader("Draft Abstract")
        
        # Generate or use cached abstract
        cache_key = f"abstract_{selected_index}"
        if cache_key not in st.session_state:
            st.session_state[cache_key] = generate_abstract(selected_idea["title"], profile)
        
        abstract = st.text_area(
            "Edit your abstract:",
            value=st.session_state[cache_key],
            height=200,
            key=f"abstract_edit_{selected_index}",
        )
        
        if abstract != st.session_state[cache_key]:
            st.session_state[cache_key] = abstract
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Regenerate Abstract", use_container_width=True):
                st.session_state[cache_key] = generate_abstract(selected_idea["title"], profile)
                st.rerun()
        with col2:
            st.download_button(
                "📋 Copy Abstract",
                data=abstract,
                file_name="abstract.txt",
                mime="text/plain",
                use_container_width=True,
            )
    
    with tab_takeaways:
        st.subheader("Key Takeaways")
        st.write("What attendees will learn from your talk:")
        
        # Generate or use cached takeaways
        cache_key = f"takeaways_{selected_index}"
        if cache_key not in st.session_state:
            st.session_state[cache_key] = generate_key_takeaways(selected_idea["title"], profile)
        
        takeaways = st.session_state[cache_key]
        
        for i, takeaway in enumerate(takeaways, 1):
            st.write(f"{i}. {takeaway}")
        
        if st.button("🔄 Regenerate Takeaways", use_container_width=True):
            st.session_state[cache_key] = generate_key_takeaways(selected_idea["title"], profile)
            st.rerun()
    
    with tab_fit:
        st.subheader("Why This Would Be a Good Fit")
        
        # Generate or use cached fit reasons
        cache_key = f"fit_{selected_index}"
        if cache_key not in st.session_state:
            st.session_state[cache_key] = generate_fit_reasons(selected_idea["title"], profile)
        
        reasons = st.session_state[cache_key]
        
        for reason in reasons:
            st.write(f"✅ {reason}")
        
        if st.button("🔄 Regenerate Fit Analysis", use_container_width=True):
            st.session_state[cache_key] = generate_fit_reasons(selected_idea["title"], profile)
            st.rerun()
    
    with tab_chat:
        st.subheader("🤖 CFP AI Assistant")
        st.write("Chat with AI to refine your CFP submission, get feedback, or brainstorm ideas.")
        
        # Check for API key
        if not os.environ.get("OPENAI_API_KEY"):
            st.warning("⚠️ Set the `OPENAI_API_KEY` environment variable to enable AI chat.")
            st.code("export OPENAI_API_KEY='your-api-key'")
        
        # Display chat history
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about your CFP idea..."):
            # Add user message
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = chat_with_ai(
                        st.session_state.chat_messages,
                        selected_idea,
                        profile,
                    )
                    st.markdown(response)
            
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
        
        # Quick action buttons
        st.divider()
        st.write("**Quick prompts:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Improve my abstract", use_container_width=True):
                prompt = f"Please help me improve this abstract for my talk '{selected_idea['title']}': {st.session_state.get(f'abstract_{selected_index}', '')}"
                st.session_state.chat_messages.append({"role": "user", "content": prompt})
                st.rerun()
            if st.button("💡 Suggest examples", use_container_width=True):
                prompt = f"What are some good real-world examples or case studies I could include in my talk about '{selected_idea['title']}'?"
                st.session_state.chat_messages.append({"role": "user", "content": prompt})
                st.rerun()
        with col2:
            if st.button("🎯 Sharpen the focus", use_container_width=True):
                prompt = f"How can I make my talk '{selected_idea['title']}' more focused and impactful? What should I cut or emphasize?"
                st.session_state.chat_messages.append({"role": "user", "content": prompt})
                st.rerun()
            if st.button("❓ Anticipate Q&A", use_container_width=True):
                prompt = f"What questions might the audience ask after my talk on '{selected_idea['title']}'? How should I prepare to answer them?"
                st.session_state.chat_messages.append({"role": "user", "content": prompt})
                st.rerun()


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="CFP Idea Generator",
        page_icon="🎤",
        layout="wide",
    )
    
    # Route to appropriate page
    if "selected_idea_index" in st.session_state and "ideas" in st.session_state:
        render_detail_page()
    else:
        render_generator_page()


if __name__ == "__main__":
    main()
