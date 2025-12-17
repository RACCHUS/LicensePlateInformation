"""
Search Controller for License Plate Information System.

Wraps the existing JSONSearchEngine and provides search functionality
with debouncing and result categorization for the UI panels.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

from PySide6.QtCore import QObject, Signal, QTimer

# Add src to path for imports
src_dir = Path(__file__).parent.parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from gui.utils.json_search_engine import JSONSearchEngine

# Minimum characters required to start searching
MIN_SEARCH_CHARS = 2


@dataclass
class SearchResult:
    """A single search result."""
    state_code: str
    state_name: str
    field: str
    value: str
    match_type: str  # 'state_info' or 'plate_type'
    plate_type: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'state': self.state_code,
            'state_name': self.state_name,
            'field': self.field,
            'value': self.value,
            'match_type': self.match_type,
            'plate_type': self.plate_type
        }


@dataclass
class CategorizedResults:
    """Search results categorized by panel type."""
    query: str
    category: str
    state_filter: Optional[str]
    
    # Results by panel
    state_results: List[SearchResult] = field(default_factory=list)
    plate_type_results: List[SearchResult] = field(default_factory=list)
    char_rules_results: List[SearchResult] = field(default_factory=list)
    all_results: List[SearchResult] = field(default_factory=list)
    
    @property
    def total_count(self) -> int:
        return len(self.all_results)
    
    @property
    def state_count(self) -> int:
        # Count unique states
        return len(set(r.state_code for r in self.all_results))
    
    @property
    def is_empty(self) -> bool:
        return len(self.all_results) == 0


class SearchController(QObject):
    """
    Controller for search functionality.
    
    Provides debounced search with categorized results for UI panels.
    """
    
    # Signals
    search_started = Signal()
    search_completed = Signal(object)  # CategorizedResults
    search_cleared = Signal()
    search_error = Signal(str)
    
    # Category mappings for UI dropdown
    CATEGORIES = {
        'all': 'All Fields',
        'slogans': 'Slogans',
        'type': 'Plate Types',
        'fonts': 'Fonts',
        'colors': 'Colors',
        'handling_rules': 'Character Rules',
        'processing': 'Processing Rules',
    }
    
    # Fields that belong to character rules panel
    CHAR_RULES_FIELDS = {
        'uses_zero_for_o', 'allows_letter_o', 'zero_is_slashed',
        'character_formatting', 'stacked_characters', 'slanted_characters',
        'character_restrictions', 'vertical_handling', 'omit_characters',
        'character_modifications', 'font', 'main_font'
    }
    
    def __init__(self, parent=None, debounce_ms: int = 300):
        super().__init__(parent)
        
        self.engine = JSONSearchEngine()
        self.debounce_ms = debounce_ms
        self._debounce_timer = QTimer()
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.timeout.connect(self._execute_search)
        
        self._pending_query: str = ""
        self._pending_category: str = "all"
        self._pending_state_filter: Optional[str] = None
        
        self._last_results: Optional[CategorizedResults] = None
        self._is_searching = False
    
    @property
    def is_searching(self) -> bool:
        return self._is_searching
    
    @property
    def last_results(self) -> Optional[CategorizedResults]:
        return self._last_results
    
    def get_all_states(self) -> List[str]:
        """Get list of all available state codes."""
        return self.engine.get_all_state_codes()
    
    def search(
        self,
        query: str,
        category: str = 'all',
        state_filter: Optional[str] = None,
        immediate: bool = False
    ):
        """
        Perform a search with debouncing.
        
        Args:
            query: Search text (case-insensitive)
            category: Category to filter by (see CATEGORIES)
            state_filter: Optional state code to limit search
            immediate: If True, skip debounce and search immediately
        """
        self._pending_query = query.strip()
        self._pending_category = category
        self._pending_state_filter = state_filter
        
        if not self._pending_query:
            self.clear_search()
            return
        
        # Require minimum characters before searching
        if len(self._pending_query) < MIN_SEARCH_CHARS:
            self.clear_search()
            return
        
        if immediate:
            self._debounce_timer.stop()
            self._execute_search()
        else:
            # Restart debounce timer
            self._debounce_timer.stop()
            self._debounce_timer.start(self.debounce_ms)
    
    def clear_search(self):
        """Clear the current search and results."""
        self._debounce_timer.stop()
        self._pending_query = ""
        self._last_results = None
        self.search_cleared.emit()
    
    def _execute_search(self):
        """Execute the pending search."""
        if not self._pending_query:
            return
        
        self._is_searching = True
        self.search_started.emit()
        
        try:
            # Use existing search engine
            raw_results = self.engine.search(
                query=self._pending_query,
                category=self._pending_category,
                state_filter=self._pending_state_filter
            )
            
            # Convert and categorize results
            categorized = self._categorize_results(
                raw_results,
                self._pending_query,
                self._pending_category,
                self._pending_state_filter
            )
            
            self._last_results = categorized
            self.search_completed.emit(categorized)
            
        except Exception as e:
            self.search_error.emit(str(e))
        finally:
            self._is_searching = False
    
    def _categorize_results(
        self,
        raw_results: List[Dict],
        query: str,
        category: str,
        state_filter: Optional[str]
    ) -> CategorizedResults:
        """Categorize raw search results by panel type."""
        
        results = CategorizedResults(
            query=query,
            category=category,
            state_filter=state_filter
        )
        
        seen_states = set()
        
        for raw in raw_results:
            result = SearchResult(
                state_code=raw.get('state', ''),
                state_name=raw.get('state_name', ''),
                field=raw.get('field', ''),
                value=str(raw.get('value', '')),
                match_type=raw.get('match_type', ''),
                plate_type=raw.get('plate_type')
            )
            
            results.all_results.append(result)
            
            # Categorize by panel
            field_lower = result.field.lower()
            
            # Character rules panel
            if any(cf in field_lower for cf in self.CHAR_RULES_FIELDS):
                results.char_rules_results.append(result)
            
            # Plate type panel
            if result.match_type == 'plate_type' or result.plate_type:
                results.plate_type_results.append(result)
            
            # State info panel (unique states only)
            if result.state_code not in seen_states:
                seen_states.add(result.state_code)
                results.state_results.append(result)
        
        return results
    
    def get_state_data(self, state_code: str) -> Dict[str, Any]:
        """Get full data for a specific state."""
        return self.engine.load_state_data(state_code)
