"""Unit tests for CFP Generator."""

import pytest
from unittest.mock import patch

from cfp_generator import (
    CONFERENCES,
    UserProfile,
    select_conference,
    collect_user_input,
    generate_ideas,
    generate_abstract,
)


class TestSelectConference:
    """Tests for select_conference function."""

    def test_select_conference_valid_input(self):
        """Should return correct conference, track, and format for valid inputs."""
        # Select PyCon US (1), Web Development track (2), tutorial format (2)
        inputs = ["1", "2", "2"]
        with patch("builtins.input", side_effect=inputs):
            conference, track, talk_format = select_conference()

        assert conference == "PyCon US"
        assert track == "Web Development"
        assert talk_format == "tutorial"

    def test_select_conference_kubecon_with_track(self):
        """Should correctly select KubeCon with a specific track."""
        # Select KubeCon (2), CI/CD & GitOps track (2), talk format (1)
        inputs = ["2", "2", "1"]
        with patch("builtins.input", side_effect=inputs):
            conference, track, talk_format = select_conference()

        assert conference == "KubeCon"
        assert track == "CI/CD & GitOps"
        assert talk_format == "talk"

    def test_select_conference_default_inputs(self):
        """Should use defaults when empty input provided."""
        # Empty conference choice defaults to last (Other / Custom)
        # Custom conference asks for theme (empty), then format (empty defaults to first)
        inputs = ["", "", ""]
        with patch("builtins.input", side_effect=inputs):
            conference, track, talk_format = select_conference()

        # Other / Custom returns None for conference name
        assert conference is None
        assert track is None
        assert talk_format == "talk"

    def test_select_conference_no_track_selected(self):
        """Should handle 'no specific track' selection."""
        # Select PyCon US (1), No specific track (8), talk format (1)
        inputs = ["1", "8", "1"]
        with patch("builtins.input", side_effect=inputs):
            conference, track, talk_format = select_conference()

        assert conference == "PyCon US"
        assert track is None
        assert talk_format == "talk"

    def test_select_conference_invalid_input_falls_back(self):
        """Should handle invalid inputs gracefully."""
        # Invalid conference choice falls back to Other / Custom
        inputs = ["invalid", "custom theme", "1"]
        with patch("builtins.input", side_effect=inputs):
            conference, track, talk_format = select_conference()

        assert conference is None
        assert track == "custom theme"
        assert talk_format == "talk"


class TestCollectUserInput:
    """Tests for collect_user_input function."""

    def test_collect_user_input_parses_correctly(self):
        """Should correctly parse and store user data into a UserProfile."""
        inputs = [
            "Jane Doe",  # name
            "3",  # conference: AWS re:Invent
            "2",  # track: Compute
            "1",  # format: talk
            "Python, AWS, serverless",  # expertise
            "migrated to lambda, built data pipeline",  # projects
            "cloud architecture, open source",  # interests
            "2",  # intermediate audience
        ]
        with patch("builtins.input", side_effect=inputs):
            profile = collect_user_input()

        assert profile.name == "Jane Doe"
        assert profile.expertise_areas == ["Python", "AWS", "serverless"]
        assert profile.recent_projects == ["migrated to lambda", "built data pipeline"]
        assert profile.interests == ["cloud architecture", "open source"]
        assert profile.target_audience == "intermediate"
        assert profile.conference_name == "AWS re:Invent"
        assert profile.conference_track == "Compute"
        assert profile.talk_format == "talk"

    def test_collect_user_input_default_name(self):
        """Should use 'Speaker' as default when name is empty."""
        inputs = [
            "",  # empty name
            "1",  # PyCon US
            "1",  # Python Language track
            "1",  # talk format
            "Python",  # expertise
            "project",  # projects
            "coding",  # interests
            "4",  # mixed audience
        ]
        with patch("builtins.input", side_effect=inputs):
            profile = collect_user_input()

        assert profile.name == "Speaker"

    def test_collect_user_input_handles_whitespace(self):
        """Should trim whitespace from comma-separated inputs."""
        inputs = [
            "Test User",
            "1",  # PyCon US
            "1",  # Python Language track
            "1",  # talk format
            "  Python  ,  Django  ,  REST APIs  ",  # expertise with extra spaces
            "  built app  ",  # project with spaces
            "  testing  ",  # interest with spaces
            "1",  # beginner audience
        ]
        with patch("builtins.input", side_effect=inputs):
            profile = collect_user_input()

        assert profile.expertise_areas == ["Python", "Django", "REST APIs"]
        assert profile.recent_projects == ["built app"]
        assert profile.interests == ["testing"]
        assert profile.target_audience == "beginners"

    def test_collect_user_input_default_audience(self):
        """Should default to mixed audience for invalid input."""
        inputs = [
            "User",
            "1", "1", "1",  # conference selections
            "Python",  # expertise
            "project",  # projects
            "coding",  # interests
            "99",  # invalid audience choice
        ]
        with patch("builtins.input", side_effect=inputs):
            profile = collect_user_input()

        assert profile.target_audience == "mixed"


