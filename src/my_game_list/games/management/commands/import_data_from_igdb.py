"""A custom django command to import data from the IGDB database."""

import time
from dataclasses import dataclass
from datetime import UTC, date, datetime
from typing import TYPE_CHECKING, Any, Literal, Self, TypeVar

from django.core.management.base import BaseCommand, CommandParser
from django.db.models import Max

from my_game_list.games.management.commands._igdb_wrapper import (
    IGDBApiResponse,
    IGDBCompanyResponse,
    IGDBEndpoints,
    IGDBGameEngineResponse,
    IGDBGameModeResponse,
    IGDBGameResponse,
    IGDBGameStatusResponse,
    IGDBGameTypeResponse,
    IGDBGenreResponse,
    IGDBInteractionError,
    IGDBInvolvedCompanyResponse,
    IGDBObject,
    IGDBPlatformResponse,
    IGDBPlayerPerspectiveResponse,
    IGDBWrapper,
)
from my_game_list.games.models import (
    Company,
    Game,
    GameEngine,
    GameMode,
    GameStatus,
    GameType,
    Genre,
    Platform,
    PlayerPerspective,
)

if TYPE_CHECKING:
    from collections.abc import Iterator


ModelType = TypeVar(
    "ModelType",
    Game,
    Company,
    Genre,
    Platform,
    GameEngine,
    GameMode,
    PlayerPerspective,
    GameStatus,
    GameType,
)


@dataclass
class RecursiveDataCollector:
    """Collector for recursive data during import."""

    parent_updates: list[tuple[int, int]]
    recursive_m2m_data: dict[str, list[tuple[int, int]]]
    all_target_igdb_ids: set[int]


