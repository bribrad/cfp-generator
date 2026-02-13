#!/usr/bin/env python3
"""
CFP Idea Generator - Generate novel talk/workshop/speech ideas for conferences.
"""

import random
from dataclasses import dataclass
from typing import Optional


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


def select_conference() -> tuple[Optional[str], Optional[str], str]:
    """Let user select a conference and track. Returns (conference, track, format)."""
    print("\n📋 Select a conference (or choose 'Other' for custom):\n")
    
    conf_list = list(CONFERENCES.keys())
    for i, conf in enumerate(conf_list, 1):
        print(f"  {i}. {conf}")
    
    choice = input(f"\nChoose (1-{len(conf_list)}) [9]: ").strip()
    try:
        idx = int(choice) - 1 if choice else len(conf_list) - 1
        conf_name = conf_list[idx]
    except (ValueError, IndexError):
        conf_name = "Other / Custom"
    
    conf_data = CONFERENCES[conf_name]
    track = None
    
    # Select track if conference has tracks
    if conf_data["tracks"]:
        print(f"\n🎯 Select a track for {conf_name}:\n")
        for i, t in enumerate(conf_data["tracks"], 1):
            print(f"  {i}. {t}")
        print(f"  {len(conf_data['tracks']) + 1}. No specific track")
        
        track_choice = input(f"\nChoose (1-{len(conf_data['tracks']) + 1}): ").strip()
        try:
            track_idx = int(track_choice) - 1
            if 0 <= track_idx < len(conf_data["tracks"]):
                track = conf_data["tracks"][track_idx]
        except (ValueError, IndexError):
            pass
    else:
        # Custom conference - ask for theme
        print("\nEnter your conference theme/track (optional):")
        custom_track = input("> ").strip()
        if custom_track:
            track = custom_track

    # Select format
    print(f"\n📝 Select talk format:\n")
    formats = conf_data["formats"]
    for i, fmt in enumerate(formats, 1):
        print(f"  {i}. {fmt.title()}")
    
    fmt_choice = input(f"\nChoose (1-{len(formats)}) [1]: ").strip()
    try:
        fmt_idx = int(fmt_choice) - 1 if fmt_choice else 0
        talk_format = formats[fmt_idx]
    except (ValueError, IndexError):
        talk_format = formats[0]

    return (
        conf_name if conf_name != "Other / Custom" else None,
        track,
        talk_format,
    )


def collect_user_input() -> UserProfile:
    """Interactively collect information from the user."""
    print("\n" + "=" * 60)
    print("🎤 CFP Idea Generator - Let's create some talk ideas!")
    print("=" * 60)

    name = input("\nYour name: ").strip() or "Speaker"

    # Conference selection
    conference_name, conference_track, talk_format = select_conference()

    print("\n" + "-" * 40)
    print("Now tell us about yourself...")
    print("-" * 40)

    print("\nEnter your areas of expertise (comma-separated):")
    print("  Example: Python, machine learning, DevOps, databases")
    expertise_input = input("> ").strip()
    expertise_areas = [e.strip() for e in expertise_input.split(",") if e.strip()]

    print("\nRecent projects or experiences you could talk about (comma-separated):")
    print("  Example: migrated to microservices, built a CLI tool, led a team")
    projects_input = input("> ").strip()
    recent_projects = [p.strip() for p in projects_input.split(",") if p.strip()]

    print("\nTopics you're passionate about (comma-separated):")
    print("  Example: open source, mentoring, performance optimization")
    interests_input = input("> ").strip()
    interests = [i.strip() for i in interests_input.split(",") if i.strip()]

    print("\nTarget audience level:")
    print("  1. Beginners")
    print("  2. Intermediate")
    print("  3. Advanced")
    print("  4. Mixed/All levels")
    audience_choice = input("Choose (1-4) [4]: ").strip() or "4"
    audience_map = {"1": "beginners", "2": "intermediate", "3": "advanced", "4": "mixed"}
    target_audience = audience_map.get(audience_choice, "mixed")

    return UserProfile(
        name=name,
        expertise_areas=expertise_areas,
        recent_projects=recent_projects,
        interests=interests,
        target_audience=target_audience,
        conference_name=conference_name,
        conference_track=conference_track,
        talk_format=talk_format,
    )


