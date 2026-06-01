from typing import Union

from contracts.errors.handled_token import HandledToken
from .embedding_generation_error import EmbeddingGenerationError
from .query_error import QueryError
from .unsupported_feature_exception import UnsupportedFeatureException
from .database_failed_operation import DataBaseFailedOpertaion
from .handled_token import HandledToken
from .unexpected_error import UnexpectedError
AppError = Union[QueryError, EmbeddingGenerationError, UnsupportedFeatureException,DataBaseFailedOpertaion, HandledToken,UnexpectedError]