from .. import auth as auth, errors as errors, utils as utils
from ..constants import DEFAULT_DATA_CHUNK_SIZE as DEFAULT_DATA_CHUNK_SIZE
from _typeshed import Incomplete

log: Incomplete

class ImageApiMixin:
    def get_image(self, image: Incomplete, chunk_size: Incomplete = ...) -> Incomplete: ...
    def history(self, image: Incomplete) -> Incomplete: ...
    def images(
        self, name: Incomplete | None = ..., quiet: bool = ..., all: bool = ..., filters: Incomplete | None = ...
    ) -> Incomplete: ...
    def import_image(
        self,
        src: Incomplete | None = ...,
        repository: Incomplete | None = ...,
        tag: Incomplete | None = ...,
        image: Incomplete | None = ...,
        changes: Incomplete | None = ...,
        stream_src: bool = ...,
    ) -> Incomplete: ...
    def import_image_from_data(
        self,
        data: Incomplete,
        repository: Incomplete | None = ...,
        tag: Incomplete | None = ...,
        changes: Incomplete | None = ...,
    ) -> Incomplete: ...
    def import_image_from_file(
        self,
        filename: Incomplete,
        repository: Incomplete | None = ...,
        tag: Incomplete | None = ...,
        changes: Incomplete | None = ...,
    ) -> Incomplete: ...
    def import_image_from_stream(
        self,
        stream: Incomplete,
        repository: Incomplete | None = ...,
        tag: Incomplete | None = ...,
        changes: Incomplete | None = ...,
    ) -> Incomplete: ...
    def import_image_from_url(
        self,
        url: Incomplete,
        repository: Incomplete | None = ...,
        tag: Incomplete | None = ...,
        changes: Incomplete | None = ...,
    ) -> Incomplete: ...
    def import_image_from_image(
        self,
        image: Incomplete,
        repository: Incomplete | None = ...,
        tag: Incomplete | None = ...,
        changes: Incomplete | None = ...,
    ) -> Incomplete: ...
    def inspect_image(self, image: Incomplete) -> Incomplete: ...
    def inspect_distribution(self, image: Incomplete, auth_config: Incomplete | None = ...) -> Incomplete: ...
    def load_image(self, data: Incomplete, quiet: Incomplete | None = ...) -> Incomplete: ...
    def prune_images(self, filters: Incomplete | None = ...) -> Incomplete: ...
    def pull(
        self,
        repository: Incomplete,
        tag: Incomplete | None = ...,
        stream: bool = ...,
        auth_config: Incomplete | None = ...,
        decode: bool = ...,
        platform: Incomplete | None = ...,
        all_tags: bool = ...,
    ) -> Incomplete: ...
    def push(
        self,
        repository: Incomplete,
        tag: Incomplete | None = ...,
        stream: bool = ...,
        auth_config: Incomplete | None = ...,
        decode: bool = ...,
    ) -> Incomplete: ...
    def remove_image(self, image: Incomplete, force: bool = ..., noprune: bool = ...) -> Incomplete: ...
    def search(self, term: Incomplete, limit: Incomplete | None = ...) -> Incomplete: ...
    def tag(
        self, image: Incomplete, repository: Incomplete, tag: Incomplete | None = ..., force: bool = ...
    ) -> Incomplete: ...

def is_file(src: Incomplete) -> Incomplete: ...