def generate_ideas(profile: UserProfile, count: int = 10) -> list[dict]:
    """Generate novel CFP ideas based on user profile."""
    ideas = []
    all_topics = profile.expertise_areas + profile.interests
    
    # Add track as a topic modifier if available
    track_topics = []
    if profile.conference_track:
        track_topics = [profile.conference_track.lower()]
    
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
        angle = random.choice(["How we", "Why we", "What we learned when we", "The story of how we"])
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
    track_mention = f" in the {profile.conference_track} space" if profile.conference_track else ""
    conf_mention = f" at {profile.conference_name}" if profile.conference_name else ""
    
    abstracts = [
        f"In this {profile.talk_format}, we'll explore {title.lower()}{track_mention} and share practical insights from real-world experience.",
        f"Join us for an engaging session on {title.lower()}. Perfect for {profile.target_audience}{conf_mention}.",
        f"This {profile.talk_format} covers {title.lower()}, with actionable takeaways you can apply immediately.",
        f"Discover the key concepts behind {title.lower()} and learn how to apply them in your own projects{track_mention}.",
    ]
    return random.choice(abstracts)


def display_ideas(ideas: list[dict], profile: UserProfile) -> None:
    """Display generated ideas in a formatted way."""
    print("\n" + "=" * 60)
    print(f"🎯 Generated CFP Ideas for {profile.name}")
    print(f"   Format: {profile.talk_format.title()} | Audience: {profile.target_audience.title()}")
    if profile.conference_name:
        print(f"   Conference: {profile.conference_name}")
    if profile.conference_track:
        print(f"   Track: {profile.conference_track}")
    print("=" * 60)

    for i, idea in enumerate(ideas, 1):
        print(f"\n{'─' * 50}")
        print(f"💡 Idea #{i}: {idea['title']}")
        print(f"   Type: {idea['type']} | Core topic: {idea['topic']}")
        print(f"\n   📝 Draft abstract:")
        abstract = generate_abstract(idea['title'], profile)
        print(f"   {abstract}")

    print("\n" + "=" * 60)
    print("✨ Tips for refining your CFP:")
    print("   • Add a personal story or specific example")
    print("   • Include 3-5 key takeaways attendees will learn")
    print("   • Mention any demos or hands-on components")
    if profile.conference_name:
        print(f"   • Tailor language to {profile.conference_name}'s audience")
    print("=" * 60 + "\n")


def main():
    """Main entry point."""
    try:
        profile = collect_user_input()
        
        print("\nHow many ideas would you like? (default: 8)")
        count_input = input("> ").strip()
        count = int(count_input) if count_input.isdigit() else 8
        count = max(1, min(count, 20))

        ideas = generate_ideas(profile, count)
        display_ideas(ideas, profile)

        # Option to save
        print("Would you like to save these ideas to a file? (y/N)")
        save_choice = input("> ").strip().lower()
        if save_choice == "y":
            filename = f"cfp_ideas_{profile.name.lower().replace(' ', '_')}.txt"
            with open(filename, "w") as f:
                f.write(f"CFP Ideas for {profile.name}\n")
                f.write(f"Format: {profile.talk_format} | Audience: {profile.target_audience}\n")
                if profile.conference_name:
                    f.write(f"Conference: {profile.conference_name}\n")
                if profile.conference_track:
                    f.write(f"Track: {profile.conference_track}\n")
                f.write("=" * 50 + "\n\n")
                for i, idea in enumerate(ideas, 1):
                    f.write(f"Idea #{i}: {idea['title']}\n")
                    f.write(f"Type: {idea['type']} | Topic: {idea['topic']}\n")
                    f.write(f"Abstract: {generate_abstract(idea['title'], profile)}\n\n")
            print(f"✅ Saved to {filename}")

    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
