"""Project-wide string constants."""

# ---------------------------------------------------------------------------
# Public bot — callback data
# ---------------------------------------------------------------------------
CB_STATE_PREFIX: str = "state:"
CB_BACK_TO_STATES: str = "back_to_states"
CB_DELIVERY_ONLY_PREFIX: str = "delivery_only:"
CB_DELIVERY_ALL_PREFIX: str = "delivery_all:"

# Pagination
CB_PAGE_PREFIX: str = "page:"
ITEMS_PER_PAGE: int = 10

# Search
CB_SEARCH: str = "search"
CB_SEARCH_RESULT_PREFIX: str = "search_result:"

# ---------------------------------------------------------------------------
# Public bot — messages
# ---------------------------------------------------------------------------
MSG_WELCOME: str = (
    "👋 <b>Welcome to USA Restaurants Bot!</b>\n\n"
    "Choose a state to explore restaurants:"
)
MSG_NO_RESTAURANTS: str = "No restaurants found for this state."
MSG_NO_DELIVERY: str = "😔 No delivery restaurants found in this state."
MSG_STATE_NOT_FOUND: str = "State not found."
MSG_SEARCH_PROMPT: str = (
    "🔍 <b>Search a state</b>\n\n"
    "Type part of the state name (e.g. <code>new</code> or <code>New York</code>):"
)
MSG_SEARCH_NO_RESULTS: str = "😔 No states found. Try a different query."
MSG_PAGE_INFO: str = "Page {page} of {total}"

BTN_DELIVERY_ONLY: str = "🚚 Delivery Only"
BTN_SHOW_ALL: str = "🔄 Show All"
BTN_BACK_TO_STATES: str = "⬅ Back to States"
BTN_SEARCH: str = "🔍 Search State"
BTN_PREV_PAGE: str = "◀️ Prev"
BTN_NEXT_PAGE: str = "▶️ Next"

# ---------------------------------------------------------------------------
# Admin panel — callback data
# ---------------------------------------------------------------------------
CB_ADMIN_ADD: str = "admin:add"
CB_ADMIN_EDIT: str = "admin:edit"
CB_ADMIN_DELETE: str = "admin:delete"
CB_ADMIN_LIST: str = "admin:list"
CB_ADMIN_EXIT: str = "admin:exit"
CB_ADMIN_BACK_MENU: str = "admin:back_menu"

CB_ADMIN_STATE_PREFIX: str = "adm_state:"
CB_ADMIN_DELIVERY_YES: str = "adm_delivery:yes"
CB_ADMIN_DELIVERY_NO: str = "adm_delivery:no"
CB_ADMIN_CONFIRM_YES: str = "adm_confirm:yes"
CB_ADMIN_CONFIRM_NO: str = "adm_confirm:no"

CB_ADMIN_EDIT_SELECT_PREFIX: str = "adm_edit_sel:"
CB_ADMIN_EDIT_FIELD_PREFIX: str = "adm_edit_field:"
CB_ADMIN_DEL_STATE_PREFIX: str = "adm_del_state:"
CB_ADMIN_DEL_REST_PREFIX: str = "adm_del_rest:"
CB_ADMIN_DEL_CONFIRM_PREFIX: str = "adm_del_confirm:"
CB_ADMIN_LIST_STATE_PREFIX: str = "adm_list_state:"

# ---------------------------------------------------------------------------
# Admin panel — messages
# ---------------------------------------------------------------------------
MSG_ACCESS_DENIED: str = "⛔ Access denied."
MSG_ADMIN_WELCOME: str = "🛠 <b>Admin Panel</b>\n\nChoose an action:"
MSG_ADMIN_CHOOSE_STATE: str = "Select a <b>state</b> for the new restaurant:"
MSG_ADMIN_ENTER_NAME: str = "Enter the restaurant <b>name</b>:"
MSG_ADMIN_ENTER_PHONE: str = "Enter the restaurant <b>phone</b>:"
MSG_ADMIN_ENTER_ADDRESS: str = "Enter the restaurant <b>address</b>:"
MSG_ADMIN_ENTER_DELIVERY: str = "Does the restaurant offer <b>delivery</b>?"
MSG_ADMIN_ENTER_TELEGRAM: str = (
    "Enter the <b>Telegram link</b> (or send <code>-</code> to skip):"
)
MSG_ADMIN_ENTER_MAPS: str = "Enter the <b>Google Maps link</b>:"
MSG_ADMIN_CHOOSE_EDIT_STATE: str = "Select the <b>state</b> of the restaurant to edit:"
MSG_ADMIN_CHOOSE_DEL_STATE: str = "Select the <b>state</b> of the restaurant to delete:"
MSG_ADMIN_CHOOSE_LIST_STATE: str = "Select a <b>state</b> to view its restaurants:"

BTN_ADD: str = "➕ Add Restaurant"
BTN_EDIT: str = "✏️ Edit Restaurant"
BTN_DELETE: str = "🗑 Delete Restaurant"
BTN_LIST: str = "📋 View Restaurants"
BTN_EXIT: str = "❌ Exit"
BTN_BACK_ADMIN: str = "⬅ Back to Admin Menu"
BTN_YES: str = "✅ Yes"
BTN_NO: str = "❌ No"
BTN_CONFIRM: str = "✅ Confirm"
BTN_CANCEL: str = "❌ Cancel"

EDIT_FIELDS: dict[str, str] = {
    "name": "Name",
    "phone": "Phone",
    "address": "Address",
    "delivery": "Delivery",
    "telegram": "Telegram link",
    "maps": "Maps link",
}