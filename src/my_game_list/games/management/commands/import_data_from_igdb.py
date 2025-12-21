"""A custom django command to import data from the IGDB database."""

from collections.abc import Iterator
from datetime import UTC, date, datetime
from typing import Any, Literal, Self, TypeVar

from django.core.management.base import BaseCommand, CommandParser
from django.db.models import Max

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
    ) -> dict[str, str | int | None | datetime | date | Company]:
        """
        Get the input for the model from the item from the IGDB database.

        Args:
            item_from_igdb (IGDBObject): The item from the IGDB database.
            company_igdb_to_db_mapping (dict[int, Company]): The mapping between IGDB companies and database companies.

        Returns:
            dict[str, str | int | None | datetime | date | Company]: The input for the model.
        """
        model_input: dict[str, str | int | None | datetime | date | Company] = {
            "igdb_id": item_from_igdb.id,
            "igdb_updated_at": (
                datetime.fromtimestamp(item_from_igdb.updated_at, tz=UTC) if item_from_igdb.updated_at else None
            ),
        }
        match item_from_igdb:
            case IGDBGameResponse():
                model_input.update(
                    {
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
                    },
                )
            case IGDBGenreResponse():
                model_input.update(
                    {
                        "name": item_from_igdb.name,
                    },
                )
            case IGDBPlatformResponse():
                model_input.update(
                    {
                        "abbreviation": item_from_igdb.abbreviation,
                        "name": item_from_igdb.name,
                    },
                )
            case IGDBCompanyResponse():
                model_input.update(
                    {
                        "name": item_from_igdb.name,
                        "company_logo_id": (item_from_igdb.logo.image_id if item_from_igdb.logo else ""),
                    },
                )
            case _:
                message_error = f"Invalid type of data from IGDB: {type(item_from_igdb)}"
                raise IGDBInteractionError(message_error)

        return model_input

    def _import_data(
        self: Self,
        endpoint: IGDBEndpoints,
        query: str,
        model: type[ModelType],
    ) -> Iterator[tuple[list[ModelType], IGDBApiResponse]]:
        """Import data from the IGDB database to the application database.

        Args:
            endpoint (IGDBEndpoints): The IGDB endpoint to fetch data from.
            query (str): The query string for the IGDB API.
            model (type[ModelType]): The Django model class to map the IGDB data to.

        Yields:
            Iterator[tuple[list[ModelType], IGDBApiResponse]]: A generator yielding a tuple containing
            a list of created model instances and the raw IGDB API response data for each batch.
        """
        last_updated_at = model.objects.aggregate(max_updated_at=Max("igdb_updated_at"))["max_updated_at"]
        if last_updated_at:
            timestamp = int(last_updated_at.timestamp())
            query = f"{query} where updated_at > {timestamp};"

        self.stdout.write(f"Fetching data from IGDB endpoint: {endpoint.value}, query: {query}")

        for data_from_igdb in self.igdb_wrapper.iter_all_objects(endpoint=endpoint, query=query):
            if not data_from_igdb:
                continue

            # Deduplicate data_from_igdb based on id, keeping the last occurrence
            data_from_igdb_dict = {item.id: item for item in data_from_igdb}
            unique_data_from_igdb = list(data_from_igdb_dict.values())

            company_igdb_to_db_mapping = {company.igdb_id: company for company in Company.objects.all()}
            data_to_import = []
            update_fields: set[str] = set()

            for data in unique_data_from_igdb:
                model_input = self._get_model_input(data, company_igdb_to_db_mapping)
                data_to_import.append(model(**model_input))
                update_fields.update(model_input.keys())

            update_fields.discard("igdb_id")

            yield (
                model.objects.bulk_create(
                    data_to_import,
                    update_conflicts=True,
                    unique_fields=["igdb_id"],
                    update_fields=list(update_fields),
                ),
                unique_data_from_igdb,
            )

    def import_games(self: Self) -> None:
        """Import games from the IGDB database to the application database."""
        genre_igdb_to_db_mapping = {genre.igdb_id: genre.id for genre in Genre.objects.all()}
        platform_igdb_to_db_mapping = {platform.igdb_id: platform.id for platform in Platform.objects.all()}

        total_imported_games = 0

        for imported_games, igdb_games in self._import_data(
            endpoint=IGDBEndpoints.GAMES,
            query=(
                "fields name, cover.image_id, first_release_date, genres, "
                "involved_companies.developer, involved_companies.publisher, involved_companies.company, "
                "platforms, summary, updated_at;"
            ),
            model=Game,
        ):
            total_imported_games += len(imported_games)
            genres_to_games_relation = []
            platforms_to_games_relation = []

            for imported_game, game_from_igdb in zip(imported_games, igdb_games, strict=True):
                if game_from_igdb and isinstance(game_from_igdb, IGDBGameResponse):
                    if genres_ids := game_from_igdb.genres:
                        genres = [
                            Game.genres.through(
                                game_id=imported_game.id,
                                genre_id=genre_igdb_to_db_mapping[genre_id],
                            )
                            for genre_id in genres_ids
                            if genre_id in genre_igdb_to_db_mapping
                        ]
                        genres_to_games_relation.extend(genres)
                    if platform_ids := game_from_igdb.platforms:
                        platforms = [
                            Game.platforms.through(
                                game_id=imported_game.id,
                                platform_id=platform_igdb_to_db_mapping[platform],
                            )
                            for platform in platform_ids
                            if platform in platform_igdb_to_db_mapping
                        ]
                        platforms_to_games_relation.extend(platforms)

            Game.genres.through.objects.bulk_create(genres_to_games_relation, ignore_conflicts=True)
            Game.platforms.through.objects.bulk_create(platforms_to_games_relation, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {total_imported_games} 'Game' from the IGDB database."),
        )

    def import_companies(self: Self) -> None:
        """Import companies from the IGDB database to the application database."""
        total_companies = 0
        for created_companies, _ in self._import_data(
            endpoint=IGDBEndpoints.COMPANIES,
            query="fields name, logo.image_id, updated_at;",
            model=Company,
        ):
            total_companies += len(created_companies)

        self.stdout.write(
            self.style.SUCCESS(
                (f"Successfully created {total_companies} 'Companies' from the IGDB database."),
            ),
        )

    def import_genres(self: Self) -> None:
        """Import genres from the IGDB database to the application database."""
        total_genres = 0
        for created_genres, _ in self._import_data(
            endpoint=IGDBEndpoints.GENRES,
            query="fields name, updated_at;",
            model=Genre,
        ):
            total_genres += len(created_genres)

        self.stdout.write(
            self.style.SUCCESS(
                (f"Successfully created {total_genres} 'Genres' from the IGDB database."),
            ),
        )

    def import_platforms(self: Self) -> None:
        """Import platforms from the IGDB database to the application database."""
        total_platforms = 0
        for created_platforms, _ in self._import_data(
            endpoint=IGDBEndpoints.PLATFORMS,
            query="fields abbreviation, name, updated_at;",
            model=Platform,
        ):
            total_platforms += len(created_platforms)

        self.stdout.write(
            self.style.SUCCESS(
                (f"Successfully created {total_platforms} 'Platforms' from the IGDB database."),
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
