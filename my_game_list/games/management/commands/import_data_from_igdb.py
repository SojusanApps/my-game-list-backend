"""A custom django command to import data from the IGDB database."""

from datetime import UTC, datetime
from typing import Any, Self, cast

from django.core.management.base import BaseCommand, CommandParser

from my_game_list.games.management.commands._igdb_wrapper import (
    IGDBCompanyResponse,
    IGDBEndpoints,
    IGDBGameResponse,
    IGDBGenreResponse,
    IGDBInvolvedCompanyResponse,
    IGDBPlatformResponse,
    IGDBWrapper,
)
from my_game_list.games.models import Company, Game, Genre, Platform


class Command(BaseCommand):
    """A custom django command to import data from the IGDB database."""

    help = "Import data from the IGDB database."

    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Initializer for the command."""
        super().__init__(*args, **kwargs)
        self.igdb_wrapper = IGDBWrapper()

    def add_arguments(self: Self, parser: CommandParser) -> None:
        """Add arguments to the command."""
        parser.add_argument(
            "what_to_import",
            choices=("platforms", "genres", "companies", "games"),
            nargs="+",
            help="What to import from the IGDB database.",
        )

    def import_games(self: Self) -> None:
        """Import games from the IGDB database to the application database."""
        games = cast(
            list[IGDBGameResponse],
            self.igdb_wrapper.get_all_objects(
                IGDBEndpoints.GAMES,
                (
                    "fields name, cover.image_id, first_release_date, genres, involved_companies.developer, "
                    "involved_companies.publisher, involved_companies.company, platforms, summary;"
                ),
            ),
        )

        company_igdb_to_db_mapping = {company.igdb_id: company for company in Company.objects.all()}

        def get_publisher(involved_companies: list[IGDBInvolvedCompanyResponse]) -> Company | None:
            """Get the publisher company from the involved companies list."""
            for company in involved_companies:
                if company["publisher"]:
                    return company_igdb_to_db_mapping[company["company"]]
            return None

        def get_developer(involved_companies: list[IGDBInvolvedCompanyResponse]) -> Company | None:
            """Get the developer company from the involved companies list."""
            for company in involved_companies:
                if company["developer"]:
                    return company_igdb_to_db_mapping[company["company"]]
            return None

        games_to_import = [
            Game(
                title=game["name"],
                release_date=(
                    datetime.fromtimestamp(game["first_release_date"], tz=UTC).date()
                    if game.get("first_release_date")
                    else None
                ),
                cover_image_id=game["cover"]["image_id"] if game.get("cover") else "",
                summary=game.get("summary", ""),
                publisher=get_publisher(game.get("involved_companies", [])),
                developer=get_developer(game.get("involved_companies", [])),
                igdb_id=game["id"],
            )
            for game in games
        ]

        imported_games = Game.objects.bulk_create(games_to_import, ignore_conflicts=True)

        genre_igdb_to_db_mapping = {genre.igdb_id: genre.id for genre in Genre.objects.all()}
        platform_igdb_to_db_mapping = {platform.igdb_id: platform.id for platform in Platform.objects.all()}
        igdb_games_mapping = {game["id"]: game for game in games}

        genres_to_games_relation = []
        platforms_to_games_relation = []
        for imported_game in Game.objects.all():
            game_from_igdb = igdb_games_mapping.get(imported_game.igdb_id)
            if game_from_igdb:
                genres = [
                    Game.genres.through(game_id=imported_game.id, genre_id=genre_igdb_to_db_mapping[genre])
                    for genre in game_from_igdb.get("genres", [])
                ]
                genres_to_games_relation.extend(genres)
                platforms = [
                    Game.platforms.through(game_id=imported_game.id, platform_id=platform_igdb_to_db_mapping[platform])
                    for platform in game_from_igdb.get("platforms", [])
                ]
                platforms_to_games_relation.extend(platforms)

        Game.genres.through.objects.bulk_create(genres_to_games_relation, ignore_conflicts=True)
        Game.platforms.through.objects.bulk_create(platforms_to_games_relation, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {len(imported_games)} 'Game' from the IGDB database."),
        )

    def import_companies(self: Self) -> None:
        """Import companies from the IGDB database to the application database."""
        companies = cast(
            list[IGDBCompanyResponse],
            self.igdb_wrapper.get_all_objects(
                IGDBEndpoints.COMPANIES,
                "fields name, logo.image_id;",
            ),
        )
        companies_to_import = [
            Company(
                name=company["name"],
                igdb_id=company["id"],
                company_logo_id=company["logo"]["image_id"] if company.get("logo") else "",
            )
            for company in companies
        ]

        imported_companies = Company.objects.bulk_create(companies_to_import, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {len(imported_companies)} 'Company' from the IGDB database."),
        )

    def import_genres(self: Self) -> None:
        """Import genres from the IGDB database to the application database."""
        genres = cast(
            list[IGDBGenreResponse],
            self.igdb_wrapper.get_all_objects(
                IGDBEndpoints.GENRES,
                "fields name;",
            ),
        )
        genres_to_import = [
            Genre(
                name=genre["name"],
                igdb_id=genre["id"],
            )
            for genre in genres
        ]

        imported_genres = Genre.objects.bulk_create(genres_to_import, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {len(imported_genres)} 'Genres' from the IGDB database."),
        )

    def import_platforms(self: Self) -> None:
        """Import platforms from the IGDB database to the application database."""
        platforms = cast(
            list[IGDBPlatformResponse],
            self.igdb_wrapper.get_all_objects(
                IGDBEndpoints.PLATFORMS,
                "fields abbreviation, name;",
            ),
        )
        platforms_to_import = [
            Platform(
                abbreviation=platform.get("abbreviation", ""),
                igdb_id=platform["id"],
                name=platform["name"],
            )
            for platform in platforms
        ]

        imported_platforms = Platform.objects.bulk_create(platforms_to_import, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {len(imported_platforms)} 'Platforms' from the IGDB database."),
        )

    def handle(self: Self, *args: None, **options: dict[str, int | None | str]) -> None:
        """Handle the command logic."""
        self.stdout.write(f"{args}")
        self.stdout.write(f"{options}")
        what_to_import = options["what_to_import"]
        if "platforms" in what_to_import:
            self.import_platforms()
        if "genres" in what_to_import:
            self.import_genres()
        if "companies" in what_to_import:
            self.import_companies()
        if "games" in what_to_import:
            self.import_games()

        self.stdout.write(
            self.style.SUCCESS("Import process completed."),
        )
