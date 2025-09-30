"""A custom django command to import data from the IGDB database."""

from datetime import UTC, date, datetime
from typing import Any, Literal, Self, TypeVar

from django.core.management.base import BaseCommand, CommandParser

from my_game_list.games.management.commands._igdb_wrapper import (
    IGDBApiResponse,
    IGDBCompanyResponse,
    IGDBEndpoints,
    IGDBGameResponse,
    IGDBGenreResponse,
    IGDBInteractionError,
    IGDBInvolvedCompanyResponse,
    IGDBObject,
    IGDBPlatformResponse,
    IGDBWrapper,
)
from my_game_list.games.models import Company, Game, Genre, Platform

ModelType = TypeVar("ModelType", Game, Company, Genre, Platform)


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

    @staticmethod
    def _get_company(
        company_type: Literal["developer", "publisher"],
        involved_companies: list[IGDBInvolvedCompanyResponse] | None,
        company_igdb_to_db_mapping: dict[int, Company],
    ) -> Company | None:
        """
        Get the company from the involved companies list.

        Args:
            company_type (Literal["developer", "publisher"]): The type of company to look for.
            involved_companies (list[IGDBInvolvedCompanyResponse] | None): The list of involved companies.
            company_igdb_to_db_mapping (dict[int, Company]): The mapping between IGDB companies and database companies.

        Returns:
            Company | None: The company or None if not found.
        """
        if involved_companies is None:
            return None

        companies_by_id = {company.company: company for company in involved_companies}
        company_id = next(
            (company_id for company_id, company in companies_by_id.items() if getattr(company, company_type)),
            None,
        )

        return company_igdb_to_db_mapping.get(company_id) if company_id is not None else None

    def _get_model_input(
        self: Self,
        item_from_igdb: IGDBObject,
        company_igdb_to_db_mapping: dict[int, Company],
    ) -> dict[str, str | int | None | date | Company]:
        """
        Get the input for the model from the item from the IGDB database.

        Args:
            item_from_igdb (IGDBObject): The item from the IGDB database.
            company_igdb_to_db_mapping (dict[int, Company]): The mapping between IGDB companies and database companies.

        Returns:
            dict[str, str | int | None | date | Company]: The input for the model.
        """
        match item_from_igdb:
            case IGDBGameResponse():
                return {
                    "title": item_from_igdb.name,
                    "release_date": (
                        datetime.fromtimestamp(item_from_igdb.first_release_date, tz=UTC).date()
                        if item_from_igdb.first_release_date
                        else None
                    ),
                    "cover_image_id": (item_from_igdb.cover.image_id if item_from_igdb.cover else ""),
                    "summary": item_from_igdb.summary,
                    "publisher": self._get_company(
                        company_type="publisher",
                        involved_companies=item_from_igdb.involved_companies,
                        company_igdb_to_db_mapping=company_igdb_to_db_mapping,
                    ),
                    "developer": self._get_company(
                        company_type="developer",
                        involved_companies=item_from_igdb.involved_companies,
                        company_igdb_to_db_mapping=company_igdb_to_db_mapping,
                    ),
                    "igdb_id": item_from_igdb.id,
                }
            case IGDBGenreResponse():
                return {
                    "name": item_from_igdb.name,
                    "igdb_id": item_from_igdb.id,
                }
            case IGDBPlatformResponse():
                return {
                    "abbreviation": item_from_igdb.abbreviation,
                    "igdb_id": item_from_igdb.id,
                    "name": item_from_igdb.name,
                }
            case IGDBCompanyResponse():
                return {
                    "name": item_from_igdb.name,
                    "igdb_id": item_from_igdb.id,
                    "company_logo_id": (item_from_igdb.logo.image_id if item_from_igdb.logo else ""),
                }
            case _:
                message_error = f"Invalid type of data from IGDB: {type(item_from_igdb)}"
                raise IGDBInteractionError(message_error)

    def _import_data(
        self: Self,
        endpoint: IGDBEndpoints,
        query: str,
        model: type[ModelType],
    ) -> tuple[list[ModelType], IGDBApiResponse]:
        """Import data from the IGDB database to the application database.

        Args:
            endpoint (IGDBEndpoints): The IGDB endpoint to fetch data from.
            query (str): The query string for the IGDB API.
            model (type[ModelType]): The Django model class to map the IGDB data to.

        Returns:
            tuple[list[ModelType], IGDBApiResponse]: A tuple containing a list of created model instances
            and the raw IGDB API response data.
        """
        data_from_igdb = self.igdb_wrapper.get_all_objects(
            endpoint=endpoint,
            query=query,
        )

        company_igdb_to_db_mapping = {company.igdb_id: company for company in Company.objects.all()}
        data_to_import = [model(**self._get_model_input(data, company_igdb_to_db_mapping)) for data in data_from_igdb]

        return (
            model.objects.bulk_create(data_to_import, ignore_conflicts=True),
            data_from_igdb,
        )

    def import_games(self: Self) -> None:
        """Import games from the IGDB database to the application database."""
        imported_games, igdb_games = self._import_data(
            endpoint=IGDBEndpoints.GAMES,
            query=(
                "fields name, cover.image_id, first_release_date, genres, "
                "involved_companies.developer, involved_companies.publisher, involved_companies.company, "
                "platforms, summary;"
            ),
            model=Game,
        )

        genre_igdb_to_db_mapping = {genre.igdb_id: genre.id for genre in Genre.objects.all()}
        platform_igdb_to_db_mapping = {platform.igdb_id: platform.id for platform in Platform.objects.all()}
        igdb_games_mapping = {game.id: game for game in igdb_games}

        genres_to_games_relation = []
        platforms_to_games_relation = []
        for imported_game in Game.objects.all():
            game_from_igdb = igdb_games_mapping.get(imported_game.igdb_id)
            if game_from_igdb and isinstance(game_from_igdb, IGDBGameResponse):
                if genres_ids := game_from_igdb.genres:
                    genres = [
                        Game.genres.through(
                            game_id=imported_game.id,
                            genre_id=genre_igdb_to_db_mapping[genre_id],
                        )
                        for genre_id in genres_ids
                    ]
                    genres_to_games_relation.extend(genres)
                if platform_ids := game_from_igdb.platforms:
                    platforms = [
                        Game.platforms.through(
                            game_id=imported_game.id,
                            platform_id=platform_igdb_to_db_mapping[platform],
                        )
                        for platform in platform_ids
                    ]
                    platforms_to_games_relation.extend(platforms)

        Game.genres.through.objects.bulk_create(genres_to_games_relation, ignore_conflicts=True)
        Game.platforms.through.objects.bulk_create(platforms_to_games_relation, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {len(imported_games)} 'Game' from the IGDB database."),
        )

    def import_companies(self: Self) -> None:
        """Import companies from the IGDB database to the application database."""
        created_companies, _ = self._import_data(
            endpoint=IGDBEndpoints.COMPANIES,
            query="fields name, logo.image_id;",
            model=Company,
        )

        self.stdout.write(
            self.style.SUCCESS(
                (f"Successfully created {len(created_companies)} 'Companies' from the IGDB database."),
            ),
        )

    def import_genres(self: Self) -> None:
        """Import genres from the IGDB database to the application database."""
        created_genres, _ = self._import_data(
            endpoint=IGDBEndpoints.GENRES,
            query="fields name;",
            model=Genre,
        )

        self.stdout.write(
            self.style.SUCCESS(
                (f"Successfully created {len(created_genres)} 'Genres' from the IGDB database."),
            ),
        )

    def import_platforms(self: Self) -> None:
        """Import platforms from the IGDB database to the application database."""
        created_platforms, _ = self._import_data(
            endpoint=IGDBEndpoints.PLATFORMS,
            query="fields abbreviation, name;",
            model=Platform,
        )

        self.stdout.write(
            self.style.SUCCESS(
                (f"Successfully created {len(created_platforms)} 'Platforms' from the IGDB database."),
            ),
        )

    def handle(self: Self, *args: None, **options: dict[str, int | None | str]) -> None:
        """Handle the command logic."""
        self.stdout.write(f"{args=}")
        self.stdout.write(f"{options=}")
        actions = {
            "platforms": self.import_platforms,
            "genres": self.import_genres,
            "companies": self.import_companies,
            "games": self.import_games,
        }

        for item in options["what_to_import"]:
            action = actions.get(item)
            if action:
                action()

        self.stdout.write(
            self.style.SUCCESS("Import process completed."),
        )