class TestGenerateIdeas:
    """Tests for generate_ideas function."""

    @pytest.fixture
    def sample_profile(self):
        """Create a sample UserProfile for testing."""
        return UserProfile(
            name="Test User",
            expertise_areas=["Python", "machine learning"],
            recent_projects=["built a chatbot", "deployed ML model"],
            interests=["open source", "AI ethics"],
            target_audience="intermediate",
            conference_name="PyCon US",
            conference_track="Data Science & ML",
            talk_format="talk",
        )

    def test_generate_ideas_returns_specified_count(self, sample_profile):
        """Should produce exactly the specified number of ideas."""
        for count in [5, 10, 15]:
            ideas = generate_ideas(sample_profile, count=count)
            assert len(ideas) == count

    def test_generate_ideas_minimum_count(self, sample_profile):
        """Should handle count of 1."""
        ideas = generate_ideas(sample_profile, count=1)
        assert len(ideas) == 1

    def test_generate_ideas_structure(self, sample_profile):
        """Each idea should have required keys."""
        ideas = generate_ideas(sample_profile, count=5)
        for idea in ideas:
            assert "title" in idea
            assert "type" in idea
            assert "topic" in idea
            assert isinstance(idea["title"], str)
            assert len(idea["title"]) > 0

    def test_generate_ideas_includes_angle_based(self, sample_profile):
        """Should include angle-based ideas in output."""
        # Generate many ideas to ensure all strategies are represented
        ideas = generate_ideas(sample_profile, count=20)
        idea_types = {idea["type"] for idea in ideas}
        assert "angle-based" in idea_types

    def test_generate_ideas_includes_cross_pollination(self, sample_profile):
        """Should include cross-pollination ideas combining topics."""
        ideas = generate_ideas(sample_profile, count=20)
        idea_types = {idea["type"] for idea in ideas}
        assert "cross-pollination" in idea_types

    def test_generate_ideas_includes_experience_based(self, sample_profile):
        """Should include experience-based ideas from recent projects."""
        ideas = generate_ideas(sample_profile, count=20)
        idea_types = {idea["type"] for idea in ideas}
        assert "experience-based" in idea_types

    def test_generate_ideas_includes_format_specific(self, sample_profile):
        """Should include format-specific ideas."""
        ideas = generate_ideas(sample_profile, count=20)
        idea_types = {idea["type"] for idea in ideas}
        assert "format-specific" in idea_types

    def test_generate_ideas_includes_audience_targeted(self, sample_profile):
        """Should include audience-targeted ideas."""
        ideas = generate_ideas(sample_profile, count=20)
        idea_types = {idea["type"] for idea in ideas}
        assert "audience-targeted" in idea_types

    def test_generate_ideas_includes_track_aligned_when_track_set(self, sample_profile):
        """Should include track-aligned ideas when conference track is set."""
        ideas = generate_ideas(sample_profile, count=20)
        idea_types = {idea["type"] for idea in ideas}
        assert "track-aligned" in idea_types

    def test_generate_ideas_no_track_aligned_without_track(self):
        """Should not include track-aligned ideas when no track is set."""
        profile = UserProfile(
            name="User",
            expertise_areas=["Python"],
            recent_projects=["a project"],
            interests=["coding"],
            target_audience="mixed",
            conference_track=None,  # No track
        )
        ideas = generate_ideas(profile, count=20)
        idea_types = {idea["type"] for idea in ideas}
        assert "track-aligned" not in idea_types

    def test_generate_ideas_unique_titles(self, sample_profile):
        """Should return unique idea titles (no duplicates)."""
        ideas = generate_ideas(sample_profile, count=15)
        titles = [idea["title"].lower() for idea in ideas]
        assert len(titles) == len(set(titles))

    def test_generate_ideas_with_empty_topics_uses_defaults(self):
        """Should use default topics when user provides none."""
        profile = UserProfile(
            name="User",
            expertise_areas=[],
            recent_projects=[],
            interests=[],
            target_audience="mixed",
        )
        ideas = generate_ideas(profile, count=5)
        assert len(ideas) == 5
        # Ideas should still be generated
        for idea in ideas:
            assert idea["title"]


