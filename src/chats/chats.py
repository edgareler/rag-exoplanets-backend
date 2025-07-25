from datetime import datetime
from nanoid import generate as nanoid
from src.chats.types import Chat
from src.database.client import get_client
from src.database.tables import CHATS_TABLE
from src.database.utils import page_to_range, build_response

async def create_chat(user_id: str) -> str:
  chat_date = datetime.now().isoformat()
  supabase = await get_client()
  response = await (
    supabase.table(CHATS_TABLE)
    .insert({
      "id": nanoid(),
      "user_id": user_id,
      "created_at": chat_date,
    })
    .execute()
  )
  return response

async def read_chat(chat: Chat):
  supabase = await get_client()
  response = await (
    supabase.table(CHATS_TABLE)
    .select("*")
    .eq("id", chat.id)
    .eq("user_id", chat.user_id)
    .execute()
  )
  if len(response.data) == 0:
    return None
  return response.data[0]

async def list_chats(user_id: str, page: int = 1, page_size: int = 10):
  range = page_to_range(page, page_size)

  supabase = await get_client()
  response = await (
    supabase.table(CHATS_TABLE)
    .select("*", count="exact")
    .eq("user_id", user_id)
    .order("created_at", desc=True)
    .range(range.start, range.end)
    .execute()
  )

  return build_response(response, page, page_size)

async def update_chat(
  chat: Chat,
  title: str,
  recent_history: list[dict],
  old_history: list[dict],
  old_history_summary: str
):
  supabase = await get_client()
  response = await (
    supabase.table(CHATS_TABLE)
    .update({
      "title": title,
      "recent_history": recent_history,
      "old_history": old_history,
      "old_history_summary": old_history_summary,
    })
    .eq("id", chat.id)
    .eq("user_id", chat.user_id)
    .execute()
  )
  return response
