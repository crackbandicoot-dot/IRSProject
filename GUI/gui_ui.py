from typing import List, assert_never

from contracts.rich_result.rich_result import RichResult
from .GUI import GUI
from contracts.either import Either,Ok,Error
from contracts.errors import QueryError, EmbeddingGenerationError, UnsupportedFeatureException, AppError
_gui = GUI()


def wait_query() -> str:
    return _gui.wait_query()


def show_result(search_results_either: Either[AppError,List[RichResult]]) -> None:
    #Currently the UI just handle the happy path.You
    #should extend the bevaior to also display errors feedback to user
    match search_results_either:
        case Ok(search_results):
            _gui.show_result(search_results)
        case Error(app_error):
            match app_error:
                case QueryError():
                    return
                case EmbeddingGenerationError():
                    return
                case UnsupportedFeatureException():
                    return
                case _:
                    assert_never(app_error)
        case _:
            assert_never(search_results_either)
               
        
        