class TestGenerateAbstract:
    """Tests for generate_abstract function."""

    @pytest.fixture
    def profile_with_all_fields(self):
        """Profile with conference and track set."""
        return UserProfile(
            name="Jane Speaker",
            expertise_areas=["Python", "testing"],
            recent_projects=["automated testing suite"],
            interests=["quality assurance"],
            target_audience="intermediate",
            conference_name="PyCon US",
            conference_track="Testing & Quality",
            talk_format="talk",
        )

    @pytest.fixture
    def profile_minimal(self):
        """Minimal profile without conference details."""
        return UserProfile(
            name="Speaker",
            expertise_areas=["coding"],
            recent_projects=[],
            interests=[],
            target_audience="beginners",
        )

    def test_generate_abstract_includes_title(self, profile_with_all_fields):
        """Abstract should include the idea title."""
        title = "Testing Best Practices"
        abstract = generate_abstract(title, profile_with_all_fields)
        assert title.lower() in abstract.lower()

    def test_generate_abstract_includes_talk_format(self, profile_with_all_fields):
        """Abstract should mention the talk format."""
        title = "My Great Talk"
        abstract = generate_abstract(title, profile_with_all_fields)
        assert profile_with_all_fields.talk_format in abstract.lower()

    def test_generate_abstract_includes_conference_track(self, profile_with_all_fields):
        """Abstract should mention conference track when set."""
        title = "Testing Talk"
        # Generate multiple abstracts since one is chosen randomly
        abstracts = [generate_abstract(title, profile_with_all_fields) for _ in range(20)]
        # At least some abstracts should mention the track
        track_mentioned = any(
            profile_with_all_fields.conference_track in abstract
            for abstract in abstracts
        )
        assert track_mentioned

    def test_generate_abstract_includes_conference_name(self, profile_with_all_fields):
        """Abstract may include conference name when set."""
        title = "Great Talk"
        abstracts = [generate_abstract(title, profile_with_all_fields) for _ in range(20)]
        # At least some abstracts should mention the conference
        conf_mentioned = any(
            profile_with_all_fields.conference_name in abstract
            for abstract in abstracts
        )
        assert conf_mentioned

    def test_generate_abstract_includes_target_audience(self, profile_with_all_fields):
        """Abstract may mention target audience."""
        title = "Cool Topic"
        abstracts = [generate_abstract(title, profile_with_all_fields) for _ in range(20)]
        audience_mentioned = any(
            profile_with_all_fields.target_audience in abstract
            for abstract in abstracts
        )
        assert audience_mentioned

    def test_generate_abstract_without_conference(self, profile_minimal):
        """Should generate valid abstract without conference details."""
        title = "Basic Topic"
        abstract = generate_abstract(title, profile_minimal)
        assert abstract
        assert title.lower() in abstract.lower()
        # Should not have empty mentions
        assert "at None" not in abstract
        assert "in the None" not in abstract

    def test_generate_abstract_returns_string(self, profile_with_all_fields):
        """Should return a non-empty string."""
        title = "Any Topic"
        abstract = generate_abstract(title, profile_with_all_fields)
        assert isinstance(abstract, str)
        assert len(abstract) > 0