class Command(BaseCommand):
    """A custom django command to import data from the IGDB database."""

    help = "Import data from the IGDB database."
    NAME_UPDATED_AT_QUERY = "fields name, updated_at;"

    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Initializer for the command."""
        super().__init__(*args, **kwargs)
        self.igdb_wrapper = IGDBWrapper()

    def add_arguments(self: Self, parser: CommandParser) -> None:
        """Add arguments to the command."""
        parser.add_argument(
            "what_to_import",
            choices=(
                "platforms",
                "genres",
                "companies",
                "games",
                "game_modes",
                "player_perspectives",
                "game_engines",
                "game_types",
                "game_statuses",
            ),
            nargs="+",
            help="What to import from the IGDB database.",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Import all data from the beginning, ignoring the last update time.",
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

    def _get_game_input(
        self: Self,
        item_from_igdb: IGDBGameResponse,
        company_igdb_to_db_mapping: dict[int, Company],
        extra_mappings: dict[str, dict[int, Any]] | None = None,
    ) -> dict[str, Any]:
        """Get the input for the Game model."""
        game_type_mapping = extra_mappings.get("game_type") if extra_mappings else None
        game_status_mapping = extra_mappings.get("game_status") if extra_mappings else None

        game_type = (
            game_type_mapping.get(item_from_igdb.game_type)
            if game_type_mapping and item_from_igdb.game_type is not None
            else None
        )
        game_status = (
            game_status_mapping.get(item_from_igdb.game_status)
            if game_status_mapping and item_from_igdb.game_status is not None
            else None
        )

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
            "game_type": game_type,
            "game_status": game_status,
            "screenshots": ([s.image_id for s in item_from_igdb.screenshots] if item_from_igdb.screenshots else []),
        }

    def _get_game_type_input(self: Self, item_from_igdb: IGDBGameTypeResponse) -> dict[str, Any]:
        """Get the input for the GameType model."""
        return {"type": item_from_igdb.type}

    def _get_game_status_input(self: Self, item_from_igdb: IGDBGameStatusResponse) -> dict[str, Any]:
        """Get the input for the GameStatus model."""
        return {"status": item_from_igdb.status}

    def _get_platform_input(self: Self, item_from_igdb: IGDBPlatformResponse) -> dict[str, Any]:
        """Get the input for the Platform model."""
        return {
            "abbreviation": item_from_igdb.abbreviation,
            "name": item_from_igdb.name,
        }

    def _get_company_input(self: Self, item_from_igdb: IGDBCompanyResponse) -> dict[str, Any]:
        """Get the input for the Company model."""
        return {
            "name": item_from_igdb.name,
            "company_logo_id": (item_from_igdb.logo.image_id if item_from_igdb.logo else ""),
        }

    def _get_model_input(
        self: Self,
        item_from_igdb: IGDBObject,
        company_igdb_to_db_mapping: dict[int, Company],
        extra_mappings: dict[str, dict[int, Any]] | None = None,
    ) -> dict[str, str | int | None | datetime | date | Company | GameType | GameStatus | list[str]]:
        """
        Get the input for the model from the item from the IGDB database.

        Args:
            item_from_igdb (IGDBObject): The item from the IGDB database.
            company_igdb_to_db_mapping (dict[int, Company]): The mapping between IGDB companies and database companies.
            extra_mappings (dict[str, dict[int, Any]] | None): Extra mappings for game type and status.

        Returns:
            dict[str, str | int | None | datetime | date | Company | GameType | GameStatus | list[str]]: The input
                for the model.
        """
        model_input: dict[str, Any] = {
            "igdb_id": item_from_igdb.id,
            "igdb_updated_at": (
                datetime.fromtimestamp(item_from_igdb.updated_at, tz=UTC) if item_from_igdb.updated_at else None
            ),
        }
        match item_from_igdb:
            case IGDBGameResponse():
                model_input.update(
                    self._get_game_input(item_from_igdb, company_igdb_to_db_mapping, extra_mappings),
                )
            case (
                IGDBGenreResponse()
                | IGDBGameModeResponse()
                | IGDBPlayerPerspectiveResponse()
                | IGDBGameEngineResponse()
            ):
                model_input.update({"name": item_from_igdb.name})
            case IGDBGameTypeResponse():
                model_input.update(self._get_game_type_input(item_from_igdb))
            case IGDBGameStatusResponse():
                model_input.update(self._get_game_status_input(item_from_igdb))
            case IGDBPlatformResponse():
                model_input.update(self._get_platform_input(item_from_igdb))
            case IGDBCompanyResponse():
                model_input.update(self._get_company_input(item_from_igdb))
            case _:
                message_error = f"Invalid type of data from IGDB: {type(item_from_igdb)}"
                raise IGDBInteractionError(message_error)

        return model_input

    def _build_query(
        self: Self,
        query: str,
        model: type[ModelType],
        *,
        import_all: bool,
        import_start_timestamp: int | None,
    ) -> str:
        """Build the query string with appropriate time bounds."""
        last_updated_at = model.objects.aggregate(max_updated_at=Max("igdb_updated_at"))["max_updated_at"]

        where_clauses = []
        if last_updated_at and not import_all:
            timestamp = int(last_updated_at.timestamp())
            where_clauses.append(f"updated_at > {timestamp}")

        if import_start_timestamp:
            where_clauses.append(f"updated_at <= {import_start_timestamp}")

        if where_clauses:
            return f"{query} where {' & '.join(where_clauses)};"
        return query

    def _get_company_mapping(self: Self, unique_data_from_igdb: list[IGDBObject]) -> dict[int, Company]:
        """Get the mapping of IGDB company IDs to local Company objects for a batch of games."""
        company_ids = set()
        for data in unique_data_from_igdb:
            if isinstance(data, IGDBGameResponse) and data.involved_companies:
                for involved_company in data.involved_companies:
                    company_ids.add(involved_company.company)

        if company_ids:
            return {company.igdb_id: company for company in Company.objects.filter(igdb_id__in=company_ids)}
        return {}

    def _import_data(  # noqa: PLR0913
        self: Self,
        endpoint: IGDBEndpoints,
        query: str,
        model: type[ModelType],
        extra_mappings: dict[str, dict[int, Any]] | None = None,
        *,
        import_all: bool = False,
        import_start_timestamp: int | None = None,
    ) -> Iterator[tuple[list[ModelType], IGDBApiResponse]]:
        """Import data from the IGDB database to the application database.

        Args:
            endpoint (IGDBEndpoints): The IGDB endpoint to fetch data from.
            query (str): The query string for the IGDB API.
            model (type[ModelType]): The Django model class to map the IGDB data to.
            extra_mappings (dict[str, dict[int, Any]] | None): Extra mappings for model creation.
            import_all (bool): Whether to import all data ignoring last update time.
            import_start_timestamp (int | None): The timestamp when the import process started.

        Yields:
            Iterator[tuple[list[ModelType], IGDBApiResponse]]: A generator yielding a tuple containing
            a list of created model instances and the raw IGDB API response data for each batch.
        """
        query = self._build_query(query, model, import_all=import_all, import_start_timestamp=import_start_timestamp)

        self.stdout.write(f"Fetching data from IGDB endpoint: {endpoint.value}, query: {query}")

        for data_from_igdb in self.igdb_wrapper.iter_all_objects(endpoint=endpoint, query=query):
            if not data_from_igdb:
                continue

            # Deduplicate data_from_igdb based on id, keeping the last occurrence
            data_from_igdb_dict = {item.id: item for item in data_from_igdb}
            unique_data_from_igdb = list(data_from_igdb_dict.values())

            # Prepare mapping for companies if importing games
            company_igdb_to_db_mapping = {}
            if model == Game:
                company_igdb_to_db_mapping = self._get_company_mapping(unique_data_from_igdb)

            data_to_import = []
            update_fields: set[str] = set()

            for data in unique_data_from_igdb:
                model_input = self._get_model_input(
                    data,
                    company_igdb_to_db_mapping,
                    extra_mappings=extra_mappings,
                )
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

    def import_games(self: Self, *, import_all: bool = False, import_start_timestamp: int | None = None) -> None:
        """Import games from the IGDB database to the application database."""
        genre_igdb_to_db_mapping = {genre.igdb_id: genre.id for genre in Genre.objects.all()}
        platform_igdb_to_db_mapping = {platform.igdb_id: platform.id for platform in Platform.objects.all()}
        game_mode_igdb_to_db_mapping = {mode.igdb_id: mode.id for mode in GameMode.objects.all()}
        player_perspective_igdb_to_db_mapping = {pp.igdb_id: pp.id for pp in PlayerPerspective.objects.all()}
        game_engine_igdb_to_db_mapping = {engine.igdb_id: engine.id for engine in GameEngine.objects.all()}

        game_type_mapping = {gt.igdb_id: gt for gt in GameType.objects.all()}
        game_status_mapping = {gs.igdb_id: gs for gs in GameStatus.objects.all()}

        total_imported_games = 0

        query_fields = (
            "fields name, cover.image_id, first_release_date, genres, "
            "involved_companies.developer, involved_companies.publisher, involved_companies.company, "
            "platforms, summary, updated_at, "
            "game_type, game_status, parent_game, "
            "bundles, dlcs, expanded_games, expansions, forks, ports, standalone_expansions, "
            "game_engines, game_modes, player_perspectives, screenshots.image_id;"
        )

        collector = RecursiveDataCollector(
            parent_updates=[],
            recursive_m2m_data={
                "bundles": [],
                "dlcs": [],
                "expanded_games": [],
                "expansions": [],
                "forks": [],
                "ports": [],
                "standalone_expansions": [],
            },
            all_target_igdb_ids=set(),
        )

        extra_mappings: dict[str, Any] = {
            "game_type": game_type_mapping,
            "game_status": game_status_mapping,
        }

        for imported_games, igdb_games in self._import_data(
            endpoint=IGDBEndpoints.GAMES,
            query=query_fields,
            model=Game,
            extra_mappings=extra_mappings,
            import_all=import_all,
            import_start_timestamp=import_start_timestamp,
        ):
            total_imported_games += len(imported_games)
            self._process_game_batch(
                imported_games,
                igdb_games,
                {
                    "genres": genre_igdb_to_db_mapping,
                    "platforms": platform_igdb_to_db_mapping,
                    "game_modes": game_mode_igdb_to_db_mapping,
                    "player_perspectives": player_perspective_igdb_to_db_mapping,
                    "game_engines": game_engine_igdb_to_db_mapping,
                },
                collector,
            )

        self._handle_recursive_relations(collector)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created/updated {total_imported_games} 'Game' from the IGDB database."),
        )

    def _process_game_batch(
        self: Self,
        imported_games: list[Game],
        igdb_games: IGDBApiResponse,
        mappings: dict[str, dict[int, int]],
        collector: RecursiveDataCollector,
    ) -> None:
        """Process a batch of imported games and their relations."""
        rel_containers: dict[str, list[Any]] = {
            "genres": [],
            "platforms": [],
            "modes": [],
            "perspectives": [],
            "engines": [],
        }

        for imported_game, game_from_igdb in zip(imported_games, igdb_games, strict=True):
            if not (game_from_igdb and isinstance(game_from_igdb, IGDBGameResponse)):
                continue

            self._collect_simple_relations(imported_game, game_from_igdb, mappings, rel_containers)
            self._collect_recursive_relations(
                imported_game,
                game_from_igdb,
                collector,
            )

        self._bulk_create_simple_relations(rel_containers)

    def _collect_simple_relations(
        self: Self,
        imported_game: Game,
        game_from_igdb: IGDBGameResponse,
        mappings: dict[str, dict[int, int]],
        rel_containers: dict[str, list[Any]],
    ) -> None:
        if genres_ids := game_from_igdb.genres:
            rel_containers["genres"].extend(
                [
                    Game.genres.through(game_id=imported_game.id, genre_id=mappings["genres"][gid])
                    for gid in genres_ids
                    if gid in mappings["genres"]
                ],
            )
        if platform_ids := game_from_igdb.platforms:
            rel_containers["platforms"].extend(
                [
                    Game.platforms.through(game_id=imported_game.id, platform_id=mappings["platforms"][pid])
                    for pid in platform_ids
                    if pid in mappings["platforms"]
                ],
            )
        if mode_ids := game_from_igdb.game_modes:
            rel_containers["modes"].extend(
                [
                    Game.game_modes.through(game_id=imported_game.id, gamemode_id=mappings["game_modes"][mid])
                    for mid in mode_ids
                    if mid in mappings["game_modes"]
                ],
            )
        if pp_ids := game_from_igdb.player_perspectives:
            rel_containers["perspectives"].extend(
                [
                    Game.player_perspectives.through(
                        game_id=imported_game.id,
                        playerperspective_id=mappings["player_perspectives"][pid],
                    )
                    for pid in pp_ids
                    if pid in mappings["player_perspectives"]
                ],
            )
        if engine_ids := game_from_igdb.game_engines:
            rel_containers["engines"].extend(
                [
                    Game.game_engines.through(game_id=imported_game.id, gameengine_id=mappings["game_engines"][eid])
                    for eid in engine_ids
                    if eid in mappings["game_engines"]
                ],
            )

    def _collect_recursive_relations(
        self: Self,
        imported_game: Game,
        game_from_igdb: IGDBGameResponse,
        collector: RecursiveDataCollector,
    ) -> None:
        if game_from_igdb.parent_game:
            collector.parent_updates.append((imported_game.id, game_from_igdb.parent_game))
            collector.all_target_igdb_ids.add(game_from_igdb.parent_game)

        for field, target_list in collector.recursive_m2m_data.items():
            if targets := getattr(game_from_igdb, field):
                for t in targets:
                    target_list.append((imported_game.id, t))
                    collector.all_target_igdb_ids.add(t)

    def _bulk_create_simple_relations(
        self: Self,
        rel_containers: dict[str, list[Any]],
    ) -> None:
        Game.genres.through.objects.bulk_create(rel_containers["genres"], ignore_conflicts=True)
        Game.platforms.through.objects.bulk_create(rel_containers["platforms"], ignore_conflicts=True)
        Game.game_modes.through.objects.bulk_create(rel_containers["modes"], ignore_conflicts=True)
        Game.player_perspectives.through.objects.bulk_create(rel_containers["perspectives"], ignore_conflicts=True)
        Game.game_engines.through.objects.bulk_create(rel_containers["engines"], ignore_conflicts=True)

    def _handle_recursive_relations(
        self: Self,
        collector: RecursiveDataCollector,
    ) -> None:
        if not collector.all_target_igdb_ids:
            return

        self.stdout.write(self.style.NOTICE("Fetching game ID mapping..."))

        game_map = {
            item[1]: item[0]
            for item in Game.objects.filter(igdb_id__in=collector.all_target_igdb_ids).values_list("id", "igdb_id")
        }

        self.stdout.write(self.style.NOTICE("Game parents update - started."))

        to_update_parent = []
        for game_id, parent_igdb_id in collector.parent_updates:
            if parent_igdb_id in game_map:
                to_update_parent.append(Game(id=game_id, parent_game_id=game_map[parent_igdb_id]))

        if to_update_parent:
            # Using a sensible batch_size for bulk_update
            Game.objects.bulk_update(to_update_parent, ["parent_game"], batch_size=2000)

        self.stdout.write(self.style.NOTICE("Game parents update - finished."))

        for field, data in collector.recursive_m2m_data.items():
            self.stdout.write(self.style.NOTICE(f"Game {field} m2m relations - started."))
            m2m_model = getattr(Game, field).through
            m2m_objs = [
                m2m_model(from_game_id=src_id, to_game_id=game_map[tgt_igdb_id])
                for src_id, tgt_igdb_id in data
                if tgt_igdb_id in game_map
            ]
            if m2m_objs:
                # Using a sensible batch_size for bulk_create
                m2m_model.objects.bulk_create(m2m_objs, ignore_conflicts=True, batch_size=2000)

            self.stdout.write(self.style.NOTICE(f"Game {field} m2m relations - finished."))

    def import_companies(self: Self, *, import_all: bool = False, import_start_timestamp: int | None = None) -> None:
        """Import companies from the IGDB database to the application database."""
        total_companies = 0
        for created_companies, _ in self._import_data(
            endpoint=IGDBEndpoints.COMPANIES,
            query="fields name, logo.image_id, updated_at;",
            model=Company,
            import_all=import_all,
            import_start_timestamp=import_start_timestamp,
        ):
            total_companies += len(created_companies)

        self.stdout.write(
            self.style.SUCCESS(
                (f"Successfully created/updated {total_companies} 'Companies' from the IGDB database."),
            ),
        )

    def import_genres(self: Self, *, import_all: bool = False, import_start_timestamp: int | None = None) -> None:
        """Import genres from the IGDB database to the application database."""
        total_genres = 0
        for created_genres, _ in self._import_data(
            endpoint=IGDBEndpoints.GENRES,
            query=self.NAME_UPDATED_AT_QUERY,
            model=Genre,
            import_all=import_all,
            import_start_timestamp=import_start_timestamp,
        ):
            total_genres += len(created_genres)

        self.stdout.write(
            self.style.SUCCESS(
                (f"Successfully created/updated {total_genres} 'Genres' from the IGDB database."),
            ),
        )

    def import_platforms(self: Self, *, import_all: bool = False, import_start_timestamp: int | None = None) -> None:
        """Import platforms from the IGDB database to the application database."""
        total_platforms = 0
        for created_platforms, _ in self._import_data(
            endpoint=IGDBEndpoints.PLATFORMS,
            query="fields abbreviation, name, updated_at;",
            model=Platform,
            import_all=import_all,
            import_start_timestamp=import_start_timestamp,
        ):
            total_platforms += len(created_platforms)

        self.stdout.write(
            self.style.SUCCESS(
                (f"Successfully created/updated {total_platforms} 'Platforms' from the IGDB database."),
            ),
        )

    def import_game_modes(self: Self, *, import_all: bool = False, import_start_timestamp: int | None = None) -> None:
        """Import game modes from the IGDB database."""
        total_items = 0
        for created_items, _ in self._import_data(
            endpoint=IGDBEndpoints.GAME_MODES,
            query=self.NAME_UPDATED_AT_QUERY,
            model=GameMode,
            import_all=import_all,
            import_start_timestamp=import_start_timestamp,
        ):
            total_items += len(created_items)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created/updated {total_items} 'Game Modes' from the IGDB database."),
        )

    def import_player_perspectives(
        self: Self,
        *,
        import_all: bool = False,
        import_start_timestamp: int | None = None,
    ) -> None:
        """Import player perspectives from the IGDB database."""
        total_items = 0
        for created_items, _ in self._import_data(
            endpoint=IGDBEndpoints.PLAYER_PERSPECTIVES,
            query=self.NAME_UPDATED_AT_QUERY,
            model=PlayerPerspective,
            import_all=import_all,
            import_start_timestamp=import_start_timestamp,
        ):
            total_items += len(created_items)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created/updated {total_items} 'Player Perspectives' from the IGDB database.",
            ),
        )

    def import_game_engines(self: Self, *, import_all: bool = False, import_start_timestamp: int | None = None) -> None:
        """Import game engines from the IGDB database."""
        total_items = 0
        for created_items, _ in self._import_data(
            endpoint=IGDBEndpoints.GAME_ENGINES,
            query=self.NAME_UPDATED_AT_QUERY,
            model=GameEngine,
            import_all=import_all,
            import_start_timestamp=import_start_timestamp,
        ):
            total_items += len(created_items)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created/updated {total_items} 'Game Engines' from the IGDB database."),
        )

    def import_game_types(self: Self, *, import_all: bool = False, import_start_timestamp: int | None = None) -> None:
        """Import game types from the IGDB database."""
        total_items = 0
        for created_items, _ in self._import_data(
            endpoint=IGDBEndpoints.GAME_TYPES,
            query="fields type, updated_at;",
            model=GameType,
            import_all=import_all,
            import_start_timestamp=import_start_timestamp,
        ):
            total_items += len(created_items)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created/updated {total_items} 'Game Types' from the IGDB database."),
        )

    def import_game_statuses(
        self: Self,
        *,
        import_all: bool = False,
        import_start_timestamp: int | None = None,
    ) -> None:
        """Import game statuses from the IGDB database."""
        total_items = 0
        for created_items, _ in self._import_data(
            endpoint=IGDBEndpoints.GAME_STATUSES,
            query="fields status, updated_at;",
            model=GameStatus,
            import_all=import_all,
            import_start_timestamp=import_start_timestamp,
        ):
            total_items += len(created_items)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created/updated {total_items} 'Game Statuses' from the IGDB database."),
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
            "game_modes": self.import_game_modes,
            "player_perspectives": self.import_player_perspectives,
            "game_engines": self.import_game_engines,
            "game_types": self.import_game_types,
            "game_statuses": self.import_game_statuses,
        }

        import_all = bool(options.get("all", False))
        import_start_timestamp = int(datetime.now(tz=UTC).timestamp())

        for item in options["what_to_import"]:
            action = actions.get(item)
            if action:
                try:
                    action(import_all=import_all, import_start_timestamp=import_start_timestamp)
                except Exception as e:  # noqa: BLE001
                    self.stdout.write(self.style.ERROR(f"Error importing {item}: {e}"))
            time.sleep(1)  # To avoid hitting IGDB rate limits

        self.stdout.write(
            self.style.SUCCESS("Import process completed."),
        )
